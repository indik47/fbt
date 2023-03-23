import os
import subprocess
import platform

FILEBROWSER_PATH = os.path.join(os.getenv("WINDIR"), "explorer.exe")
NOTEPAD_PATH = r"C:\Program Files (x86)\Notepad++\notepad++.exe"


def explore(path):
    """Path can be a directory or a file
        directory -> open directory in WinExplorer
        file -> open in Notepad++"""

    # explorer would choke on forward slashes
    path = os.path.normpath(path)

    if os.path.exists(path):
        if os.path.isdir(path):
                if platform.system() == "Windows":
                    os.startfile(path)
                    
        elif os.path.isfile(path):
            subprocess.run([NOTEPAD_PATH, path])