@echo off
echo Installing SkyDown Dependencies...

set FFmpeg_ZIP=https://skydown.vercel.app/ffmpeg.zip
set Installer_MSI=https://skydown.vercel.app/skydown-installer.msi

set FFmpeg_ZIP_PATH=%TEMP%\ffmpeg.zip
set MSI_PATH=%TEMP%\skydown-installer.msi

echo Downloading FFmpeg...
powershell -Command "Invoke-WebRequest -Uri %FFmpeg_ZIP% -OutFile %FFmpeg_ZIP_PATH%"

echo Extracting FFmpeg to C:\ffmpeg...
powershell -Command "Expand-Archive -Path %FFmpeg_ZIP_PATH% -DestinationPath C:\ffmpeg"

echo Downloading SkyDown Installer...
powershell -Command "Invoke-WebRequest -Uri %Installer_MSI% -OutFile %MSI_PATH%"

echo Running SkyDown Installer...
start /wait msiexec /i %MSI_PATH%

echo Cleaning up...
del %FFmpeg_ZIP_PATH%
del %MSI_PATH%

echo Installation complete!
pause
