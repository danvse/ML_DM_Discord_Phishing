@echo off
echo ===============================================================================
echo   Starting Discord Sentinel - Angular 18 Frontend Portal (Port 4200)
echo ===============================================================================
echo.

cd /d "%~dp0frontend"

if not exist "node_modules\" (
    echo [INFO] First-time setup: Installing frontend dependencies via npm...
    call npm install
)

echo [INFO] Launching Angular 18 dev server at http://localhost:4200/ ...
call npx ng serve --host 127.0.0.1 --port 4200
