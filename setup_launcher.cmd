@echo off
setlocal
cd /d "%~dp0"
for %%I in ("%~dp0.") do set "PROJECT_ROOT=%%~fI"

echo.
echo LinguaMCP MCP Launcher Setup
echo ============================
echo.

set "PYTHON_CMD="
where py >nul 2>nul
if not errorlevel 1 set "PYTHON_CMD=py -3"

if not defined PYTHON_CMD (
    where python >nul 2>nul
    if not errorlevel 1 set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
    echo Python 3.10 or newer was not found.
    echo Install Python from https://www.python.org/downloads/ and run this file again.
    pause
    exit /b 1
)

%PYTHON_CMD% -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"
if errorlevel 1 (
    echo Python 3.10 or newer is required.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating the local Python environment...
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 goto :failed
)

echo Installing LinguaMCP dependencies...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :failed

where dotnet >nul 2>nul
if errorlevel 1 (
    echo .NET 9 SDK was not found. Install it from https://dotnet.microsoft.com/download
    goto :failed
)

echo Building the desktop launcher...
dotnet publish "launcher\LinguaMCP.Launcher.csproj" -c Release -o "launcher\publish" --nologo
if errorlevel 1 goto :failed

echo Creating the desktop shortcut...
cscript //nologo "scripts\create_launcher_shortcut.vbs" "%PROJECT_ROOT%"
if errorlevel 1 goto :failed

echo.
echo Setup complete.
echo Use the "LinguaMCP MCP" shortcut on your desktop to start and stop the server.
echo.
pause
exit /b 0

:failed
echo.
echo Setup did not complete. Review the error above and try again.
echo.
pause
exit /b 1
