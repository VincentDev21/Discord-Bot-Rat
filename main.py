import os
import getpass
import win32com.client

def create_startup_shortcut(file_path):
    # Get the current user's Startup folder path
    startup_folder = os.path.join(
        "C:\\Users", getpass.getuser(), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup"
    )

    # Create a shortcut file in the Startup folder
    shortcut_name = os.path.splitext(os.path.basename(file_path))[0] + ".lnk"
    shortcut_path = os.path.join(startup_folder, shortcut_name)

    # Create the shortcut using the file path
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = file_path
    shortcut.WorkingDirectory = os.path.dirname(file_path)
    shortcut.Save()

if __name__ == "__main__":
    # Specify the Python file you want to run on startup
    python_file_path = "C:\\Users\\Ling\\Desktop\\Discord-ratv2\\index.py"

    # Check if the file exists
    if not os.path.isfile(python_file_path):
        print("The specified file does not exist.")
    else:
        # Create the shortcut in the Startup folder
        create_startup_shortcut(python_file_path)
        print("Shortcut created successfully.")
