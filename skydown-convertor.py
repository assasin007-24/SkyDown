import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
import sys
import requests
from tkinter import scrolledtext
from io import BytesIO
from tkinter import PhotoImage
from pydub import AudioSegment
from pydub.exceptions import PydubException

# Redirecting stdout and stderr to capture them in the log window
class TextRedirector:
    def __init__(self, widget, stream):
        self.widget = widget
        self.stream = stream

    def write(self, message):
        self.widget.config(state=tk.NORMAL)
        self.widget.insert(tk.END, message)
        self.widget.config(state=tk.DISABLED)
        self.widget.yview(tk.END)

    def flush(self):
        pass

# Function to browse for input file
def browse_input():
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    if file_path:
        input_file_var.set(file_path)

# Function to browse for output folder
def browse_output():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_folder_var.set(folder_path)

# Function to show logs
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

# Function to display logs in the console-like window
def log_message(message):
    print(message)

# Function to show the notification
def show_conversion_notification(input_file, output_file, output_folder):
    file_name = os.path.splitext(os.path.basename(input_file))[0]
    output_name = os.path.splitext(os.path.basename(output_file))[0]
    messagebox.showinfo(
        "SkyDown - Converter",
        f"Your file {file_name}{os.path.splitext(input_file)[1]} was converted to {output_name}{os.path.splitext(output_file)[1]}\n"
        f"at {output_folder}"
    )

# Function to perform the conversion and log output in a thread
def convert_file_thread(log_text=None):
    # Run the conversion process in a separate thread
    thread = threading.Thread(target=convert_file, args=(log_text,))
    thread.start()

# Function to perform the conversion and log output (this runs in a separate thread)
def convert_file(log_text):
    input_file = input_file_var.get()
    output_folder = output_folder_var.get()
    selected_format = format_var.get()

    if not input_file or not output_folder or not selected_format:
        messagebox.showerror("Error", "Please select both input file, output folder, and a format.")
        return

    try:
        # Get the input file name without extension
        file_name = os.path.splitext(os.path.basename(input_file))[0]

        # Generate the output file path
        output_file = os.path.join(output_folder, f"{file_name}.{selected_format}")

        # Start the conversion and log the output
        log_message(f"Starting conversion: {input_file} -> {output_file}...")

        # Start the conversion process
        converter = AudioConverter(input_file, output_file, selected_format)
        converter.convert(log_text)

        # Show conversion notification
        show_conversion_notification(input_file, output_file, output_folder)

        # Success message and logs
        messagebox.showinfo("Success", f"File converted successfully!\nSaved as: {output_file}")
        log_message(f"Conversion completed successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        log_message(f"Error: {str(e)}")

# Audio conversion with PyDub (when the selected format is audio)
class AudioConverter:
    def __init__(self, input_file, output_file, selected_format):
        self.input_file = input_file
        self.output_file = output_file
        self.selected_format = selected_format

    def convert(self, log_text):
        try:
            # Check if the input file is a video file by looking at its extension
            video_formats = ["mp4", "mov", "mkv", "avi", "flv", "webm"]
            input_extension = os.path.splitext(self.input_file)[1].lower()

            # If the file is a video, extract the audio
            if any(input_extension.endswith(fmt) for fmt in video_formats):
                log_message(f"Extracting audio from video file {self.input_file}...")
                audio = AudioSegment.from_file(self.input_file, format=input_extension.strip('.'))
            else:
                # If it's not a video, just treat it as an audio file
                log_message(f"Converting audio file {self.input_file}...")
                audio = AudioSegment.from_file(self.input_file)

            # Export the audio in the selected format
            audio.export(self.output_file, format=self.selected_format)
            log_message(f"Audio converted successfully to {self.output_file}")

        except PydubException as e:
            log_message(f"Audio conversion failed: {str(e)}")

def set_external_icon():

    icon_url = "https://skydown.vercel.app/skydown.png"
    
    response = requests.get(icon_url)
    if response.status_code == 200:

        icon_data = BytesIO(response.content)

        app.iconphoto(True, PhotoImage(data=icon_data.read()))
    else:
        print("Failed to download the icon.")

# Create the main window
app = tk.Tk()
app.title("SkyDown - File Converter")

# Set dark mode colors
app.configure(bg="#121212")
app.resizable(False, False)  # Make the window non-resizable
set_external_icon()
# Input file path
input_file_var = tk.StringVar()
input_label = tk.Label(app, text="Input File:", fg="#ffffff", bg="#121212", font=("Arial", 12))
input_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
input_entry = tk.Entry(app, textvariable=input_file_var, width=50, bg="#2e2e2e", fg="#ffffff", font=("Arial", 12))
input_entry.grid(row=0, column=1, padx=10, pady=10)
input_button = tk.Button(app, text="Browse", command=browse_input, bg="#007bff", fg="#ffffff", font=("Arial", 12))
input_button.grid(row=0, column=2, padx=10, pady=10)

# Output folder path
output_folder_var = tk.StringVar()
output_label = tk.Label(app, text="Output Folder:", fg="#ffffff", bg="#121212", font=("Arial", 12))
output_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
output_entry = tk.Entry(app, textvariable=output_folder_var, width=50, bg="#2e2e2e", fg="#ffffff", font=("Arial", 12))
output_entry.grid(row=1, column=1, padx=10, pady=10)
output_button = tk.Button(app, text="Browse", command=browse_output, bg="#007bff", fg="#ffffff", font=("Arial", 12))
output_button.grid(row=1, column=2, padx=10, pady=10)

# Format selection dropdown
format_label = tk.Label(app, text="Select Format:", fg="#ffffff", bg="#121212", font=("Arial", 12))
format_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
format_options = ["mp3", "ogg", "wav", "flac"]
format_var = tk.StringVar()
format_var.set(format_options[0])  # Default to mp3
format_menu = tk.OptionMenu(app, format_var, *format_options)
format_menu.config(bg="#2e2e2e", fg="#ffffff", font=("Arial", 12))
format_menu.grid(row=2, column=1, padx=10, pady=10)

# Convert button
convert_button = tk.Button(app, text="Convert", command=lambda: convert_file_thread(), bg="#28a745", fg="#ffffff", font=("Arial", 12))
convert_button.grid(row=3, column=0, columnspan=3, padx=10, pady=20)

# Show logs button
logs_button = tk.Button(app, text="Show Logs", command=show_logs, bg="#007bff", fg="#ffffff", font=("Arial", 12))
logs_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Run the Tkinter event loop
app.mainloop()
