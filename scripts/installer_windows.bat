@echo off
echo Password Strength Analyzer
echo 'Wordlist' is not recognized as an internal or external command,
echo operable program or batch file.
echo  Windows Installer
echo ===================================================
echo.

cd /d "%~dp0\.."
echo Current directory: %CD%

echo Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo Failed to create virtual environment.
    pause
    exit /b 1
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

echo Installing required packages...
pip install --upgrade pip setuptools
pip install -e .
if errorlevel 1 (
    echo Failed to install packages.
    pause
    exit /b 1
)

echo Installation completed successfully!
echo You can now run: python -m pass_tool.gui
pause

