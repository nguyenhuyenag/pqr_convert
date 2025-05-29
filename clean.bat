@echo off
echo Cleaning Python build artifacts...

:: Xóa trong thư mục hiện tại
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
del *.spec 2>nul

:: Xóa trong thư mục app (nếu có)
if exist app\build rmdir /s /q app\build
if exist app\dist rmdir /s /q app\dist
if exist app\__pycache__ rmdir /s /q app\__pycache__
del app\*.spec 2>nul

echo Done!

timeout /t 5 /nobreak
exit /b
