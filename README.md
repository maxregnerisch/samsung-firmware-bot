# Samsung Custom Firmware Bot 🚀

A comprehensive Telegram bot for Samsung firmware management and custom firmware creation. This bot allows users to download official Samsung firmware, create custom firmware with various modifications, and provides detailed flashing guides.

## ✨ Features

### 🔧 Custom Firmware Creation
- **Interactive Firmware Builder**: Step-by-step custom firmware creation
- **Multiple Firmware Types**: Custom ROM, Stock Mods, Performance, Security
- **Extensive Customization Options**:
  - 🎨 UI Customization (Dark themes, custom icons, scaling)
  - ⚡ Performance Tweaks (CPU overclock, battery optimization, RAM management)
  - 🔒 Security Modifications (Root access, SELinux, encryption settings)
  - 📱 System Apps Management (Bloatware removal, custom apps)
  - 🔧 Advanced Options (Build.prop mods, filesystem tweaks)

### 📥 Firmware Management
- **Official Firmware Download**: Direct download from Samsung servers
- **Firmware Information**: Detailed firmware info with changelog
- **Firmware Extraction**: Extract and analyze uploaded firmware files
- **Update Checking**: Check for latest firmware versions

### 📱 Device Support
- **Wide Device Coverage**: Galaxy S, Note, and A series support
- **Device-Specific Guides**: Tailored flashing instructions per device
- **Support Status Tracking**: Full, Beta, and In-Development support levels

### 🆘 User Assistance
- **Comprehensive Help System**: Detailed guides and troubleshooting
- **Interactive Menus**: Easy-to-use button interfaces
- **Emergency Recovery**: Recovery procedures for bricked devices
- **Community Support**: Integrated support group access

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Telegram Bot Token
- Telegram API credentials

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/maxregnerisch/samsung-firmware-bot.git
cd samsung-firmware-bot
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure the bot**:
```bash
cp config.json.example config.json
# Edit config.json with your credentials
```

4. **Configure credentials**:
```bash
# Option 1: Edit config.json (recommended)
cp config.json.example config.json
# Edit config.json with your Telegram credentials

# Option 2: Use environment variables
export TELEGRAM_API_ID="your_api_id"
export TELEGRAM_API_HASH="your_api_hash"
export TELEGRAM_BOT_TOKEN="your_bot_token"
```

5. **Run the bot**:
```bash
# Using the startup script (recommended)
python start_bot.py

# Or directly
python -m samfirm_bot
```

## 📋 Commands

### 🔧 Firmware Creation
- `/create_firmware` - Interactive custom firmware builder
- `/firmware_help` - Detailed firmware creation guide

### 📥 Firmware Management
- `/firmware_info MODEL CSC REGION` - Get firmware information
- `/download_firmware MODEL CSC REGION` - Download official firmware
- `/extract_firmware` - Extract uploaded firmware files (reply to file)

### 📱 Device Support
- `/device_support` - List all supported devices
- `/flash_guide MODEL` - Device-specific flashing instructions

### 🔍 Information & Help
- `/start` - Welcome message and quick actions
- `/help` - Complete command list and guides

### 📋 Example Usage
```
/firmware_info SM-G973F XEF EUR
/download_firmware SM-G973F XEF EUR
/flash_guide SM-G973F
```

## 🏗️ Architecture

### Core Components

#### 📁 Project Structure
```
samfirm_bot/
├── classes/
│   ├── firmware_builder.py    # Custom firmware building logic
│   ├── local_client.py        # Local storage management
│   ├── samfirm.py            # Samsung firmware operations
│   └── sftp_client.py        # SFTP operations
├── modules/
│   ├── custom_firmware.py    # Custom firmware creation handlers
│   ├── firmware_tools.py     # Firmware management tools
│   ├── main.py              # Main bot commands and help
│   ├── sam_check.py         # Firmware checking
│   ├── sam_get.py           # Firmware downloading
│   └── sam_mirror.py        # Firmware mirroring
├── utils/
│   └── loader.py            # Module loading utilities
└── samfirm_bot.py           # Main bot application
```

#### 🔧 Key Classes

**FirmwareBuilder**: Handles custom firmware creation
- Device-specific firmware building
- Customization application
- Progress tracking
- Output packaging

