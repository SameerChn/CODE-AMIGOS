import os
import sys
import subprocess
import tempfile
import shutil
import urllib.request
import zipfile
import ctypes
import winreg

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def download_file(url, dest_path):
    print(f"Downloading {url} to {dest_path}...")
    try:
        urllib.request.urlretrieve(url, dest_path)
        return True
    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        return False

def install_tesseract():
    # Check if Tesseract is already installed
    try:
        from shutil import which
        tesseract_path = which('tesseract')
        if tesseract_path:
            print(f"Tesseract is already installed at: {tesseract_path}")
            return True
    except Exception:
        pass
    
    # Common installation paths
    common_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        r'C:\Tesseract-OCR\tesseract.exe'
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            print(f"Tesseract is already installed at: {path}")
            # Add to PATH if not already there
            add_to_path(os.path.dirname(path))
            return True
    
    print("Tesseract OCR is not installed. Starting installation...")
    
    # Create temp directory
    temp_dir = tempfile.mkdtemp()
    installer_path = os.path.join(temp_dir, "tesseract-installer.exe")
    
    # Download Tesseract installer
    tesseract_url = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe"
    if not download_file(tesseract_url, installer_path):
        print("Failed to download Tesseract installer.")
        return False
    
    # Run installer
    print("Running Tesseract installer...")
    print("Please follow the installation wizard and select the default options.")
    print("Make sure to check 'Add to PATH' during installation.")
    
    try:
        # Run installer with admin privileges if possible
        if is_admin():
            subprocess.run([installer_path], check=True)
        else:
            # Try to elevate privileges
            ctypes.windll.shell32.ShellExecuteW(None, "runas", installer_path, None, None, 1)
            input("Press Enter after completing the Tesseract installation...")
    except Exception as e:
        print(f"Error running installer: {str(e)}")
        print("\nManual installation instructions:")
        print("1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Run the installer and follow the instructions")
        print("3. Make sure to check 'Add to PATH' during installation")
        return False
    
    # Clean up
    try:
        shutil.rmtree(temp_dir)
    except:
        pass
    
    # Verify installation
    for path in common_paths:
        if os.path.exists(path):
            print(f"Tesseract successfully installed at: {path}")
            # Add to PATH if not already there
            add_to_path(os.path.dirname(path))
            return True
    
    print("Tesseract installation may have failed or was installed to a non-standard location.")
    print("Please restart your computer and try running the application again.")
    return False

def add_to_path(directory):
    if not os.path.exists(directory):
        print(f"Directory does not exist: {directory}")
        return False
    
    try:
        # Get the current PATH
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment', 0, winreg.KEY_READ | winreg.KEY_WRITE)
        path, _ = winreg.QueryValueEx(key, 'PATH')
        
        # Check if directory is already in PATH
        if directory.lower() in [p.lower() for p in path.split(';') if p]:
            print(f"{directory} is already in PATH")
            return True
        
        # Add directory to PATH
        new_path = path + ';' + directory
        winreg.SetValueEx(key, 'PATH', 0, winreg.REG_EXPAND_SZ, new_path)
        winreg.CloseKey(key)
        print(f"Added {directory} to PATH")
        
        # Notify the system about the change
        subprocess.run(['setx', 'PATH', new_path], check=True, capture_output=True)
        return True
    except Exception as e:
        print(f"Error adding to PATH: {str(e)}")
        return False

if __name__ == "__main__":
    print("===== Tesseract OCR Installer =====\n")
    
    if not sys.platform.startswith('win'):
        print("This script is for Windows only. Please install Tesseract manually on your platform.")
        sys.exit(1)
    
    success = install_tesseract()
    
    if success:
        print("\nTesseract OCR installation completed successfully.")
        print("You may need to restart your application or computer for changes to take effect.")
    else:
        print("\nTesseract OCR installation may not have completed successfully.")
        print("Please try installing manually from: https://github.com/UB-Mannheim/tesseract/wiki")