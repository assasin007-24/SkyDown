# SkyDown - Video/Audio Downloader

SkyDown is a lightweight downloader that supports video and audio downloads in MP4 and MP3 formats. It can download from popular platforms like DailyMotion, Facebook, TikTok, and YouTube. The app is designed with ease of use in mind and provides a simple user interface for downloading media files directly to your computer.

## Features

- **Download Videos & Audio**: Supports MP4 and MP3 formats.
- **Supported Platforms**:
  - DailyMotion
  - Facebook
  - TikTok
  - YouTube
- **Easy-to-Use Interface**: Built with `tkinter` for a simple, intuitive experience.
- **Automatic Setup**: 
  - The installer automatically installs both SkyDown and FFmpeg on your system.
  - FFmpeg is automatically extracted and set up in `C:\ffmpeg` via a `.bat` or `.ps1` script.
  - A shortcut is created in the Start Menu for easy access to SkyDown.
- **No Data Collection**: We respect your privacy. SkyDown does not track users or collect any data about them.

## Libraries Used

SkyDown is built using Python and the following libraries:

- `tkinter`: For the graphical user interface (GUI).
- `yt_dlp`: For downloading videos and audio from supported platforms.
- `os`: For file system interactions.
- `re`: For regular expressions.
- `threading`: To handle downloading tasks concurrently.
- `sys`: For system-related operations.
- `traceback`: For error handling and logging.
- `webbrowser`: For opening links in the web browser.
- `requests`: For downloading files.
- `BytesIO`: To handle in-memory file operations.
- `PhotoImage`: For handling image files in the GUI.

## How to Convert to Executable

SkyDown is converted into an executable file using **auto-py-to-exe** for easy sharing. The executable can be run on Windows systems without requiring Python to be installed.

## Installation

To install SkyDown on your system, follow these steps:

1. Download the installer from the official site:
   - Website: [skydown.vercel.app](https://skydown.vercel.app)
   - Download the `.exe` installer.

2. Run the `.exe` installer file:
   - The installer will automatically install SkyDown on your system.
   - It will also extract FFmpeg from the `.zip` file and install it in the directory `C:\ffmpeg`.
   - The installer will create a shortcut for SkyDown in the Start Menu for easy access.

3. After installation, FFmpeg will be set up automatically, and you can start using SkyDown right away.

4. You can easily access SkyDown from the Start Menu or by searching for "SkyDown" on your Windows system.

## Website and Contact

- Website: [skydown.vercel.app](https://skydown.vercel.app)
- RythmMV: [rythmmv.cloudns.org](https://rythmmv.cloudns.org)
- Discord: [Join our Discord](https://discord.gg/EY7v56BeFc)

## Privacy Policy

- **We do not track users**: SkyDown does not collect or track any data about users.
- **No data storage**: The application does not save or store any data or media files downloaded by users.
- **Privacy First**: Your privacy is important to us, and we respect that by ensuring no personal information is ever collected.

## Contributing

You are welcome to fork the repository, suggest improvements, or fix bugs. However, **you may not redistribute or claim the software as your own**. Contributions are welcomed through pull requests.

## License

SkyDown is licensed under the MIT License. For more details, refer to the `LICENSE` file in the repository.

## Acknowledgments

- SkyDown uses `yt-dlp`, a powerful tool for downloading videos from various platforms.
- Thanks to the Python and tkinter communities for creating the foundation for SkyDown.

We hope you enjoy using SkyDown for your video and audio downloading needs! If you encounter any issues or have suggestions, feel free to contact us on our Discord channel.

Happy downloading!
