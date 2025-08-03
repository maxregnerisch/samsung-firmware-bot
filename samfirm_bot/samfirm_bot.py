#!/usr/bin/env python3
""" SamFirm Telegram Bot"""
import asyncio
import pickle
import sys
from os import path, remove

from telethon.sync import TelegramClient

from samfirm_bot import API_KEY, API_HASH, BOT_TOKEN, TG_LOGGER, LOCAL_STORAGE, WEB_STORAGE, PARENT_DIR, WORK_DIR
from samfirm_bot.classes.local_client import LocalClient
from samfirm_bot.classes.samfirm import SamFirm
from samfirm_bot.modules import ALL_MODULES
from samfirm_bot.utils.loader import load_modules

# Initialize bot with error handling for different Python/Telethon versions
try:
    BOT = TelegramClient('samfirm_bot', API_KEY, API_HASH).start(bot_token=BOT_TOKEN)
    BOT.parse_mode = 'markdown'
    BOT_INFO = {}
    
    # Initialize storage (doesn't need event loop)
    STORAGE = LocalClient(LOCAL_STORAGE, WEB_STORAGE)
    
    # Initialize SamFirm without loop initially - it will be set up later
    SAM_FIRM = SamFirm()
    
except Exception as e:
    print(f"❌ Error initializing bot: {e}")
    print("This might be due to:")
    print("1. Incompatible Telethon version - try: pip install --upgrade Telethon>=1.28.0")
    print("2. Invalid credentials in config.json")
    print("3. Network connectivity issues")
    sys.exit(1)


def main():
    """Main"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


async def run():
    """Run the bot."""
    global SAM_FIRM
    
    # Set the event loop on the existing SamFirm instance
    try:
        loop = asyncio.get_running_loop()
        SAM_FIRM.loop = loop
        # Now create the models_loop task
        if hasattr(SAM_FIRM, 'models_loop'):
            SAM_FIRM.loop.create_task(SAM_FIRM.models_loop())
        TG_LOGGER.info("SamFirm event loop initialized successfully")
    except Exception as e:
        TG_LOGGER.warning(f"Could not set SamFirm event loop: {e}")
    
    bot_info = await BOT.get_me()
    BOT_INFO.update({'name': bot_info.first_name,
                     'username': bot_info.username, 'id': bot_info.id})
    TG_LOGGER.info("Bot started as %s! Username is %s and ID is %s",
                   BOT_INFO['name'], BOT_INFO['username'], BOT_INFO['id'])
    TG_LOGGER.info(f"Storage location: {LOCAL_STORAGE} - Website URL:{WEB_STORAGE}")
    TG_LOGGER.info(f"Work directory: {WORK_DIR} - Parent directory: {PARENT_DIR}")
    load_modules(ALL_MODULES, __package__)
    # Check if the bot is restarting
    if path.exists('restart.pickle'):
        with open('restart.pickle', 'rb') as status:
            restart_message = pickle.load(status)
        await BOT.edit_message(restart_message['chat'], restart_message['message'], 'Restarted Successfully!')
        remove('restart.pickle')
    async with BOT:
        await BOT.run_until_disconnected()
