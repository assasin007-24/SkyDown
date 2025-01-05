import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import yt_dlp
import os
import re
import threading
from tkinter import ttk
import sys
import traceback
import webbrowser
import requests
from io import BytesIO
from tkinter import PhotoImage

class TextRedirector:
    def __init__(self, text_widget, tag):
        self.text_widget = text_widget
        self.tag = tag

    def write(self, message):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, message, self.tag)
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.see(tk.END)

    def flush(self):
        pass 


def log_message(message):
    print(message)  


def clear_logs():
    log_text.config(state=tk.NORMAL)
    log_text.delete(1.0, tk.END)
    log_text.config(state=tk.DISABLED)


def download_video(url, format, output_path):
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]+bestvideo[ext=mp4]/best[ext=mp4]' if format == 'mp4' else 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if format == 'mp3' else [],
        'merge_output_format': 'mp4' if format == 'mp4' else None,
        'ffmpeg_location': 'C:/ffmpeg/bin'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.add_progress_hook(progress_hook)
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)  
            video_title = info.get('title', 'Unknown Title')
        messagebox.showinfo(
            title="SkyDown - Completed",
            message=(
                f"Your video '{video_title}' has been successfully downloaded.\n"
                f"Format: {format.upper()}\n"
                f"Location: {output_path}\n"
            )
        )
    except Exception as e:
        log_message(f"Error: {traceback.format_exc()}")


def download_playlist(url, format, output_path):
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]+bestvideo[ext=mp4]/best[ext=mp4]' if format == 'mp4' else 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if format == 'mp3' else [],
        'merge_output_format': 'mp4' if format == 'mp4' else None,
        'ffmpeg_location': 'C:/ffmpeg/bin'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.add_progress_hook(progress_hook)
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', 'Playlist')
        messagebox.showinfo(
            title="SkyDown - Completed",
            message=(
                f"Your playlist '{video_title}' has been successfully downloaded.\n"
                f"Format: {format.upper()}\n"
                f"Location: {output_path}\n"
            )
        )
    except Exception as e:
        log_message(f"Error: {traceback.format_exc()}")


def is_playlist(url):
    return "playlist" in url or re.search(r"list=[\w-]+", url)


def start_download():
    try:
        url = url_entry.get().strip()
        format = format_var.get().lower()
        output_path = output_entry.get().strip()

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        download_thread = threading.Thread(target=download, args=(url, format, output_path))
        download_thread.start()
    except Exception:
        log_message(f"Error: {traceback.format_exc()}")


def download(url, format, output_path):
    if is_playlist(url):
        download_playlist(url, format, output_path)
    else:
        download_video(url, format, output_path)


def progress_hook(d):
    if d['status'] == 'downloading':
        log_message(f"Downloading: {d['_percent_str']} of {d['_total_bytes_str']} at {d['_speed_str']}")
    elif d['status'] == 'finished':
        log_message(f"Finished downloading: {d['filename']}")


def show_logs():
    if hasattr(app, 'log_window') and app.log_window.winfo_exists():
        app.log_window.lift()
        return

    app.log_window = tk.Toplevel(app)
    app.log_window.title("SkyDown - Logs")
    app.log_window.geometry("600x400")
    app.log_window.configure(bg="#121212")

    log_frame = tk.Frame(app.log_window, bg="#121212")
    log_frame.pack(expand=True, fill='both', padx=10, pady=10)

    log_window_text = scrolledtext.ScrolledText(
        log_frame,
        state='disabled',
        bg="#1e1e1e",
        fg="#ffffff",
        wrap=tk.WORD,
        font=("Consolas", 10)
    )
    log_window_text.pack(expand=True, fill='both')

    global log_text
    log_text = log_window_text

    sys.stdout = TextRedirector(log_text, "stdout")
    sys.stderr = TextRedirector(log_text, "stderr")


def browse_output_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, folder_selected)

def on_hover(event, button):
    button.config(bg="#2e86de")


def on_leave(event, button):
    button.config(bg="#0984e3")


def show_version():
    messagebox.showinfo(
        title="SkyDown - Version",
        message="Version 1.0 Stable Fusion \n For updates check our website."
    )


def open_url(url):
    webbrowser.open(url)

def set_external_icon():

    icon_url = "https://skydown.vercel.app/skydown.icon"
    
    response = requests.get(icon_url)
    if response.status_code == 200:

        icon_data = BytesIO(response.content)

        app.iconphoto(True, PhotoImage(data=icon_data.read()))
    else:
        print("Failed to download the icon.")


