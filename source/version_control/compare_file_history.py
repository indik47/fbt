import subprocess
import os
import time
import tkinter as tk
from tkinter import ttk, scrolledtext
import re
import json

import unreal

UI = []


def setup_p4(P4USER, P4PORT, P4CLIENT):
    
    success = False

    # Build the p4 command
    p4_set_commands = [["p4", "set", f'P4USER={P4USER}'], ["p4", "set", f'P4PORT={P4PORT}'], ["p4", "set", f'P4CLIENT={P4CLIENT}']]

    # Run the command and capture the output
    try:
        for p4_command in p4_set_commands:
            result = subprocess.run(p4_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        success=True
        return success
    
    except subprocess.CalledProcessError as e:
        log(UI[0], f"Error: {e}\n{e.stderr}")
        return success
    

def query_file_history(file_path, client):
    # Check if the required environment variables are set

    # Build the p4 command
    p4_command = ["p4", "-c", client, "filelog", "-L",  file_path]

    # Run the command and capture the output
    try:
        result = subprocess.run(p4_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return result.stdout
    
    except subprocess.CalledProcessError as e:
        log(UI[0], f"Error: {e}\n{e.stderr}")
        return None


def construct_file_path(client_root):
    if not client_root:
        return
    
    unreal.log_warning(client_root)
    
    if '\\' in client_root:
        client_root = client_root.replace('\\\\', '\\')
    
    if client_root in SOURCE_FILE_PATH:
        return SOURCE_FILE_PATH
    
    else:
        end = re.findall(r"\\MK12\\Content\\.+", SOURCE_FILE_PATH)
        if end:
            return client_root + end[0]
        else:
            return None


def parse_perforce_history(output):
    # Define a regular expression for the desired lines
    # history_entry_pattern = re.compile(r'\.\.\. #(\d+) change (\d+) edit on (\d{4}/\d{2}/\d{2}) by (.+?) \(binary\+l\)\n\n\t(.+\n?.+)\n\n', re.DOTALL)
    history_entry_pattern = re.compile(r'\.\.\. #(\d+) change (\d+) .+on (\d{4}/\d{2}/\d{2}) by (.+?) \(binary\+l\)\n\n(.+\n*.+)\n\n')

    # Find all matches in the entire output
    matches = history_entry_pattern.finditer(output)

    # Initialize a list to store parsed information
    history_entries = []

    # Iterate over each match
    for match in matches:
        entry_info = {
            'change_number': match.group(1),
            'change_id': match.group(2),
            'change_date': match.group(3),
            'user': match.group(4),
            'description': match.group(5).strip()  # Remove leading/trailing whitespaces
        }
        history_entries.append(entry_info)

    return history_entries


def log(ui, message):
    ui.insert(tk.END, f"{message}\n")
    # ui.see(tk.END)  # Scroll to the end


def load_cached_p4_data(filename = 'p4data.json'):
    # Get the script's directory
    script_dir = os.path.dirname(os.path.realpath(__file__))
    user = None
    server = None
    switch_workspace = None
    main_workspace = None

    # Create a path to the JSON file in the script's directory
    file_path = os.path.join(script_dir, filename)

    # Check if the file already exists
    if os.path.exists(file_path):
        # If it does, read the existing file
        with open(file_path, "r") as json_file:
            existing_data = json.load(json_file)
            user = existing_data.get('user')
            server = existing_data.get('server')
            switch_workspace = existing_data.get('switch_workspace')
            main_workspace = existing_data.get('main_workspace')
            
    else:
        pass
    
    return user, server, switch_workspace, main_workspace

  
def save_to_json(data_dict, filename="p4data.json"):
    # Get the script's directory
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Create a path to the JSON file in the script's directory
    file_path = os.path.join(script_dir, filename)
    
    if os.path.exists(file_path):
        # If it does, read the existing file
        with open(file_path, "r") as json_file:
            existing_data = json.load(json_file)
            new_data = {**existing_data, **data_dict}
            
            # Write the dictionary to the JSON file
            with open(file_path, "w") as json_file:
                json.dump(new_data, json_file) 
            
            return new_data
    else:
        # Write the dictionary to the JSON file
        with open(file_path, "w") as json_file:
            json.dump(data_dict, json_file)   
        

def get_client_root(client):
    p4_command = ["p4", "-c", client, "info"]

    # Run the command and capture the output
    try:
        info_output = subprocess.run(p4_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except subprocess.CalledProcessError as e:
        # log(log_text_switch, f"Error: {e}\n{e.stderr}")
        return None  

    if info_output:
        # Define a regular expression to match the "Client root" line
        client_root_pattern = re.compile(r'Client root:\s+(.+)')

        # Search for the pattern in the output
        match = client_root_pattern.search(info_output.stdout)

        if match:
            # Return the matched client root
            return match.group(1)
        else:
            # Return None if the pattern is not found
            return None


def print_parsed_(ui, result):
    if result:
        parsed_result = parse_perforce_history(result)
        for entry in parsed_result:
            log(ui, f"Change #{entry['change_number']}  CL{entry['change_id']}  {entry['change_date']}")
            log(ui, f"User: {entry['user']}")
            log(ui, f"Message: {entry['description']}")
            log(ui, "\n")
    else:
        log(ui, f"No file history")


def validate_loaded_p4_data(user, server, switch_workspace, main_workspace):
    
    switch_data_valid = True
    main_data_valid = True
    
    for k in [user, server, switch_workspace]:
        if not k:
            switch_data_valid = False
    # no main repo
        for k in [main_workspace]:
            if not k:
                main_data_valid = False
    
    return switch_data_valid, main_data_valid


class MainUI:
    def __init__(self, master):
        self.master = master
        self.root = self.initUI()
        
        self.root.after(100, self.run)

    
    def initUI(self):
        # GUI setup
        root = tk.Tk()
        root.title("Perforce File History Query")

        frame = ttk.Frame(root, padding="10")
        frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        file_path_label = ttk.Label(frame, width=10, text="")
        file_path_label.grid(column=0, row=0, sticky=tk.W)

        file_path_label = ttk.Label(frame, width=100, text="")
        file_path_label.grid(column=1, row=0, sticky=tk.W)

        query_button = ttk.Button(frame, text="Perforce data", command=self.on_button_reenter_p4_data_click)
        query_button.grid(column=1, row=0, sticky=tk.W)

        result_label = ttk.Label(frame, text="Result:")
        result_label.grid(column=0, row=1, sticky=tk.W)

        result_text = tk.StringVar()
        result_display = ttk.Label(frame, textvariable=result_text, wraplength=400)
        result_display.grid(column=1, row=1, columnspan=2, sticky=tk.W)

        log_text_switch = scrolledtext.ScrolledText(frame, width=80, height=40, wrap=tk.WORD)
        log_text_switch.grid(column=1, row=2, columnspan=1, sticky=(tk.W, tk.E))
        UI.append(log_text_switch)

        log_text_main = scrolledtext.ScrolledText(frame, width=80, height=40, wrap=tk.WORD)
        log_text_main.grid(column=2, row=2, columnspan=3, sticky=(tk.W, tk.E))
        UI.append(log_text_main)

        return root
      
    def actualize_p4_data(self, force=False):
        user, server, switch_workspace, main_workspace = load_cached_p4_data()
                
        if force:
            server, user, switch_workspace, child_window = self.enter_p4_switch_data()
            main_workspace = self.enter_p4_main_data()

            if None or '' in [server, user, switch_workspace, main_workspace]:
                return None
            
            data = {'user':user, 'server':server, 'switch_workspace':switch_workspace, 'main_workspace':main_workspace}
            save_to_json(data)
            
        else:
            switch_data_valid, main_data_valid = validate_loaded_p4_data(user, server, switch_workspace, main_workspace)
            if not switch_data_valid:
                server, user, switch_workspace, child_window = self.enter_p4_switch_data()
                
            if not main_data_valid:
                main_workspace = self.enter_p4_main_data()
            
            if None or '' in [server, user, switch_workspace, main_workspace]:
                return None
            
            data = {'user':user, 'server':server, 'switch_workspace':switch_workspace, 'main_workspace':main_workspace}
            save_to_json(data)
            
        return data
    
    def on_button_reenter_p4_data_click(self):
        self.p4_data = self.actualize_p4_data(force=True)
        if not self.p4_data:
            unreal.log_warning('sdfsfsdf')
            return
        
        self.query()
    
    def query(self):
        if not SOURCE_FILE_PATH:
            log(UI[0], 'Source file path of the asset could not be found')
            return
        
        workspaces = self.p4_data['switch_workspace'], self.p4_data['main_workspace']        
        for i, workspace in enumerate(workspaces):
            setup_success = setup_p4(self.p4_data['user'], self.p4_data['server'], workspace)
            if not setup_success:
                log(UI[0], 'P4 setup was not successfull. Try re-enter P4User, P4server and Workspaces')
                return
            
            workspace_root_dir = get_client_root(workspace)
            if not workspace_root_dir:
                log(UI[i], f'workspace_root_dir could not be found for {workspace}')
                return
                
            file_path =  construct_file_path(workspace_root_dir)
            if not file_path:
                log(UI[i], f'File path of the asset could not be found for {workspace_root_dir}')
                return
            
            log(UI[i], file_path)
            log(UI[i], '\n')
            
            result = query_file_history(file_path, workspace)
            
            print_parsed_(UI[i], result)
            
    def enter_p4_switch_data(self):
        try:
            data_form = SwitchDataEntryForm(self.root)
            self.root.wait_window(data_form.root)  # Wait for the data entry form to be closed
        except:
            unreal.log_warning('Main window closed')
            return None, None, None, None
        
        return data_form.server, data_form.user, data_form.switch_workspace, data_form

    def enter_p4_main_data(self):
        try:
            data_form = MainDataEntryForm(self.root)
            self.root.wait_window(data_form.root)  # Wait for the data entry form to be closed     
        except:
            unreal.log_warning('Main window closed')
            return None
                
        return data_form.main_workspace

    def cancel(self):
        self.root.destroy()  # Close the Tkinter window
    
    def on_close(self):
        self.cancel()  
        
    def run(self):
        self.p4_data = self.actualize_p4_data()
        
        if not self.p4_data:
            return
        
        self.query()
    
           
class DataEntryForm:
    def __init__(self, master):
        self.master = master
        self.result = None  # Initialize result attribute

    def initUI(self, master):
        pass

    def save_values(self):
        pass

    def cancel(self):
        self.master.deiconify()
        self.master.focus_set()
        
        self.root.destroy()  # Close the Tkinter window

    def on_close(self):
        self.cancel()
        # Explicitly give focus back to the main window

        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.master.winfo_screenwidth() - width) // 2
        y = (self.master.winfo_screenheight() - height) // 2
        self.root.geometry(f"+{x}+{y}")
    
          
class SwitchDataEntryForm(DataEntryForm):
    def __init__(self, master):
        super().__init__(master)
        self.initUI(master)
        self.server = ''
        self.user = ''
        self.switch_workspace = ''

    def initUI(self, master):
        # Create the Tkinter window for data entry
        self.root = tk.Toplevel(master)
        self.root.title("Switch Repository")
        
        self.root.grab_set()

        # Labels, entry widgets, and buttons (same as the previous script)
        self.label1 = tk.Label(self.root, text="Server")
        self.label2 = tk.Label(self.root, text="User")
        self.label3 = tk.Label(self.root, text="Switch Workspace")

        self.entry1 = tk.Entry(self.root, width=50)
        self.entry2 = tk.Entry(self.root, width=50)
        self.entry3 = tk.Entry(self.root, width=50)
        
        user, server, switch_workspace, main_workspace = load_cached_p4_data()
    
        if server:
            self.entry1.delete(0, tk.END)
            self.entry1.insert(0, server) 
        else:
            self.entry1.delete(0, tk.END)
            self.entry1.insert(0, 'ssl:nrs-p4-ext-euwe2.netherrealm.com:1666')
        
        if user:
            self.entry2.delete(0, tk.END)
            self.entry2.insert(0, user)        
                
        if switch_workspace:
            self.entry3.delete(0, tk.END)
            self.entry3.insert(0, switch_workspace)

        self.save_button = tk.Button(self.root, width=10, text="Save", command=self.save_values)
        self.cancel_button = tk.Button(self.root, width=10, text="Cancel", command=self.cancel)

        # Grid layout
        self.label1.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry1.grid(row=0, column=1, padx=10, pady=5)
        
        self.label2.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry2.grid(row=1, column=1, padx=10, pady=5)
        self.label3.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry3.grid(row=2, column=1, padx=10, pady=5)

        self.save_button.grid(row=3, column=0, columnspan=1, pady=10)
        self.cancel_button.grid(row=3, column=1, columnspan=2, pady=10)
        
        # Bind the custom function to the window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Center the window on the master window
        self.center_window()
        
    def save_values(self):
        self.server = self.entry1.get()
        self.user = self.entry2.get()
        self.switch_workspace = self.entry3.get()
        
        self.master.deiconify()
        self.master.focus_set()
        
        self.root.destroy()  # Close the Tkinter window
      
        
class MainDataEntryForm(DataEntryForm):
    def __init__(self, master):
        super().__init__(master)
        self.initUI(master)
        self.main_workspace = ''

    def initUI(self, master):
        # Create the Tkinter window for data entry
        self.root = tk.Toplevel(master)
        self.root.title("Main repository")

        # Labels, entry widgets, and buttons (same as the previous script)
        self.label1 = tk.Label(self.root, text="Main workspace")
        self.entry1 = tk.Entry(self.root, width=50)

        self.save_button = tk.Button(self.root, width=10, text="Save", command=self.save_values)
        self.cancel_button = tk.Button(self.root, width=10, text="Cancel", command=self.cancel)

        # Grid layout
        self.label1.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry1.grid(row=0, column=1, padx=10, pady=5)
        
        user, server, switch_workspace, main_workspace = load_cached_p4_data()
        
        if main_workspace:
            self.entry1.delete(0, tk.END)
            self.entry1.insert(0, main_workspace)           
        
        self.save_button.grid(row=3, column=0, columnspan=1, pady=10)
        self.cancel_button.grid(row=3, column=1, columnspan=2, pady=10)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Center the window on the master window
        self.center_window()

    def save_values(self):
        self.main_workspace = self.entry1.get()
        self.root.destroy()


def get_file_path():
    selected = unreal.EditorUtilityLibrary.get_selected_assets()
    
    if len(selected) == 1:
        return unreal.SystemLibrary.get_system_path(selected[0])
    else:
        return None


SOURCE_FILE_PATH = None
SOURCE_FILE_PATH = get_file_path().replace('/', '\\')
unreal.log(SOURCE_FILE_PATH)

# SOURCE_FILE_PATH = r'C:\SwitchDevMinNSA\MK12\Content\Disk\Env\Hourglass\Map\BGND_Hourglass.umap'


main_app = MainUI(None)
# ttk.Style().theme_use('xpnative')
main_app.root.mainloop()




    

