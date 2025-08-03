#!/usr/bin/env python3
"""
Samsung Custom Firmware Bot Startup Script
This script provides a user-friendly way to start the bot with proper error handling.
"""

import os
import sys
import json
from pathlib import Path

def print_banner():
    """Print startup banner"""
    print("🚀 Samsung Custom Firmware Bot")
    print("=" * 50)

def check_config():
    """Check if configuration is properly set up"""
    config_path = Path("config.json")
    
    # Check if config.json exists and has valid content
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                
            # Check if required fields are filled
            required_fields = ['api_key', 'api_hash', 'tg_bot_token']
            missing_fields = []
            
            for field in required_fields:
                if not config.get(field) or config.get(field) == "" or config.get(field) == 0:
                    missing_fields.append(field)
            
            if missing_fields:
                print("⚠️  Configuration incomplete!")
                print(f"Missing or empty fields in config.json: {', '.join(missing_fields)}")
                return False
            
            return True
            
        except json.JSONDecodeError:
            print("❌ Error: config.json contains invalid JSON")
            return False
    
    # Check environment variables as fallback
    env_vars = ['TELEGRAM_API_ID', 'TELEGRAM_API_HASH', 'TELEGRAM_BOT_TOKEN']
    missing_env = []
    
    for var in env_vars:
        if not os.getenv(var):
            missing_env.append(var)
    
    if missing_env:
        print("❌ Configuration not found!")
        print("Neither config.json nor environment variables are properly set.")
        print("\n📋 Setup Instructions:")
        print("=" * 30)
        print("\n1️⃣  Option 1: Edit config.json")
        print("   - Copy config.json.example to config.json")
        print("   - Fill in your Telegram credentials")
        print("\n2️⃣  Option 2: Set environment variables")
        for var in env_vars:
            print(f"   export {var}=your_value_here")
        
        print("\n🔑 Get your credentials:")
        print("   - API ID & Hash: https://my.telegram.org/apps")
        print("   - Bot Token: @BotFather on Telegram")
        print("\n💡 Quick setup: Run ./setup.sh for automated installation")
        return False
    
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import telethon
        import aiohttp
        import requests
        print("✅ Dependencies check passed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def create_directories():
    """Create necessary directories"""
    dirs = ['storage', 'temp', 'logs']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
    print("✅ Directories created")

def main():
    """Main startup function"""
    print_banner()
    
    # Check configuration
    if not check_config():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    print("🚀 Starting Samsung Custom Firmware Bot...")
    print("Press Ctrl+C to stop the bot")
    print("-" * 50)
    
    # Import and run the bot
    try:
        from samfirm_bot import samfirm_bot
        samfirm_bot.main()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Bot crashed: {e}")
        print("Check the logs for more details")
        sys.exit(1)

if __name__ == "__main__":
    main()

