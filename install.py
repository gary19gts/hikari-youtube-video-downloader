#!/usr/bin/env python3
"""
Hikari Youtube Video Downloader - Installation Script
Developed by Gary19gts
"""

import subprocess
import sys
import os

def print_header():
    """Print installation header"""
    print("=" * 60)
    print("  🎬 Hikari Youtube Video Downloader")
    print("  Installation Script")
    print("  Developed by Gary19gts")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("📋 Checking Python version...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detected")
        print("⚠️  Python 3.8 or higher is required")
        print("📥 Download from: https://www.python.org/downloads/")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    print("-" * 60)
    
    requirements = [
        "yt-dlp>=2023.12.30",
        "pytube>=15.0.0",
        "customtkinter>=5.2.0",
        "requests>=2.31.0",
        "Pillow>=10.0.0"
    ]
    
    for req in requirements:
        package_name = req.split(">=")[0]
        print(f"\n📥 Installing {package_name}...")
        
        try:
            subprocess.check_call([
                sys.executable, 
                "-m", 
                "pip", 
                "install", 
                "--upgrade",
                req
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ {package_name} installed successfully")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package_name}")
            return False
    
    return True

def verify_installation():
    """Verify that all packages are installed correctly"""
    print("\n🔍 Verifying installation...")
    print("-" * 60)
    
    packages = {
        "yt_dlp": "yt-dlp",
        "pytube": "pytube",
        "customtkinter": "customtkinter",
        "requests": "requests",
        "PIL": "Pillow"
    }
    
    all_ok = True
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"✅ {name} is working")
        except ImportError:
            print(f"❌ {name} is not installed correctly")
            all_ok = False
    
    return all_ok

def create_shortcut_windows():
    """Create desktop shortcut on Windows"""
    if sys.platform != "win32":
        return
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "Hikari Youtube Downloader.lnk")
        target = os.path.join(os.getcwd(), "hikari-youtube-video-downloader.py")
        icon = os.path.join(os.getcwd(), "hikari-youtube-video-downloader.py")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{target}"'
        shortcut.WorkingDirectory = os.getcwd()
        shortcut.IconLocation = icon
        shortcut.save()
        
        print("\n✅ Desktop shortcut created")
    except:
        print("\n⚠️  Could not create desktop shortcut")

def print_success():
    """Print success message"""
    print("\n" + "=" * 60)
    print("  ✅ Installation completed successfully!")
    print("=" * 60)
    print("\n🚀 To run Hikari Youtube Video Downloader:")
    print()
    
    if sys.platform == "win32":
        print("   Option 1: Double-click 'run_hikari.bat'")
        print("   Option 2: Run 'python hikari-youtube-video-downloader.py'")
    else:
        print("   Run: python3 hikari-youtube-video-downloader.py")
    
    print("\n📚 Documentation:")
    print("   - README.md - User guide")
    print("   - DESIGN_GUIDE.md - Design documentation")
    print("   - CHANGELOG.md - Version history")
    
    print("\n💝 Support Development:")
    print("   ☕ https://ko-fi.com/gary19gts")
    
    print("\n" + "=" * 60)
    print("  Thank you for using Hikari! ❤️")
    print("  Developed by Gary19gts - 2025")
    print("=" * 60)

def main():
    """Main installation process"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Installation failed")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        print("\n⚠️  Some packages may not be installed correctly")
        print("Try running: pip install -r requirements.txt")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Create shortcut (Windows only)
    if sys.platform == "win32":
        create_shortcut_windows()
    
    # Print success message
    print_success()
    
    # Ask to run the application
    print()
    response = input("Would you like to run Hikari now? (y/n): ").lower()
    if response == 'y':
        print("\n🚀 Starting Hikari Youtube Video Downloader...")
        try:
            subprocess.run([sys.executable, "hikari-youtube-video-downloader.py"])
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
        except Exception as e:
            print(f"\n❌ Error starting application: {e}")
    else:
        print("\n👋 Installation complete. Run Hikari anytime!")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Installation cancelled by user")
        input("\nPress Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)
