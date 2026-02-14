@echo off
REM Simple build script - assumes PyInstaller is already installed
REM If PyInstaller is not installed, run: python -m pip install pyinstaller

echo ========================================
echo Auto_Altium - Simple Build Script
echo ========================================
echo.

echo Checking Python...
py --version
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

echo.
echo Checking PyInstaller...
py -c "import PyInstaller; print('PyInstaller version:', PyInstaller.__version__)"
if errorlevel 1 (
    echo.
    echo [ERROR] PyInstaller not installed!
    echo.
    echo Please install it manually:
    echo   python -m pip install pyinstaller
    echo.
    echo Or use PowerShell:
    echo   python -m pip install --user pyinstaller
    echo.
    pause
    exit /b 1
)

echo.
echo [1/3] Cleaning previous build...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
echo    ✓ Clean

echo.
echo [2/3] Creating icon...
py create_icon.py
if errorlevel 1 (
    echo [ERROR] Icon creation failed
    pause
    exit /b 1
)
echo    ✓ Icon ready

echo.
echo [3/3] Building executable...
echo    (This will take 2-5 minutes)
echo.
py -m PyInstaller AutoAltium_RatingVerifier.spec --clean --noconfirm

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    echo Check the output above for errors.
    pause
    exit /b 1
)

echo.
if exist "dist\AutoAltium_RatingVerifier.exe" (
    move "dist\AutoAltium_RatingVerifier.exe" "."
    echo ========================================
    echo ✅ BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo Executable: AutoAltium_RatingVerifier.exe
    for %%A in (AutoAltium_RatingVerifier.exe) do echo Size: %%~zA bytes
    echo.
) else (
    echo [ERROR] Executable not found!
    echo The build may have failed silently.
    pause
    exit /b 1
)

pause
