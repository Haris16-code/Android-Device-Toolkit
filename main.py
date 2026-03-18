import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.ttk import Progressbar
import subprocess
import webbrowser
import shutil
import os
import requests
import threading

# Constants
CURRENT_VERSION = "1.3"
UPDATE_INFO_URL = "https://raw.githubusercontent.com/Haris16-code/Android-Device-Toolkit/main/update_info.json"

def run_adb_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

def get_connected_devices():
    output = run_adb_command(['adb', 'devices'])
    devices = []

    for line in output.splitlines():
        if '\tdevice' in line:
            device_id = line.split('\t')[0]
            devices.append(device_id)

    return devices

def refresh_device_list():
    devices = get_connected_devices()
    listbox.delete(0, tk.END)

    if devices:
        for device in devices:
            listbox.insert(tk.END, device)
    else:
        listbox.insert(tk.END, "No devices connected")

def show_help():
    messagebox.showinfo("Help", "First of all install the adb commands just click on Install ADB Button on top it automatically install adb commands in your pc. Now Just connect Android Device to pc and make sure you enable usb debbuging on phone. After this click on refresh button. Now every things done now you use this tool fine.🤗. If you press on Install Apk and select apk file it directly install apk to phone. \nNew Commands uses\n1. (Reboot To Recovery) This command help you to boot your phone into recovery mode directly without pressing different key combination this feature help you to save your time because you dont need to press different keys just click on Reboot Your Device To Recovery button and it boot your phone directly into recovery mode\n2. (Power Button) This command is just like your power button you press it to wake up your device from sleep you better understand this by pressing this button and notice your phone\n3. (Open Calculator) This command help you to open calculator directly\n4. (Open Contacts) This command help you to open Contacts directly\n5. **Open Browser**: This command simulates pressing the Open Browser button on your phone, allowing you to quickly access your phone's web browser.\n6. 6. **Open Camera**: This command simulates pressing the Open Camera button on your phone, allowing you to open the camera app directly.\n7. **Check Device Serial No**: This command retrieves and displays your device's serial number.\n8. **Reset Battery Stats**: This command resets the battery stats on your device. It can be useful when troubleshooting battery issues.\n9. **Get Device Bug Report**: This command generates and retrieves a bug report from your device, which can be useful for debugging or reporting issues.\nTroubleshoot: Device Not Found even phone is connected and debugging is on?\nSolution: Dont Worry make sure adb commands is properly install now just press refresh button your can see your device serial no.\nHow to install update? \njust click on check for and if update is available it show dialog just click yes it say where you want to save new update you need save in another folder not in same folder when click save update is save when click on save file then update is save just double click and enjoy new update🤗")

def show_about():
    messagebox.showinfo("About", f"Android Device Toolkit\nVersion {CURRENT_VERSION}\nCreated by Muhammad Haris")

class DownloadProgressDialog:
    def __init__(self, root, total_size):
        self.progress_window = tk.Toplevel(root)
        self.progress_window.title("Downloading Update")
        
        self.progress_label = tk.Label(self.progress_window, text="Downloading Update...")
        self.progress_label.pack(pady=10)
        
        self.progress_bar = Progressbar(self.progress_window, length=300, mode='determinate')
        self.progress_bar.pack(pady=10)
        self.progress_bar["maximum"] = total_size
        self.progress_bar["value"] = 0
        
        self.bytes_downloaded = 0

    def update_progress(self, chunk_size):
        self.bytes_downloaded += chunk_size
        self.progress_bar["value"] = self.bytes_downloaded
        self.progress_window.update_idletasks()

    def close(self):
        self.progress_window.destroy()

def check_for_updates():
    try:
        response = requests.get(UPDATE_INFO_URL)
        update_info = response.json()

        new_version = update_info["version"]
        update_url = update_info["update_url"]
        whats_new = update_info["whats_new"]

        if new_version > CURRENT_VERSION:
            result = messagebox.askyesno("Update Available", f"A new version {new_version} is available. Do you want to update?\n\nWhat's new:\n{whats_new}")
            if result:
                save_folder = filedialog.askdirectory(title="Select Folder to Save Update")
                if save_folder:
                    download_update(update_url, new_version, save_folder)
                else:
                    messagebox.showinfo("Update Cancelled", "Update download cancelled.")
        else:
            messagebox.showinfo("No Update Available", "No new update is available.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to check for updates: {str(e)}")

def download_update(url, new_version, save_folder):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))

        # Extract filename from URL
        file_name = url.split("/")[-1]
        update_file_path = os.path.join(save_folder, file_name)

        # Write the downloaded content to the file
        with open(update_file_path, 'wb') as file:
            progress_dialog = DownloadProgressDialog(root, total_size)
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
                progress_dialog.update_progress(len(chunk))

            progress_dialog.close()

        messagebox.showinfo("Update Downloaded", f"Update file successfully downloaded and saved to:\n{update_file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to download update: {str(e)}")

    

    def download_thread():
        try:
            with open(file_path, 'wb') as file:
                downloaded = 0
                for data in response.iter_content(block_size):
                    file.write(data)
                    downloaded += len(data)
                    progress_bar["value"] = downloaded // block_size
                    progress_bar.update()
                    root.update()  # Update GUI to show progress

            progress.destroy()

            # Replace the old version with the new one
            replace_old_version(file_path, new_version)

        except Exception as e:
            messagebox.showinfo("Update Downloaded", f"Update downloaded now go to the folder where you select in download new update process and open the downloaded exe file. The new version of Android Device Toolkit is {new_version}")

    thread = threading.Thread(target=download_thread)
    thread.start()

