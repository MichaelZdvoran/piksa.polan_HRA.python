$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

python -m PyInstaller `
  --noconfirm `
  --clean `
  --windowed `
  --onefile `
  --name "FireWaterPuzzleAdventure" `
  --icon "assets\icon.ico" `
  --paths "src" `
  "src\main.py"

Write-Host "Hotovo: dist\FireWaterPuzzleAdventure.exe"
