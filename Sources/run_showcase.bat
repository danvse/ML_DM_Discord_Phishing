@echo off
echo ===============================================================================
echo   Discord Phishing Sentinel - Master Showcase Pipeline
echo   Author: Edwin Lin (Team #18 - Solo Project)
echo ===============================================================================
echo.

cd /d "%~dp0"

:: Try py first, then python, then python3
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Executing with 'py'...
    py run_showcase_pipeline.py
    goto end
)

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Executing with 'python'...
    python run_showcase_pipeline.py
    goto end
)

where python3 >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Executing with 'python3'...
    python3 run_showcase_pipeline.py
    goto end
)

echo [ERROR] Python was not found in PATH. Please install Python 3.10+ or use the 'py' launcher.
pause
exit /b 1

:end
echo.
echo ===============================================================================
echo   Pipeline Execution Finished.
echo ===============================================================================
pause
