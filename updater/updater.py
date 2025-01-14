import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import requests
import os
import subprocess
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger()

# Constants
MAIN_URL = "https://downloads.skydown.cloudns.org/updates/updates.txt"
MIRROR_URL = "https://skydown-archives.vercel.app/updates/updates.txt"
LOCAL_VERSION = "1.1.301.0"
DOWNLOAD_DIR = "downloads"

# Function to fetch update.txt
def fetch_update_config(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to fetch update config. HTTP Status: {response.status_code}")
    except Exception as e:
        logger.warning(f"Error fetching update config from {url}: {e}")
        return None

# Function to parse update.txt
def parse_update_config(config_text):
    if not config_text.lower().startswith(";vox_rythm_skydown;".lower()):
        raise ValueError("Invalid configuration file. Missing ';vox_rythm_skydown;' header.")

    settings = {}
    for line in config_text.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            settings[key.strip()] = value.strip()
    return settings

# Function to check for updates
def is_new_version_available(local_version, remote_version):
    return local_version < remote_version

# Function to download update file
def download_file(url, dest_path, progress_callback=None):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get("content-length", 0))
        with open(dest_path, "wb") as f:
            downloaded_size = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    if progress_callback:
                        progress_callback(downloaded_size, total_size)
    else:
        raise Exception(f"Failed to download file. HTTP Status: {response.status_code}")

# Function to run the downloaded .exe file
def run_executable(exe_path):
    subprocess.Popen([exe_path])
    sys.exit()

# GUI for the updater
class UpdaterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SkyDown Updater")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#2e2e2e")  # Dark background

        # Title Label
        self.label_title = ttk.Label(self.root, text="SkyDown Updater", font=("Helvetica", 18, "bold"), foreground="#ffffff", background="#2e2e2e")
        self.label_title.pack(pady=20)

        # Status Label
        self.label_status = ttk.Label(self.root, text="Checking for updates...", font=("Helvetica", 12), foreground="#ffffff", background="#2e2e2e")
        self.label_status.pack(pady=10)

        # Progress Bar
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=500, mode="determinate", maximum=100)
        self.progress_bar.pack(pady=20)

        # Buttons
        self.button_update = ttk.Button(self.root, text="Start Update", command=self.start_update_thread, state=tk.DISABLED, width=20, style="Accent.TButton")
        self.button_update.pack(pady=5)

        self.button_logs = ttk.Button(self.root, text="Show Logs", command=self.show_logs, width=20, style="TButton")
        self.button_logs.pack(pady=5)

        self.button_close = ttk.Button(self.root, text="Close", command=self.root.quit, width=20, style="TButton")
        self.button_close.pack(pady=20)

        # Log Window
        self.log_window = None

        # Update Logic
        self.update_info = None
        self.check_for_updates_thread()

    def check_for_updates_thread(self):
        threading.Thread(target=self.check_for_updates, daemon=True).start()

    def check_for_updates(self):
        try:
            logger.info("Fetching update configuration...")

            # Try the main URL first
            config_text = fetch_update_config(MAIN_URL) or fetch_update_config(MIRROR_URL)
            if not config_text:
                raise Exception("Failed to fetch update configuration from both main and mirror URLs.")

            self.update_info = parse_update_config(config_text)

            # Check for new version
            remote_version = self.update_info.get("UPDATE_VERSION")
            if is_new_version_available(LOCAL_VERSION, remote_version):
                logger.info(f"Update available: {remote_version}")
                self.label_status.config(text=f"Update available: {remote_version}")
                self.button_update.config(state=tk.NORMAL)
            else:
                logger.info("No updates available.")
                self.label_status.config(text="No updates available.")
        except Exception as e:
            logger.error(f"Failed to check for updates: {e}")
            messagebox.showerror("Error", f"Failed to check for updates: {e}")
            self.label_status.config(text="Update check failed.")

    def start_update_thread(self):
        threading.Thread(target=self.start_update, daemon=True).start()

    def start_update(self):
        try:
            # Download the update
            os.makedirs(DOWNLOAD_DIR, exist_ok=True)
            update_url = self.update_info.get("GIT_EXE_URL")
            downloaded_file = os.path.join(DOWNLOAD_DIR, "update.exe")

            logger.info("Starting update...")
            self.label_status.config(text="Downloading update...")
            self.root.update_idletasks()

            def progress_callback(downloaded, total):
                percent = int((downloaded / total) * 100)
                self.progress_bar["value"] = percent
                self.root.update_idletasks()

            download_file(update_url, downloaded_file, progress_callback)

            # Run the downloaded .exe file
            self.label_status.config(text="Running update...")
            logger.info("Running downloaded .exe file.")
            run_executable(downloaded_file)

        except Exception as e:
            logger.error(f"Update failed: {e}")
            messagebox.showerror("Error", f"Update failed: {e}")
            self.label_status.config(text="Update failed.")

    def show_logs(self):
        if self.log_window:
            self.log_window.deiconify()
        else:
            self.log_window = tk.Toplevel(self.root)
            self.log_window.title("Logs")
            self.log_window.geometry("500x300")

            text_area = scrolledtext.ScrolledText(self.log_window, state="disabled", wrap=tk.WORD, bg="#1e1e1e", fg="#ffffff")
            text_area.pack(expand=True, fill="both")

            # Redirect logs to the text area
            class TextHandler(logging.Handler):
                def emit(self, record):
                    msg = self.format(record)
                    text_area.configure(state="normal")
                    text_area.insert(tk.END, msg + "\n")
                    text_area.configure(state="disabled")
                    text_area.yview(tk.END)

            handler = TextHandler()
            handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
            logger.addHandler(handler)

# Main Function
if __name__ == "__main__":
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 10), padding=6, relief="flat", background="#444444", foreground="#ffffff")
    style.configure("Accent.TButton", font=("Helvetica", 10), padding=6, relief="flat", background="#5bc0de", foreground="#ffffff")
    
    root = tk.Tk()
    app = UpdaterApp(root)
    root.mainloop()
