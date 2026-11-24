param([int]$Port = 8000)
$ErrorActionPreference = 'Stop'
Push-Location -LiteralPath $PSScriptRoot
try {
    if (-not (Test-Path -LiteralPath 'web/node_modules')) { throw 'Run npm --prefix web ci first. See docs/UI_REACT_TYPESCRIPT.md.' }
    npm --prefix web run build
    if ($LASTEXITCODE -ne 0) { throw 'UI build failed.' }
    Write-Host "Draft Lab: http://127.0.0.1:$Port (Ctrl+C to stop)"
    & '.\.venv\Scripts\python.exe' -m uvicorn src.api.app:app --host 127.0.0.1 --port $Port
} finally { Pop-Location }