def replace_old_version(file_path, new_version):
    current_executable = os.path.abspath(__file__)
    new_executable = os.path.join(os.path.dirname(current_executable), f"Android_Device_ToolKit_V{new_version}.exe")

    try:
        # Replace the old file with the new one
        shutil.copyfile(file_path, new_executable)
        os.remove(file_path)

        messagebox.showinfo("Update Complete", f"The software has been updated to version {new_version}. Now Go To same folder where you can save the Android Device Toolkit Application in same folder the you see the new file name as Android_Device_ToolKit_V{new_version}.exe just open that file and enjoy the new version")
        root.quit()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to replace old version: {str(e)}")

def install_apk():
    selected_file = filedialog.askopenfilename(filetypes=[("APK files", "*.apk")])
    if selected_file:
        selected_device = listbox.get(tk.ACTIVE)
        if selected_device and selected_device != "No devices connected":
            output = run_adb_command(['adb', '-s', selected_device, 'install', '-r', selected_file])
            info_text.delete(1.0, tk.END)
            info_text.insert(tk.END, output)
        else:
            messagebox.showerror("Error", "No device selected")

def install_adb():
    try:
        # Run the adb_installer.bat file
        result = subprocess.run(["latest_adb_installer.bat"], check=True)
        print("ADB installation process started.")
        
        # Check if the process completed successfully
        if result.returncode == 0:
            print("ADB installed successfully.")
    except FileNotFoundError:
        print("Error: adb_installer.bat file not found.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running adb_installer.bat: {e}")

commands = {
    "Battery Info": "shell dumpsys battery",
    "Device Properties": "shell getprop",
    "Reboot": "reboot",
    "Logcat": "logcat -d",
    "Reboot To Recovery Menu": "reboot recovery",
    "Power Button": "shell input keyevent 26",
    "Open Calculator": "shell input keyevent 210",
    "Open Contacts": "shell input keyevent 207",
    "Open Browser": "shell input keyevent 64",
    "Open Camera": "shell am start -a android.media.action.STILL_IMAGE_CAMERA",
    "Check Device Serial No": "get-serialno",
    "Reset Battery Stats": "shell dumpsys battery reset",
    "Get device bugs report": "bugreport"

}

def create_command_func(cmd):
    def command_func():
        selected_device = listbox.get(tk.ACTIVE)
        if selected_device and selected_device != "No devices connected":
            command = ['adb', '-s', selected_device] + cmd.split()
            output = run_adb_command(command)
            info_text.delete(1.0, tk.END)
            info_text.insert(tk.END, output)
        else:
            messagebox.showerror("Error", "No device selected")
    return command_func

def show_device_info(event):
    selected_device = listbox.get(tk.ACTIVE)
    if selected_device and selected_device != "No devices connected":
        output = run_adb_command(['adb', '-s', selected_device, 'shell', 'getprop'])
        info_text.delete(1.0, tk.END)
        info_text.insert(tk.END, output)

# Create the main window
root = tk.Tk()
root.title("Android Device ToolKit")

# Create a frame for the toolbar
toolbar = tk.Frame(root)
toolbar.pack(side=tk.TOP, fill=tk.X)
install_button = tk.Button(toolbar, text="Install ADB", command=install_adb)
install_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create buttons for Help, About, and Update
help_button = tk.Button(toolbar, text="Help", command=show_help)
help_button.pack(side=tk.LEFT, padx=5, pady=5)

about_button = tk.Button(toolbar, text="About", command=show_about)
about_button.pack(side=tk.LEFT, padx=5, pady=5)

update_button = tk.Button(toolbar, text="Check for Updates", command=check_for_updates)
update_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create a frame for the listbox and info display
main_frame = tk.Frame(root)
main_frame.pack(pady=20)

# Create a frame for the listbox and scrollbar
list_frame = tk.Frame(main_frame)
list_frame.pack(side=tk.LEFT, padx=10)

# Create a listbox to display the devices
listbox = tk.Listbox(list_frame, width=50, height=10)
listbox.pack(side=tk.LEFT)

# Create a scrollbar for the listbox
scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=listbox.yview)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)

# Create a text widget to display device info
info_text = tk.Text(main_frame, width=80, height=20)
info_text.pack(padx=10, side=tk.LEFT)

# Create a footer frame for additional buttons
footer_frame = tk.Frame(root)
footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Create buttons for predefined commands in the footer
for name, command in commands.items():
    button = tk.Button(footer_frame, text=name, command=create_command_func(command))
    button.pack(side=tk.LEFT, padx=5, pady=5)

# Create the Install APK button
install_apk_button = tk.Button(footer_frame, text="Install APK", command=install_apk)
install_apk_button.pack(side=tk.RIGHT, padx=5, pady=5)

# Create a refresh button
refresh_button = tk.Button(root, text="Click Me To Connect Your Device To Tool", command=refresh_device_list)
refresh_button.pack(side=tk.BOTTOM, padx=5, pady=5)

# Bind the listbox selection event to show device info
listbox.bind('<<ListboxSelect>>', show_device_info)

# Initial population of the list
refresh_device_list()


# Main loop
root.mainloop()
