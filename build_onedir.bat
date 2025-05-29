@echo off
:: Trỏ đến thư mục app
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

@echo off
cd /d %~dp0

python -m PyInstaller ^
    --name pqr_convert ^
    --windowed --onedir ^
    --icon=app/assets/icon.ico ^
    --add-data "app/assets/icon.png;assets" ^
    --hidden-import=sympy ^
    --hidden-import=sympy.printing ^
    --collect-all sympy ^
    --collect-submodules PIL ^
    --exclude-module matplotlib.tests ^
	--exclude-module matplotlib.tests.test_* ^
    --noconfirm --clean --noupx ^
    app/ui_main.py



:: Check error 
if %errorlevel% equ 0 (
    echo.
    echo BUILD SUCCESS - pqr_convert.exe created in dist folder
) else (
    echo.
    echo BUILD FAILED - Check the errors above
)

echo.

timeout /t 5 /nobreak
exit /b
