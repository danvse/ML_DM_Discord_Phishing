@echo off
echo ===============================================================================
echo   Starting Discord Sentinel - FastAPI Backend Server (Port 8000)
echo ===============================================================================
echo.

cd /d "%~dp0backend"

:: Try py first, then python, then python3
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Starting Uvicorn with 'py'...
    py -m uvicorn src.api:app --host 127.0.0.1 --port 8000 --reload
    goto end
)

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Starting Uvicorn with 'python'...
    python -m uvicorn src.api:app --host 127.0.0.1 --port 8000 --reload
    goto end
)

where python3 >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Starting Uvicorn with 'python3'...
    python3 -m uvicorn src.api:app --host 127.0.0.1 --port 8000 --reload
    goto end
)

echo [ERROR] Python was not found in PATH.
pause
exit /b 1

:end
