@echo off
cd /d "%~dp0app"

:: Check if Python is installed
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    timeout /t 5 /nobreak
    exit /b 1
)

:: Check if PyInstaller is installed
python -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing now...
    python -m pip install pyinstaller
)

:: Check if matplotlib is installed
python -m pip show matplotlib >nul 2>&1
if %errorlevel% neq 0 (
    echo matplotlib not found. Installing now...
    python -m pip install matplotlib
)

:: Build the executable
echo Building pqr_convert.exe...

python -m PyInstaller --onefile --windowed --name pqr_convert ^
  --hidden-import=sympy ^
  --hidden-import=sympy.printing ^
  --collect-all sympy ^
  --collect-submodules matplotlib ^
  --collect-submodules PIL ^
  main.py

:: Message
if %errorlevel% equ 0 (
    echo.
    echo BUILD SUCCESS - pqr_convert.exe created in dist folder
) else (
    echo.
    echo BUILD FAILED - Check the errors above
)

echo.
echo Closing in 5 seconds...
timeout /t 5 /nobreak
exit /b
