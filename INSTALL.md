# Quick Installation Guide

## 🚀 Easiest Installation Method

### Windows Users

1. **Clone the project**
   ```bash
   git clone https://github.com/Simon2022s/RS485-Stepper-Motor-Driver.git
   cd RS485-Stepper-Motor-Driver
   ```

2. **Double-click** `start.bat`
   
   Or run from command line:
   ```bash
   python run.py
   ```

3. **Wait for auto-installation of dependencies**, the program will launch automatically

### macOS/Linux Users

1. **Clone the project**
   ```bash
   git clone https://github.com/Simon2022s/RS485-Stepper-Motor-Driver.git
   cd RS485-Stepper-Motor-Driver
   ```

2. **Run the launcher**
   ```bash
   python3 run.py
   ```

## 📋 Manual Installation Method

If automatic installation fails, you can install manually:

### 1. Install Python

Make sure Python 3.8 or higher is installed:
```bash
python --version
```

If not installed, download from: https://www.python.org/downloads/

### 2. Install Dependencies

**Method A: Install all dependencies using pip**
```bash
pip install -r requirements.txt
```

**Method B: Install only core dependencies (faster)**
```bash
pip install PyQt5 pyserial
```

### 3. Run the Program

```bash
python BruceLee.py
```

## 🔧 Common Issues

### Q1: "pip is not recognized as an internal or external command"

**Solution**: Python was not added to PATH during installation

1. Reinstall Python and check "Add Python to PATH"
2. Or use Python's built-in pip:
   ```bash
   python -m pip install PyQt5 pyserial
   ```

### Q2: PyQt5 installation fails

**Solution**: Use a mirror source
```bash
pip install PyQt5 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: Missing other modules

**Solution**: Install all dependencies
```bash
pip install -r requirements.txt
```

### Q4: Program crashes after startup

**Solution**:
1. Check if all dependencies are installed
2. Check if a serial port device is connected
3. Check error logs in the `log/` directory

## 📝 Dependency Description

| Dependency | Version | Purpose |
|------------|---------|---------|
| PyQt5 | >=5.15.0 | GUI interface |
| pyserial | >=3.5 | Serial communication |

## 🎯 Verify Installation

Run the following commands to verify installation:

```bash
python -c "import PyQt5; print('PyQt5:', PyQt5.QtCore.PYQT_VERSION_STR)"
python -c "import serial; print('pyserial:', serial.VERSION)"
```

If version numbers are displayed, installation is successful!

## 🆘 Get Help

If you encounter installation issues:

1. Check [README.md](README.md) for detailed documentation
2. Check [CODE_REVIEW.md](CODE_REVIEW.md) for code explanation
3. Submit an [Issue](https://github.com/Simon2022s/RS485-Stepper-Motor-Driver/issues) on GitHub

## ✅ Installation Checklist

- [ ] Python 3.8+ installed
- [ ] Project cloned locally
- [ ] PyQt5 installed
- [ ] pyserial installed
- [ ] Can run `python BruceLee.py`
- [ ] Program interface displays normally

---

**Tip**: First run may take a few minutes to install dependencies, please be patient.
