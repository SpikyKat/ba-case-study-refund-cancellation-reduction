# Rebuilds data, analysis, charts and the Word pack. Requires Python 3.11+.
# Usage:  powershell -ExecutionPolicy Bypass -File run_all.ps1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
if (-not (Test-Path .venv)) { python -m venv .venv }
$py = ".\.venv\Scripts\python.exe"
& $py -m pip install --quiet -r requirements.txt
& $py scripts\generate_orders.py
& $py scripts\analyse.py | Out-Null
& $py scripts\build_word_pack.py
Write-Host "Done. See analysis\ and docs\BA_Case_Pack.docx"
