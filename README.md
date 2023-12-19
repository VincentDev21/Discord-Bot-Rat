#  Discord-Bot-Rat
Discord Remote Administration Tool that is fully written in Python3.

This RAT is controlled using Discord with 15 commands and more coming.
# Disclaimer:
This tool is for educational use only, the author will not be held responsible for any misuse of this tool.
# Commands
```
!cd [new_path]: Changes the current working directory. If no argument is provided, it defaults to the user's home directory.
!download [file_path]: Sends a file as a Discord attachment. Assumes the file is in the current working directory.
!ls: Lists the files in the current working directory and sends the list as a Discord attachment.
!create [file_name]: Creates a file with the specified name in the current working directory.
!pwd: Shows the current working directory.
!delete_files: Deletes the temporary file used in the !ls command.
!shutdown: Shuts down the bot.
!grab: Decrypts Chrome passwords and sends them as a CSV file.
!ss: Takes a screenshot and sends it as an embedded image.
!sysinfo: Displays basic system information.
!sysspecs: Displays more detailed system specifications.
!drive [list|cd] [drive_name]: Lists available drives or changes the directory to a specified drive.
!capture: Captures an image from the webcam and sends it as an embedded message.
!upload: Uploads files attached to the Discord message.
!join: Joins a voice channel specified by target_channel_id and plays the victim's microphone. (Work in progress)
!log [on|off|delete] [channel_name]: Starts or stops logging key presses to a specific channel.
```

# Instructions:
You first need to register a bot at the Discord developer portal and then add the bot to a Discord server to control the program (Make sure that the bot has admin privileges in the Discord server). Once created, copy the token from the portal and replace it with the text "REPLACE_WITH_YOUR_TOKEN" with your token which is located at the very bottom of the index.py file. 
1. Clone/Download the current [repository](https://github.com/VincentDev21/Discord-Bot-Rat)

3. Install Requirements
  ```
  pip install -r requirements.txt
  ```
3. Run the program
  ```
  python -u index.py
  ```
## Optional
You can turn the python file into a exe by following these simple steps
1. install the pyinstaller by running this command:
```
pip install pyinstaller
```
2. run this command while in the current working directory
```
pyinstaller --onefile index.py
```
# To Do

In the future, I may consider implementing the following features:
- Re-write code to make code more readable
- Add more commands with different exploits
