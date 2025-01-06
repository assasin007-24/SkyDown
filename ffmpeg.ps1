$ffmpegUrl = "https://github.com/assasin007-24/SkyDown/releases/download/v1.0/ffmpeg.zip"
$zipFilePath = "$env:TEMP\ffmpeg.zip"
$destinationFolder = "C:\ffmpeg"
if (-not (Test-Path -Path $destinationFolder)) {
    New-Item -Path $destinationFolder -ItemType Directory
}
Write-Host "Downloading FFmpeg..."
Invoke-WebRequest -Uri $ffmpegUrl -OutFile $zipFilePath
Write-Host "Extracting FFmpeg to C:\ffmpeg..."
Expand-Archive -Path $zipFilePath -DestinationPath $destinationFolder
Remove-Item -Path $zipFilePath
Write-Host "FFmpeg installation complete!"
[System.Environment]::SetEnvironmentVariable('Path', $env:Path + ";C:\ffmpeg", [System.EnvironmentVariableTarget]::Machine)
Write-Host "FFmpeg added to the system PATH."

