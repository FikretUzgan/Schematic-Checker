# Installation Instructions for Building Executable

## Prerequisites

You need Python 3.8 or higher installed on your system.

---

## Step 1: Verify Python Installation

Open PowerShell or Command Prompt and run:

```powershell
python --version
```

You should see something like: `Python 3.13.7` or similar.

**If Python is not found:**
- Download from: https://www.python.org/downloads/
- During installation, check "Add Python to PATH"

---

## Step 2: Install PyInstaller

### Method 1: Using python -m pip (Recommended)

```powershell
python -m pip install pyinstaller
```

### Method 2: Using pip directly

```powershell
pip install pyinstaller
```

### Method 3: User installation (if you don't have admin rights)

```powershell
python -m pip install --user pyinstaller
```

### Verify Installation

```powershell
python -c "import PyInstaller; print(PyInstaller.__version__)"
```

Should print: `6.16.0` or similar version.

---

## Step 3: Install Pillow (for icon creation)

```powershell
python -m pip install pillow
```

---

## Step 4: Build the Executable

### Option A: Simple Build (Recommended)

```powershell
.\build_simple.bat
```

### Option B: Full Build (with auto-install)

```powershell
.\build_exe.bat
```

### Option C: Manual PyInstaller Command

```powershell
python create_icon.py
pyinstaller AutoAltium_RatingVerifier.spec --clean --noconfirm
move dist\AutoAltium_RatingVerifier.exe .
```

---

## Troubleshooting

### "python is not recognized"

**Problem:** Python not in PATH

**Solution:**
1. Find Python installation folder (usually `C:\Users\YourName\AppData\Local\Programs\Python\Python3XX`)
2. Add to PATH environment variable, OR
3. Reinstall Python and check "Add Python to PATH"

---

### "pip is not recognized"

**Problem:** pip not in PATH or not installed

**Solution:** Use `python -m pip` instead of just `pip`

```powershell
python -m pip install pyinstaller
```

---

### "ModuleNotFoundError: No module named 'PyInstaller'"

**Problem:** PyInstaller not installed

**Solution:**
```powershell
python -m pip install pyinstaller
```

---

### "Permission denied" or "Access denied"

**Problem:** Installing to system directories without admin rights

**Solution:** Install for current user only
```powershell
python -m pip install --user pyinstaller pillow
```

---

### Build fails with "ImportError"

**Problem:** Missing dependencies

**Solution:** Install all dependencies
```powershell
python -m pip install pandas openpyxl pillow pyinstaller
```

---

### Antivirus blocks PyInstaller

**Problem:** Antivirus flags PyInstaller as suspicious

**Solution:**
1. Add PyInstaller to antivirus exceptions
2. Temporarily disable antivirus during build
3. Build on a different machine

---

### "UPX is not available"

**Problem:** UPX compressor not found (this is OK)

**Solution:** Ignore this warning. You can:
- Disable UPX in spec file: `upx=False,`
- Or install UPX from: https://upx.github.io/

---

## Quick Command Reference

```powershell
# Install everything at once
python -m pip install pyinstaller pillow pandas openpyxl

# Check installations
python -c "import PyInstaller; print('PyInstaller OK')"
python -c "import PIL; print('Pillow OK')"
python -c "import pandas; print('Pandas OK')"
python -c "import openpyxl; print('OpenPyXL OK')"

# Build
.\build_simple.bat

# Clean up
.\clean_build.bat
```

---

## If All Else Fails

### Manual Build Process

1. **Create icon:**
   ```powershell
   python create_icon.py
   ```

2. **Run PyInstaller:**
   ```powershell
   python -m PyInstaller AutoAltium_RatingVerifier.spec --clean
   ```

3. **Find executable:**
   ```
   dist\AutoAltium_RatingVerifier.exe
   ```

4. **Copy to project root:**
   ```powershell
   copy dist\AutoAltium_RatingVerifier.exe .
   ```

---

## System Requirements for Building

- **OS:** Windows 10/11
- **Python:** 3.8 or higher
- **RAM:** 2 GB minimum
- **Disk Space:** 500 MB free (for build process)
- **Internet:** Required for downloading dependencies

---

## Success Checklist

- [ ] Python installed and in PATH
- [ ] PyInstaller installed (`python -m pip install pyinstaller`)
- [ ] Pillow installed (`python -m pip install pillow`)
- [ ] Icon created (resources/app_icon.ico exists)
- [ ] Build script runs without errors
- [ ] Executable created (AutoAltium_RatingVerifier.exe)
- [ ] Executable size is 50-80 MB
- [ ] Executable runs when double-clicked

---

**Still having issues?** Check the Python version and make sure all commands use `python -m pip` instead of just `pip`.