**LocalClient**: Manages local storage and file operations
- Temporary file management
- Storage optimization
- File cleanup

## 📱 Supported Devices

### ✅ Full Support
- **Galaxy S Series**: S10, S10+, S20, S20+, S20 Ultra
- **Galaxy Note Series**: Note 10, Note 10+
- **Galaxy A Series**: A50, A51, A71

### ⚠️ Beta Support
- **Galaxy S Series**: S10 5G
- **Galaxy Note Series**: Note 20, Note 20 Ultra
- **Galaxy A Series**: A52 and newer

### 🔄 In Development
- Additional Galaxy A series devices
- Older Galaxy S and Note series
- Galaxy Tab series

## 🛠️ Configuration

### config.json Structure
```json
{
  "api_id": "your_api_id",
  "api_hash": "your_api_hash",
  "bot_token": "your_bot_token",
  "storage": {
    "local_path": "/path/to/storage",
    "web_url": "https://your-storage-url.com"
  },
  "logging": {
    "level": "INFO",
    "file": "bot.log"
  }
}
```

### Environment Variables
```bash
export TELEGRAM_API_ID="your_api_id"
export TELEGRAM_API_HASH="your_api_hash"
export TELEGRAM_BOT_TOKEN="your_bot_token"
```

## 🔒 Security & Disclaimers

### ⚠️ Important Warnings
- **Warranty Void**: Custom firmware may void device warranty
- **Brick Risk**: Improper flashing can permanently damage devices
- **Backup Required**: Always backup device before flashing
- **Bootloader**: Device bootloader must be unlocked

### 🛡️ Security Features
- Input validation and sanitization
- Secure file handling
- Temporary file cleanup
- Error handling and logging

## 🔧 Troubleshooting

### Common Issues

#### ❌ JSON Configuration Error
```
json.decoder.JSONDecodeError: Expecting value: line 1 column 2 (char 1)
```
**Solution:**
1. Ensure `config.json` exists and has valid JSON format
2. Copy from example: `cp config.json.example config.json`
3. Fill in your credentials or use environment variables

#### ❌ Missing Telegram Credentials
```
Error: Missing required Telegram credentials!
```
**Solution:**
1. Get API credentials from https://my.telegram.org/apps
2. Create a bot with @BotFather on Telegram
3. Add credentials to `config.json` or set environment variables

#### ❌ Import Errors
```
ModuleNotFoundError: No module named 'telethon'
```
**Solution:**
```bash
pip install -r requirements.txt
```

#### ❌ Permission Errors
```
PermissionError: [Errno 13] Permission denied
```
**Solution:**
```bash
chmod +x setup.sh start_bot.py
mkdir -p storage temp logs
```

### Getting Help
- Use `python start_bot.py` for user-friendly startup with error checking
- Check logs in the `logs/` directory
- Join our support group: @SamsungFirmwareSupport

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Install development dependencies
4. Make your changes
5. Test thoroughly
6. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to functions and classes
- Include error handling

## 📞 Support

### 💬 Community Support
- **Telegram Group**: [@SamsungFirmwareSupport](https://t.me/SamsungFirmwareSupport)
- **Issues**: [GitHub Issues](https://github.com/maxregnerisch/samsung-firmware-bot/issues)

### 🐛 Bug Reports
When reporting bugs, please include:
- Device model and firmware version
- Complete error message
- Steps to reproduce
- Bot logs (if available)

### 💡 Feature Requests
- Check existing issues first
- Provide detailed use case
- Include device compatibility requirements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **SamFirm**: Original firmware downloading tool
- **Telethon**: Telegram client library
- **Samsung**: For providing firmware access
- **Community**: Beta testers and contributors

## 🔄 Changelog

### v2.0.0 (Current)
- ✨ Added custom firmware creation
- 🎨 Interactive UI with buttons
- 📱 Extended device support
- 🆘 Comprehensive help system
- 🔧 Advanced customization options

### v1.0.0 (Legacy)
- 📥 Basic firmware downloading
- 🔍 Firmware information checking
- 📋 Simple command interface

---

**⚠️ Disclaimer**: This bot is for educational and research purposes. Users are responsible for their actions. Always backup your device and understand the risks before flashing custom firmware.
