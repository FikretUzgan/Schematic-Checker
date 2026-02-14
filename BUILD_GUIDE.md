# Building Executable Guide

## Quick Start

### Simple Build (Recommended)
```batch
build_exe.bat
```
This will:
1. Clean previous builds
2. Create application icon
3. Build standalone .exe
4. Place executable in project root

**Output:** `AutoAltium_RatingVerifier.exe` (~50-80 MB)

---

## What You Get

### Single Executable File
- **Name:** `AutoAltium_RatingVerifier.exe`
- **Type:** Standalone Windows executable
- **Requirements:** None (includes Python + all dependencies)
- **Icon:** PCB-themed with checkmark
- **Console:** Hidden (GUI-only application)

### Distribution
The `.exe` file can be:
- ✅ Copied to any Windows machine
- ✅ Run without Python installation
- ✅ Placed anywhere (Desktop, Program Files, USB drive, etc.)
- ✅ Shared with colleagues

---

## Manual Build (Advanced)

### If you want to customize the build:

1. **Edit the spec file:**
   ```
   AutoAltium_RatingVerifier.spec
   ```

2. **Build with PyInstaller:**
   ```batch
   pyinstaller AutoAltium_RatingVerifier.spec --clean
   ```

3. **Find executable:**
   ```
   dist\AutoAltium_RatingVerifier.exe
   ```

---

## Build Configuration

### Spec File Settings

| Setting | Current Value | Purpose |
|---------|---------------|---------|
| `console` | `False` | No console window (GUI only) |
| `onefile` | `True` | Single .exe file (not folder) |
| `icon` | `resources/app_icon.ico` | Application icon |
| `name` | `AutoAltium_RatingVerifier` | Executable name |
| `upx` | `True` | Compress executable |

### Included Files
The executable bundles:
- ✅ All Python source code
- ✅ `data/component_database.json`
- ✅ Application icon
- ✅ Pandas, openpyxl, tkinter libraries

---

## Customization Options

### Change Application Name
Edit in `AutoAltium_RatingVerifier.spec`:
```python
name='YourCustomName',
```

### Add Console Window (for debugging)
Edit in `AutoAltium_RatingVerifier.spec`:
```python
console=True,  # Shows console output
```

### Create Folder-Based Distribution
Uncomment in `AutoAltium_RatingVerifier.spec`:
```python
# Uncomment the COLLECT section at bottom
```
This creates a folder with multiple files instead of single .exe.

### Change Icon
Replace `resources/app_icon.ico` with your own icon, or:
```batch
python create_icon.py  # Regenerate with changes
```

---

## Troubleshooting

### Build Fails

**Problem:** PyInstaller not found  
**Solution:**
```batch
pip install pyinstaller
```

**Problem:** Missing dependencies during build  
**Solution:** Add to `hiddenimports` in spec file:
```python
hiddenimports = [
    'your_missing_module',
]
```

**Problem:** Executable crashes on startup  
**Solution:** Build with console window to see errors:
```python
console=True,  # in spec file
```

### Executable Too Large

Current size: ~50-80 MB (normal for bundled Python app)

**To reduce size:**
1. Disable UPX compression might paradoxically help:
   ```python
   upx=False,
   ```

2. Exclude unused libraries:
   ```python
   excludes=['matplotlib', 'scipy', 'numpy'],
   ```

### Antivirus False Positives

Some antivirus software may flag PyInstaller executables.

**Solutions:**
1. Add exception in antivirus software
2. Sign the executable (requires code signing certificate)
3. Build on same machine that will run it

---

## File Structure After Build

```
Auto_Altium/
├── AutoAltium_RatingVerifier.exe    ← Standalone executable
├── build/                            (temporary - can delete)
├── dist/                             (temporary - can delete)
├── resources/
│   ├── app_icon.ico                 ← Application icon
│   └── app_icon.png
├── build_exe.bat                     ← Build script
├── clean_build.bat                   ← Cleanup script
├── create_icon.py                    ← Icon generator
└── AutoAltium_RatingVerifier.spec   ← PyInstaller config
```

---

## Testing the Executable

### Before Distribution

1. **Test on build machine:**
   ```batch
   AutoAltium_RatingVerifier.exe
   ```

2. **Test on clean machine:**
   - Copy .exe to different PC
   - Ensure no Python installed
   - Run and verify all features work

3. **Test with real netlist:**
   - Select netlist file
   - Confirm voltage detection
   - Verify Excel/HTML output

### Known Issues

- First startup may be slow (5-10 seconds) - this is normal
- Windows Defender may scan on first run
- Some antivirus software may prompt for permission

---

## Distribution Checklist

Before sharing the executable:

- [ ] Tested on build machine
- [ ] Tested on clean machine (no Python)
- [ ] Verified all reports generate correctly
- [ ] Checked file size is reasonable (< 100 MB)
- [ ] Icon displays correctly
- [ ] No console window appears (GUI only)
- [ ] Error messages are user-friendly

---

## Versioning

To embed version information:

1. Create `version_info.txt`:
   ```
   VSVersionInfo(
     ffi=FixedFileInfo(
       filevers=(1, 0, 0, 0),
       prodvers=(1, 0, 0, 0),
       ...
     )
   )
   ```

2. Update spec file:
   ```python
   version_file='version_info.txt',
   ```

**For V1.0:** Not implemented yet (planned for V2.0)

---

## Clean Up

### Remove Build Artifacts
```batch
clean_build.bat
```

This removes:
- `build/` folder
- `dist/` folder  
- `__pycache__/` folders
- `.spec` files

### Keep For Next Build
- `create_icon.py`
- `build_exe.bat`
- `resources/app_icon.ico`
- `AutoAltium_RatingVerifier.spec`

---

## Future Enhancements

### Planned for V2.0
- Embedded version information
- Digital signature (code signing)
- Auto-update checker
- Installer package (.msi or .exe installer)
- Portable version (no install required)

---

## Support

If you encounter issues:
1. Check this guide
2. Review `build_exe.bat` output for errors
3. Try building with `console=True` to see error messages
4. Verify all dependencies are installed

---

**Last Updated:** February 14, 2026 (V1.0)
