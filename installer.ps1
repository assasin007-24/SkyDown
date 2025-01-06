# Check if wget is installed
$wgetCheck = Get-Command wget -ErrorAction SilentlyContinue
if ($null -eq $wgetCheck) {
    Write-Host "wget is not installed. Installing wget..."

    # Define wget download URL and extraction paths
    $wgetZipUrl = "https://eternallybored.org/misc/wget/releases/wget-1.21.3-win64.zip"
    $wgetZipPath = "$env:TEMP\wget.zip"
    $wgetExtractPath = "$env:TEMP\wget"
    $wgetExePath = "$wgetExtractPath\wget.exe"

    # Download wget
    Invoke-WebRequest -Uri $wgetZipUrl -OutFile $wgetZipPath
    if ($?) {
        Write-Host "wget downloaded successfully."
    } else {
        Write-Host "Error: Failed to download wget."
        exit 1
    }

    # Extract wget
    Expand-Archive -Path $wgetZipPath -DestinationPath $wgetExtractPath
    if ($?) {
        Write-Host "wget extracted successfully."
    } else {
        Write-Host "Error: Failed to extract wget."
        exit 1
    }

    # Move wget.exe to System32 to make it globally accessible
    Move-Item -Force $wgetExePath "$env:SystemRoot\System32"
    if ($?) {
        Write-Host "wget installed successfully."
    } else {
        Write-Host "Error: Failed to move wget to System32."
        exit 1
    }

    # Clean up wget files
    Remove-Item -Force $wgetZipPath
    Remove-Item -Recurse -Force $wgetExtractPath
} else {
    Write-Host "wget is already installed."
}

# Define URLs for FFmpeg and SkyDown installer
$ffmpegZipUrl = "https://github.com/assasin007-24/SkyDown/releases/download/v1.0/ffmpeg.zip"
$installerExeUrl = "https://skydown.vercel.app/skydown-installer.exe"

# Set file paths for FFmpeg and installer
$ffmpegZipPath = "$env:TEMP\ffmpeg.zip"
$installerExePath = "$env:TEMP\skydown-installer.exe"

# Download FFmpeg using wget
Write-Host "Downloading FFmpeg..."
wget -O $ffmpegZipPath $ffmpegZipUrl
if ($?) {
    Write-Host "FFmpeg downloaded successfully."
} else {
    Write-Host "Error: Failed to download FFmpeg."
    exit 1
}

# Extract FFmpeg to C:\ffmpeg
Write-Host "Extracting FFmpeg to C:\ffmpeg..."
Expand-Archive -Path $ffmpegZipPath -DestinationPath "C:\ffmpeg"
if ($?) {
    Write-Host "FFmpeg extracted successfully."
} else {
    Write-Host "Error: Failed to extract FFmpeg."
    exit 1
}

# Download SkyDown installer using wget
Write-Host "Downloading SkyDown Installer..."
wget -O $installerExePath $installerExeUrl
if ($?) {
    Write-Host "SkyDown Installer downloaded successfully."
} else {
    Write-Host "Error: Failed to download SkyDown Installer."
    exit 1
}

# Run the SkyDown installer
Write-Host "Running SkyDown Installer..."
Start-Process $installerExePath -Wait

# Clean up
Write-Host "Cleaning up..."
Remove-Item -Force $ffmpegZipPath
Remove-Item -Force $installerExePath

Write-Host "Installation complete!"
