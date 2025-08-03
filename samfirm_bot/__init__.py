""" SamFirm Bot initialization"""
import json
import logging
import sys
import os
from os.path import dirname, exists

WORK_DIR = dirname(__file__)
PARENT_DIR = '/'.join(dirname(__file__).split('/')[:-1])

# Default configuration
DEFAULT_CONFIG = {
    'tg_bot_token': '',
    'api_key': 0,
    'api_hash': '',
    'tg_bot_admins': [],
    'tg_channel': '@SamsungFirmwareSupport',
    'local_storage_path': './storage',
    'web_storage': 'http://localhost:8080'
}

# Load configuration with fallbacks
CONFIG = DEFAULT_CONFIG.copy()
config_path = f'{PARENT_DIR}/config.json'

if exists(config_path):
    try:
        with open(config_path, 'r') as f:
            file_config = json.load(f)
            CONFIG.update(file_config)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Warning: Could not load config.json: {e}")
        print("Using default configuration and environment variables")

# Environment variable fallbacks
API_KEY = int(os.getenv('TELEGRAM_API_ID', CONFIG['api_key'])) if os.getenv('TELEGRAM_API_ID') else CONFIG['api_key']
API_HASH = os.getenv('TELEGRAM_API_HASH', CONFIG['api_hash'])
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', CONFIG['tg_bot_token'])

# Extract Bot ID from token automatically
BOT_ID = None
if BOT_TOKEN:
    try:
        # Bot token format: "bot_id:auth_token"
        BOT_ID = int(BOT_TOKEN.split(':')[0])
    except (ValueError, IndexError):
        print("⚠️  Warning: Could not extract Bot ID from token")
        BOT_ID = 0
else:
    BOT_ID = 0

TG_BOT_ADMINS = CONFIG['tg_bot_admins']
TG_CHANNEL = CONFIG['tg_channel']
LOCAL_STORAGE = os.getenv('LOCAL_STORAGE', CONFIG['local_storage_path'])
WEB_STORAGE = os.getenv('WEB_STORAGE', CONFIG['web_storage'])

# Validate required configuration
if not API_KEY or not API_HASH or not BOT_TOKEN:
    print("❌ Error: Missing required Telegram credentials!")
    print("Please set the following:")
    print("1. Edit config.json with your credentials, OR")
    print("2. Set environment variables:")
    print("   - TELEGRAM_API_ID")
    print("   - TELEGRAM_API_HASH") 
    print("   - TELEGRAM_BOT_TOKEN")
    print("\nGet credentials from:")
    print("- API credentials: https://my.telegram.org/apps")
    print("- Bot token: @BotFather on Telegram")
    sys.exit(1)

# set logging
FORMATTER = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s'
                              '[%(module)s.%(funcName)s:%(lineno)d]: %(message)s')
OUT = logging.StreamHandler(sys.stdout)
ERR = logging.StreamHandler(sys.stderr)
OUT.setFormatter(FORMATTER)
ERR.setFormatter(FORMATTER)
OUT.setLevel(logging.INFO)
ERR.setLevel(logging.WARNING)
LOGGER = logging.getLogger()
LOGGER.addHandler(OUT)
LOGGER.addHandler(ERR)
LOGGER.setLevel(logging.INFO)
TG_LOGGER = logging.getLogger(__name__)
