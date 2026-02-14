@echo off
REM Clean build artifacts for Auto_Altium Rating Verification Tool

echo Cleaning build artifacts...

if exist "build" (
    rmdir /s /q build
    echo    ✓ Removed build folder
)

if exist "dist" (
    rmdir /s /q dist
    echo    ✓ Removed dist folder
)

if exist "__pycache__" (
    rmdir /s /q __pycache__
    echo    ✓ Removed __pycache__
)

for /r %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
echo    ✓ Removed all __pycache__ folders

if exist "*.spec" (
    del /q *.spec
    echo    ✓ Removed spec files
)

echo.
echo ✅ Cleanup complete!
pause
