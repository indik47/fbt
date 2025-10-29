from P4 import P4, P4Exception

# Configuration
P4PORT = "ssl:nrs-p4-ext-euwe2.netherrealm.com:1666"  # e.g., "ssl:perforce.example.com:1666"
P4USER = "x.denys.oligov"
P4PASSWORD = "wbgamesPERFORCE21"
FILE_PATH = "<FILE_PATH>"  # e.g., "//depot/path/to/file.txt"

def get_file_diff_previous_revision(p4port, p4user, p4password, file_path):
    p4 = P4()
    p4.port = p4port
    p4.user = p4user
    p4.password = p4password
    
    try:
        # Connect to the Perforce server
        p4.connect()
        # Login to the server
        p4.run_login(p4password)
        
        # Get the file history to find the current and previous revision numbers
        file_history = p4.run_filelog(file_path)
        if file_history and len(file_history[0].revisions) > 1:
            current_revision = file_history[0].revisions[0].rev
            previous_revision = file_history[0].revisions[1].rev
            
            # Format the file specs for the current and previous revisions
            current_file_spec = f"{file_path}#{current_revision}"
            previous_file_spec = f"{file_path}#{previous_revision}"
            
            # Get the diff between the current and previous revisions
            diff_output = p4.run_diff2(previous_file_spec, current_file_spec)
            
            # Print or process the diff output
            for line in diff_output:
                print(line)
        else:
            print("Not enough history for a diff.")
    except P4Exception as e:
        print("Perforce exception:", e)
    finally:
        p4.disconnect()

# Example usage
get_file_diff_previous_revision(P4PORT, P4USER, P4PASSWORD, FILE_PATH)