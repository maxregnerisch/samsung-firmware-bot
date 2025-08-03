#!/usr/bin/env python3
"""
Telethon Upgrade Script for Python 3.12 Compatibility
This script helps upgrade Telethon to a compatible version.
"""

import subprocess
import sys
import pkg_resources

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 12:
        print("⚠️  Python 3.12+ detected - Telethon upgrade required")
        return True
    return False

def get_current_telethon_version():
    """Get currently installed Telethon version"""
    try:
        version = pkg_resources.get_distribution("Telethon").version
        print(f"📦 Current Telethon version: {version}")
        return version
    except pkg_resources.DistributionNotFound:
        print("❌ Telethon not installed")
        return None

def upgrade_telethon():
    """Upgrade Telethon to compatible version"""
    print("🔄 Upgrading Telethon...")
    
    try:
        # Uninstall old version first
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "Telethon", "-y"], 
                      check=True, capture_output=True)
        print("✅ Old Telethon version uninstalled")
        
        # Install new version
        subprocess.run([sys.executable, "-m", "pip", "install", "Telethon>=1.28.0"], 
                      check=True, capture_output=True)
        print("✅ Telethon upgraded successfully")
        
        # Verify installation
        new_version = get_current_telethon_version()
        if new_version:
            print(f"🎉 Telethon {new_version} installed successfully")
            return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error upgrading Telethon: {e}")
        return False
    
    return False

def install_all_requirements():
    """Install all requirements from requirements.txt"""
    print("📋 Installing all requirements...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("✅ All requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def main():
    """Main upgrade function"""
    print("🚀 Samsung Firmware Bot - Telethon Upgrade Tool")
    print("=" * 50)
    
    # Check Python version
    needs_upgrade = check_python_version()
    
    # Get current Telethon version
    current_version = get_current_telethon_version()
    
    if needs_upgrade or (current_version and current_version < "1.28.0"):
        print("\n🔧 Telethon upgrade required for compatibility")
        
        response = input("Do you want to upgrade Telethon now? (y/N): ")
        if response.lower() in ['y', 'yes']:
            if upgrade_telethon():
                print("\n✅ Upgrade completed successfully!")
                print("You can now run the bot with: python -m samfirm_bot")
            else:
                print("\n❌ Upgrade failed. Please try manual installation:")
                print("pip uninstall Telethon -y")
                print("pip install Telethon>=1.28.0")
        else:
            print("⚠️  Upgrade cancelled. The bot may not work with your current setup.")
    else:
        print("✅ Telethon version is compatible")
    
    # Offer to install all requirements
    print("\n📋 Would you like to install/update all requirements?")
    response = input("Install all requirements? (y/N): ")
    if response.lower() in ['y', 'yes']:
        install_all_requirements()
    
    print("\n🎯 Next steps:")
    print("1. Configure your credentials in config.json")
    print("2. Run: python start_bot.py")
    print("3. Or run directly: python -m samfirm_bot")

if __name__ == "__main__":
    main()

