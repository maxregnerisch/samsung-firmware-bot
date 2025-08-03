#!/bin/bash

# Samsung Custom Firmware Bot Setup Script
# This script sets up the bot environment and dependencies

set -e

echo "🚀 Samsung Custom Firmware Bot Setup"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root for security reasons"
   exit 1
fi

# Check Python version
print_header "📋 Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_status "Python $PYTHON_VERSION found"
    
    # Check if Python version is 3.7 or higher
    if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 7) else 1)'; then
        print_status "Python version is compatible"
    else
        print_error "Python 3.7 or higher is required. Current version: $PYTHON_VERSION"
        exit 1
    fi
else
    print_error "Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Check if pip is installed
print_header "📦 Checking pip..."
if command -v pip3 &> /dev/null; then
    print_status "pip3 found"
else
    print_error "pip3 is not installed. Please install pip3."
    exit 1
fi

# Install system dependencies
print_header "🔧 Installing system dependencies..."
if command -v apt-get &> /dev/null; then
    print_status "Detected Debian/Ubuntu system"
    sudo apt-get update
    sudo apt-get install -y \
        wget \
        curl \
        unzip \
        p7zip-full \
        unrar \
        git \
        build-essential \
        python3-dev \
        libffi-dev \
        libssl-dev
elif command -v yum &> /dev/null; then
    print_status "Detected RHEL/CentOS system"
    sudo yum install -y \
        wget \
        curl \
        unzip \
        p7zip \
        unrar \
        git \
        gcc \
        python3-devel \
        libffi-devel \
        openssl-devel
elif command -v pacman &> /dev/null; then
    print_status "Detected Arch Linux system"
    sudo pacman -S --noconfirm \
        wget \
        curl \
        unzip \
        p7zip \
        unrar \
        git \
        base-devel \
        python \
        libffi \
        openssl
elif command -v brew &> /dev/null; then
    print_status "Detected macOS system"
    brew install \
        wget \
        curl \
        p7zip \
        unrar \
        git
else
    print_warning "Could not detect package manager. Please install dependencies manually:"
    print_warning "- wget, curl, unzip, p7zip, unrar, git, build tools"
fi

# Create virtual environment
print_header "🐍 Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
print_status "Virtual environment activated"

# Upgrade pip
print_header "📦 Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
print_header "📚 Installing Python dependencies..."
pip install -r requirements.txt
print_status "Python dependencies installed"

# Create necessary directories
print_header "📁 Creating directories..."
mkdir -p storage temp logs
print_status "Directories created"

# Copy configuration file
print_header "⚙️ Setting up configuration..."
if [ ! -f "config.json" ]; then
    if [ -f "config.json.example" ]; then
        cp config.json.example config.json
        print_status "Configuration file created from example"
        print_warning "Please edit config.json with your Telegram credentials"
    else
        print_error "config.json.example not found"
    fi
else
    print_status "Configuration file already exists"
fi

# Copy environment file
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_status "Environment file created from example"
        print_warning "Please edit .env with your configuration"
    fi
else
    print_status "Environment file already exists"
fi

# Set permissions
print_header "🔒 Setting permissions..."
chmod +x setup.sh
chmod 755 storage temp logs
print_status "Permissions set"

# Create systemd service (optional)
print_header "🔧 Creating systemd service (optional)..."
read -p "Do you want to create a systemd service? (y/N): " create_service
if [[ $create_service =~ ^[Yy]$ ]]; then
    SERVICE_FILE="/etc/systemd/system/samsung-firmware-bot.service"
    CURRENT_USER=$(whoami)
    CURRENT_DIR=$(pwd)
    
    sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Samsung Custom Firmware Bot
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$CURRENT_DIR
Environment=PATH=$CURRENT_DIR/venv/bin
ExecStart=$CURRENT_DIR/venv/bin/python -m samfirm_bot
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    sudo systemctl daemon-reload
    print_status "Systemd service created"
    print_status "Use 'sudo systemctl enable samsung-firmware-bot' to enable auto-start"
    print_status "Use 'sudo systemctl start samsung-firmware-bot' to start the service"
fi

# Final instructions
print_header "✅ Setup Complete!"
echo ""
print_status "Next steps:"
echo "1. Edit config.json with your Telegram API credentials"
echo "2. Edit .env with your environment configuration"
echo "3. Run the bot with: python -m samfirm_bot"
echo ""
print_status "For Docker deployment:"
echo "1. Copy .env.example to .env and configure"
echo "2. Run: docker-compose up -d"
echo ""
print_status "For more information, see README.md"
echo ""
print_warning "Remember to:"
echo "- Get Telegram API credentials from https://my.telegram.org/apps"
echo "- Create a bot with @BotFather on Telegram"
echo "- Keep your credentials secure and never commit them to version control"
echo ""
print_status "Happy firmware building! 🚀"

