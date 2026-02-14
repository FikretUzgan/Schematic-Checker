@echo off
REM Build script for Auto_Altium Rating Verification Tool
REM Creates standalone executable for Windows

echo ========================================
echo Auto_Altium Rating Verifier - Build
echo ========================================
echo.

REM Check if PyInstaller is installed
py -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [ERROR] PyInstaller not found!
    echo Installing PyInstaller...
    py -m pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] Failed to install PyInstaller
        echo Please run: py -m pip install pyinstaller
        pause
        exit /b 1
    )
)

echo [Step 1/4] Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "AutoAltium_RatingVerifier.exe" del /q AutoAltium_RatingVerifier.exe
echo    ✓ Clean complete

echo.
echo [Step 2/4] Creating application icon...
py create_icon.py
if errorlevel 1 (
    echo [ERROR] Failed to create icon
    exit /b 1
)
echo    ✓ Icon created

echo.
echo [Step 3/4] Building executable with PyInstaller...
echo    This may take several minutes...
py -m PyInstaller AutoAltium_RatingVerifier.spec --clean --noconfirm
if errorlevel 1 (
    echo [ERROR] Build failed!
    exit /b 1
)
echo    ✓ Build complete

echo.
echo [Step 4/4] Moving executable to project root...
if exist "dist\AutoAltium_RatingVerifier.exe" (
    move "dist\AutoAltium_RatingVerifier.exe" "AutoAltium_RatingVerifier.exe"
    echo    ✓ Executable ready
) else (
    echo [ERROR] Executable not found in dist folder
    exit /b 1
)

echo.
echo ========================================
echo ✅ BUILD SUCCESSFUL!
echo ========================================
echo.
echo Executable created: AutoAltium_RatingVerifier.exe
echo Size: 
for %%A in (AutoAltium_RatingVerifier.exe) do echo    %%~zA bytes
echo.
echo You can now distribute this single .exe file.
echo No Python installation required on target machines.
echo.
echo To clean up build artifacts, run: clean_build.bat
echo.
pause
