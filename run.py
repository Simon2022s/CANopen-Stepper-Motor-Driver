#!/usr/bin/env python3
"""
RS485 Stepper Motor Driver - Launcher
Auto-checks and installs dependencies, then launches the program
"""

import sys
import subprocess
import importlib.util
from pathlib import Path

def check_module(module_name):
    """Check if module is installed"""
    spec = importlib.util.find_spec(module_name)
    return spec is not None

def install_package(package):
    """Install specified package"""
    print(f"Installing {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {package} installation failed: {e}")
        return False

def install_requirements():
    """Install all dependencies from requirements.txt"""
    req_file = Path(__file__).parent / "requirements.txt"
    if req_file.exists():
        print("Installing dependencies from requirements.txt...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req_file)])
            print("✅ All dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Dependency installation failed: {e}")
            return False
    return False

def main():
    """Main function"""
    print("=" * 60)
    print("RS485 Stepper Motor Driver - Launcher")
    print("=" * 60)
    print()
    
    # Check core dependencies
    missing_deps = []
    
    print("Checking dependencies...")
    if not check_module("PyQt5"):
        missing_deps.append("PyQt5>=5.15.0")
        print("  ❌ PyQt5 not installed")
    else:
        print("  ✅ PyQt5 installed")
    
    if not check_module("serial"):
        missing_deps.append("pyserial>=3.5")
        print("  ❌ pyserial not installed")
    else:
        print("  ✅ pyserial installed")
    
    print()
    
    # Install missing dependencies
    if missing_deps:
        print(f"Found {len(missing_deps)} missing dependencies, installing...")
        print()
        
        # Try installing from requirements.txt
        if not install_requirements():
            # If requirements.txt fails, install core dependencies individually
            for dep in missing_deps:
                if not install_package(dep):
                    print(f"\n❌ Cannot install {dep}")
                    print("Please manually run: pip install " + dep)
                    input("\nPress Enter to exit...")
                    return 1
        
        print()
        print("✅ All dependencies installed!")
        print()
    else:
        print("✅ All dependencies already installed!")
        print()
    
    # Launch main program
    print("Starting RS485 Stepper Motor Driver...")
    print("=" * 60)
    print()
    
    try:
        import BruceLee
        # If BruceLee.py has main function, call it
        if hasattr(BruceLee, 'main'):
            BruceLee.main()
        else:
            # Otherwise run file directly
            exec(open("BruceLee.py").read())
    except Exception as e:
        print(f"❌ Launch failed: {e}")
        input("\nPress Enter to exit...")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
