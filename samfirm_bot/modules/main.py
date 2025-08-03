""" SamFirm Bot main module"""

from telethon import events

from samfirm_bot.samfirm_bot import BOT


@BOT.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Send a message when the command /start is sent."""
    from telethon import Button
    
    welcome_text = """
🚀 **Samsung Custom Firmware Bot**

Welcome to the most advanced Samsung firmware tool on Telegram! 

**🔧 What I can do:**
• 📥 Download official Samsung firmware
• 🛠️ Create custom firmware with your preferences
• 📱 Extract and analyze firmware files
• 🔍 Check firmware information and updates
• 📋 Provide device-specific flashing guides
• 🆘 Emergency recovery assistance

**🎯 Quick Start:**
• `/create_firmware` - Build custom firmware
• `/firmware_info MODEL CSC REGION` - Get firmware info
• `/device_support` - Check supported devices
• `/help` - Full command list

**⚡ Popular Commands:**
• `/firmware_info SM-G973F XEF EUR` - Galaxy S10 info
• `/download_firmware SM-G973F XEF EUR` - Download firmware
• `/flash_guide SM-G973F` - Flashing instructions

Ready to customize your Samsung device? Let's get started! 🎉
"""
    
    buttons = [
        [Button.inline("🔧 Create Custom Firmware", b"start_create_firmware")],
        [Button.inline("📱 Check Device Support", b"start_device_support")],
        [Button.inline("📋 View All Commands", b"start_help")],
        [Button.url("💬 Join Support Group", "https://t.me/SamsungFirmwareSupport")]
    ]
    
    await event.reply(welcome_text, buttons=buttons)
    raise events.StopPropagation

@BOT.on(events.CallbackQuery(pattern=b"start_(.*)"))
async def start_menu_callbacks(event):
    """Handle start menu button callbacks"""
    action = event.data.decode().split('_', 1)[1]
    
    if action == "create_firmware":
        await event.answer("🔧 Starting firmware creator...")
        # Trigger the create firmware flow
        from telethon import Button
        buttons = [
            [Button.inline("🔧 Custom ROM", b"fw_type_custom_rom")],
            [Button.inline("🛠️ Stock Firmware Mod", b"fw_type_stock_mod")],
            [Button.inline("⚡ Performance Firmware", b"fw_type_performance")],
            [Button.inline("🔒 Security Firmware", b"fw_type_security")],
            [Button.inline("❌ Cancel", b"fw_cancel")]
        ]
        
        await event.edit(
            "🚀 **Samsung Custom Firmware Creator**\n\n"
            "Select the type of firmware you want to create:",
            buttons=buttons
        )
    
    elif action == "device_support":
        await event.answer("📱 Loading device support...")
        # Show device support info
        supported_text = """
📱 **Quick Device Support Check**

**Fully Supported:**
• Galaxy S10 series (SM-G973F, SM-G975F)
• Galaxy S20 series (SM-G981B, SM-G985F, SM-G988B)
• Galaxy Note 10 series (SM-N970F, SM-N975F)
• Galaxy A50/A51/A71 series

**Beta Support:**
• Galaxy S10 5G, Note 20 series
• Galaxy A52 and newer A-series

Use `/device_support` for the complete list with detailed status.
"""
        await event.edit(supported_text)
    
    elif action == "help":
        await event.answer("📋 Loading help...")
        await show_help_menu(event)


@BOT.on(events.NewMessage(pattern='/help'))
async def help_command(event):
    """Show comprehensive help"""
    await show_help_menu(event)


async def show_help_menu(event):
    """Show the help menu"""
    from telethon import Button
    
    help_text = """
📋 **Samsung Firmware Bot - Complete Command List**

**🔧 Firmware Creation:**
• `/create_firmware` - Interactive custom firmware builder
• `/firmware_help` - Detailed firmware creation guide

**📥 Firmware Management:**
• `/firmware_info MODEL CSC REGION` - Get firmware information
• `/download_firmware MODEL CSC REGION` - Download official firmware
• `/extract_firmware` - Extract uploaded firmware files

**📱 Device Support:**
• `/device_support` - List all supported devices
• `/flash_guide MODEL` - Device-specific flashing instructions

