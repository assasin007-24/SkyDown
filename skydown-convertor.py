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
import docx
import PyPDF2
import csv
import json
from docx import Document
import subprocess
import ffmpeg

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

        # Handle different file formats
        file_extension = os.path.splitext(input_file)[1].lower()

        if file_extension in [".mp3", ".wav", ".flac", ".m4a", ".ogg", ".opus"]:
            # Audio conversion
            converter = AudioConverter(input_file, output_file, selected_format)
            converter.convert(log_text)
        elif file_extension in [".doc", ".docx"]:
            # Word document conversion to .txt
            converter = WordToTextConverter(input_file, output_file)
            converter.convert(log_text)
        elif file_extension == ".pdf":
            # PDF to .txt conversion
            converter = PDFToTextConverter(input_file, output_file)
            converter.convert(log_text)
        elif file_extension == ".csv":
            # CSV to JSON conversion
            converter = CSVToJSONConverter(input_file, output_file)
            converter.convert(log_text)
        elif file_extension in [".mp4", ".avi", ".mov", ".mkv"]:
            # Video file conversion
            converter = VideoConverter(input_file, output_file, selected_format)
            converter.convert(log_text)
        else:
            log_message(f"Unsupported file format: {file_extension}")
            messagebox.showerror("Error", f"Unsupported file format: {file_extension}")
            return

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

# Word to Text conversion using python-docx
class WordToTextConverter:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def convert(self, log_text):
        try:
            doc = docx.Document(self.input_file)
            text = "\n".join([para.text for para in doc.paragraphs])
            with open(self.output_file, 'w') as file:
                file.write(text)
            log_message(f"Word document converted successfully to {self.output_file}")

        except Exception as e:
            log_message(f"Word conversion failed: {str(e)}")

# PDF to Text conversion using PyPDF2
class PDFToTextConverter:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def convert(self, log_text):
        try:
            pdf_reader = PyPDF2.PdfReader(self.input_file)
            text = ""
            for page in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page].extract_text()

            with open(self.output_file, 'w') as file:
                file.write(text)

            log_message(f"PDF converted successfully to {self.output_file}")

        except Exception as e:
            log_message(f"PDF conversion failed: {str(e)}")

# CSV to JSON conversion
class CSVToJSONConverter:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def convert(self, log_text):
        try:
            with open(self.input_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
                with open(self.output_file, 'w', encoding='utf-8') as jsonfile:
                    json.dump(rows, jsonfile, indent=4)
            log_message(f"CSV converted successfully to {self.output_file}")

        except Exception as e:
            log_message(f"CSV conversion failed: {str(e)}")

# Video file conversion using FFmpeg
class VideoConverter:
    def __init__(self, input_file, output_file, selected_format):
        self.input_file = input_file
        self.output_file = output_file
        self.selected_format = selected_format

    def convert(self, log_text):
        try:
            # Using FFmpeg for video conversion
            log_message(f"Converting video file {self.input_file} to {self.output_file}...")
            ffmpeg.input(self.input_file).output(self.output_file).run()
            log_message(f"Video converted successfully to {self.output_file}")

        except Exception as e:
            log_message(f"Video conversion failed: {str(e)}")

# Initialize Tkinter app
app = tk.Tk()
app.title("SkyDown - File Converter")
app.geometry("600x400")

# Variables
input_file_var = tk.StringVar()
output_folder_var = tk.StringVar()
format_var = tk.StringVar(value="mp3")

# Input File Label and Button
tk.Label(app, text="Input File:").pack(pady=5)
tk.Entry(app, textvariable=input_file_var, width=50).pack(pady=5)
tk.Button(app, text="Browse Input", command=browse_input).pack(pady=5)

# Output Folder Label and Button
tk.Label(app, text="Output Folder:").pack(pady=5)
tk.Entry(app, textvariable=output_folder_var, width=50).pack(pady=5)
tk.Button(app, text="Browse Output", command=browse_output).pack(pady=5)

# Format Selection Dropdown
tk.Label(app, text="Select Format:").pack(pady=5)
tk.OptionMenu(app, format_var, "mp3", "wav", "flac", "ogg", "opus", "mp4", "avi", "mov", "mkv", "txt", "json").pack(pady=5)

# Convert Button
tk.Button(app, text="Convert", command=lambda: convert_file_thread(log_text)).pack(pady=20)

# Show Logs Button
tk.Button(app, text="Show Logs", command=show_logs).pack(pady=5)

# Start Tkinter event loop
app.mainloop()
