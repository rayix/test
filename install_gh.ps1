# Download and install GitHub CLI
$ghZip = "$env:TEMP\gh.zip"
$ghDir = "$env:TEMP\gh"

Write-Host "Downloading GitHub CLI..."
Invoke-WebRequest -Uri "https://github.com/cli/cli/releases/download/v2.63.0/gh_2.63.0_windows_amd64.zip" -OutFile $ghZip

Write-Host "Extracting..."
Expand-Archive -Path $ghZip -DestinationPath $ghDir -Force

Write-Host "Testing gh..."
& "$ghDir\bin\gh.exe" --version