app = tk.Tk()
app.title("SkyDown - VOX")
app.geometry("800x550")
app.configure(bg="#121212")

set_external_icon()

menubar = tk.Menu(app)

sky_down_menu = tk.Menu(menubar, tearoff=0)
sky_down_menu.add_command(label="Version", command=show_version)
menubar.add_cascade(label="SkyDown", menu=sky_down_menu)

web_menu = tk.Menu(menubar, tearoff=0)
web_menu.add_command(label="SkyDown (Vercel)", command=lambda: open_url("https://skydown.vercel.app"))
web_menu.add_command(label="RythmMV", command=lambda: open_url("https://rythmmv.cloudns.org"))
web_menu.add_command(label="YouTube", command=lambda: open_url("https://www.youtube.com/channel/UCfWtjVJhqhOobHUjORDyX5w"))
web_menu.add_command(label="GitHub", command=lambda: open_url("https://github.com/assasin007-24"))
web_menu.add_command(label="Facebook", command=lambda: open_url("https://www.facebook.com/mihai14launcher"))
web_menu.add_command(label="TikTok", command=lambda: open_url("https://www.tiktok.com/@mihai14launcher"))
web_menu.add_command(label="Discord", command=lambda: open_url("https://discord.gg/EY7v56BeFc"))
menubar.add_cascade(label="Web", menu=web_menu)

app.config(menu=menubar)
style = {
    "bg": "#121212",
    "fg": "#ffffff",
    "font": ("Arial", 12),
    "highlightbackground": "#1e1e1e",
    "highlightcolor": "#1e1e1e",
}

container = tk.Frame(app, bg="#121212")
container.pack(padx=20, pady=20, fill="both", expand=True)

url_frame = tk.Frame(container, bg="#121212")
url_frame.pack(anchor="w", pady=10, fill="x")
tk.Label(url_frame, text="Enter Video or Playlist URL:", **style).pack(anchor="w")
url_entry = tk.Entry(url_frame, width=60, **style)
url_entry.pack(anchor="w", pady=5)

path_frame = tk.Frame(container, bg="#121212")
path_frame.pack(anchor="w", pady=10, fill="x")
tk.Label(path_frame, text="Output Folder Path:", **style).pack(anchor="w")
output_entry = tk.Entry(path_frame, width=60, **style)
output_entry.pack(side="left", pady=5, padx=(0, 5))
browse_button = tk.Button(path_frame, text="Browse", command=browse_output_path, bg="#0984e3", fg="white", font=("Arial", 10), width=10)
browse_button.pack(side="left")
browse_button.bind("<Enter>", lambda e: on_hover(e, browse_button))
browse_button.bind("<Leave>", lambda e: on_leave(e, browse_button))

format_frame = tk.Frame(container, bg="#121212")
format_frame.pack(anchor="w", pady=10)
tk.Label(format_frame, text="Select Format:", **style).pack(anchor="w")
format_var = tk.StringVar(value="mp4")
tk.Radiobutton(format_frame, text="MP4", variable=format_var, value="mp4", **style, selectcolor="#1e1e1e").pack(anchor="w")
tk.Radiobutton(format_frame, text="MP3", variable=format_var, value="mp3", **style, selectcolor="#1e1e1e").pack(anchor="w")

button_frame = tk.Frame(container, bg="#121212")
button_frame.pack(anchor="center", pady=20)
start_button = tk.Button(button_frame, text="Start Download", command=start_download, bg="#27ae60", fg="white", font=("Arial", 12), width=15)
start_button.pack(side="left", padx=10)
start_button.bind("<Enter>", lambda e: on_hover(e, start_button))
start_button.bind("<Leave>", lambda e: on_leave(e, start_button))

logs_button = tk.Button(button_frame, text="Show Logs", command=show_logs, bg="#0984e3", fg="white", font=("Arial", 12), width=15)
logs_button.pack(side="left", padx=10)
logs_button.bind("<Enter>", lambda e: on_hover(e, logs_button))
logs_button.bind("<Leave>", lambda e: on_leave(e, logs_button))

clear_button = tk.Button(button_frame, text="Clear Logs", command=clear_logs, bg="#e74c3c", fg="white", font=("Arial", 12), width=15)
clear_button.pack(side="left", padx=10)
clear_button.bind("<Enter>", lambda e: on_hover(e, clear_button))
clear_button.bind("<Leave>", lambda e: on_leave(e, clear_button))

app.mainloop()