**🔍 Information Commands:**
• `/start` - Show welcome message and quick actions
• `/help` - Show this help menu

**📋 Example Usage:**
• `/firmware_info SM-G973F XEF EUR`
• `/download_firmware SM-G973F XEF EUR`
• `/flash_guide SM-G973F`

**💡 Tips:**
• Always backup your device before flashing
• Ensure bootloader is unlocked for custom firmware
• Join our support group for assistance

**⚠️ Disclaimer:**
This bot is for educational purposes. Flashing custom firmware may void warranty and can brick your device. Proceed at your own risk.
"""
    
    buttons = [
        [Button.inline("🔧 Firmware Creation Help", b"help_firmware")],
        [Button.inline("📱 Device Support", b"help_devices")],
        [Button.inline("🆘 Troubleshooting", b"help_troubleshoot")],
        [Button.url("💬 Support Group", "https://t.me/SamsungFirmwareSupport")]
    ]
    
    if hasattr(event, 'edit'):
        await event.edit(help_text, buttons=buttons)
    else:
        await event.reply(help_text, buttons=buttons)


@BOT.on(events.CallbackQuery(pattern=b"help_(.*)"))
async def help_callbacks(event):
    """Handle help menu callbacks"""
    help_type = event.data.decode().split('_', 1)[1]
    
    if help_type == "firmware":
        help_text = """
🔧 **Custom Firmware Creation Help**

**Step-by-Step Process:**

**1. Start Creation:**
• Use `/create_firmware` command
• Select firmware type (Custom ROM, Stock Mod, etc.)

**2. Device Information:**
• Provide: MODEL CSC REGION
• Example: `SM-G973F XEF EUR`

**3. Customization Options:**
• **UI:** Dark themes, custom icons, scaling
• **Performance:** CPU overclock, battery optimization
• **Security:** Root access, SELinux modifications
• **Apps:** Bloatware removal, custom apps
• **Advanced:** Build.prop mods, filesystem tweaks

**4. Build Process:**
• Review selections
• Start build (takes 5-15 minutes)
• Download completed firmware

**5. Installation:**
• Use Odin (Windows) or Heimdall (Linux/Mac)
• Follow device-specific flashing guide
• Flash at your own risk!

**Requirements:**
• Unlocked bootloader
• USB debugging enabled
• Proper USB drivers installed
"""
        
    elif help_type == "devices":
        help_text = """
📱 **Device Support Information**

**Support Levels:**
• ✅ **Full Support:** All features available
• ⚠️ **Beta Support:** Basic features, some limitations
• 🔄 **In Development:** Coming soon

**How to Check Support:**
• Use `/device_support` for complete list
• Check your exact model number
• Verify CSC/region compatibility

**Request New Device Support:**
• Send model number and region
• Provide firmware download links if available
• Join support group for faster processing

**Common Issues:**
• Model variants may have different support levels
• Some regions may not be supported yet
• Carrier-locked devices may have limitations
"""
        
    elif help_type == "troubleshoot":
        help_text = """
🆘 **Troubleshooting Guide**

**Common Issues:**

**Bot Not Responding:**
• Check internet connection
• Try restarting conversation with `/start`
• Report persistent issues in support group

**Firmware Download Fails:**
• Verify model/CSC/region format
• Check if device is supported
• Try again later (server may be busy)

**Custom Firmware Build Fails:**
• Ensure all required info is provided
• Check device support level
• Contact support with error details

**Flashing Issues:**
• Verify bootloader is unlocked
• Use correct Odin version
• Check USB drivers and cable
• Ensure sufficient battery (50%+)

**Device Won't Boot After Flash:**
• Try flashing stock firmware
• Wipe data in recovery mode
• Use emergency recovery procedures

**Need More Help?**
Join our support group: @SamsungFirmwareSupport
"""
    
    from telethon import Button
    back_button = [[Button.inline("🔙 Back to Help", b"start_help")]]
    
    await event.edit(help_text, buttons=back_button)


# @BOT.on(events.NewMessage)
# async def echo(event):
#     """Echo the user message."""
#     await event.respond(event.text)
