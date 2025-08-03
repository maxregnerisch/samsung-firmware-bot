""" Samsung Custom Firmware Creator Module """

import os
import asyncio
import zipfile
import tempfile
import shutil
from pathlib import Path
from telethon import events, Button
from telethon.tl.types import DocumentAttributeFilename

from samfirm_bot.samfirm_bot import BOT, TG_LOGGER
from samfirm_bot.classes.firmware_builder import FirmwareBuilder


@BOT.on(events.NewMessage(pattern='/create_firmware'))
async def create_firmware_start(event):
    """Start custom firmware creation process"""
    user_id = event.sender_id
    
    # Create inline keyboard for firmware type selection
    buttons = [
        [Button.inline("🔧 Custom ROM", b"fw_type_custom_rom")],
        [Button.inline("🛠️ Stock Firmware Mod", b"fw_type_stock_mod")],
        [Button.inline("⚡ Performance Firmware", b"fw_type_performance")],
        [Button.inline("🔒 Security Firmware", b"fw_type_security")],
        [Button.inline("❌ Cancel", b"fw_cancel")]
    ]
    
    await event.reply(
        "🚀 **Samsung Custom Firmware Creator**\n\n"
        "Select the type of firmware you want to create:",
        buttons=buttons
    )
    raise events.StopPropagation


@BOT.on(events.CallbackQuery(pattern=b"fw_type_(.*)"))
async def firmware_type_selected(event):
    """Handle firmware type selection"""
    fw_type = event.data.decode().split('_', 2)[2]
    
    if fw_type == "cancel":
        await event.edit("❌ Firmware creation cancelled.")
        return
    
    # Store user's firmware type choice
    user_data = {
        'fw_type': fw_type,
        'step': 'device_info'
    }
    
    await event.edit(
        f"✅ **{get_fw_type_name(fw_type)}** selected!\n\n"
        "📱 Please provide your device information:\n"
        "Format: `MODEL CSC REGION`\n\n"
        "Example: `SM-G973F XEF EUR`\n"
        "- MODEL: Your device model (e.g., SM-G973F)\n"
        "- CSC: Country/Carrier code (e.g., XEF)\n"
        "- REGION: Region code (e.g., EUR)\n\n"
        "Send the device info in the next message."
    )


@BOT.on(events.NewMessage(pattern='/device_info (.+)'))
async def device_info_received(event):
    """Handle device information input"""
    device_info = event.pattern_match.group(1).strip().split()
    
    if len(device_info) != 3:
        await event.reply(
            "❌ Invalid format! Please use: `MODEL CSC REGION`\n"
            "Example: `SM-G973F XEF EUR`"
        )
        return
    
    model, csc, region = device_info
    
    # Validate device info format
    if not model.startswith('SM-'):
        await event.reply("❌ Invalid model format! Model should start with 'SM-'")
        return
    
    # Create firmware builder instance
    builder = FirmwareBuilder(model, csc, region)
    
    # Create inline keyboard for customization options
    buttons = [
        [Button.inline("🎨 UI Customization", b"custom_ui")],
        [Button.inline("⚡ Performance Tweaks", b"custom_performance")],
        [Button.inline("🔒 Security Mods", b"custom_security")],
        [Button.inline("📱 System Apps", b"custom_apps")],
        [Button.inline("🔧 Advanced Options", b"custom_advanced")],
        [Button.inline("✅ Start Building", b"start_build")],
        [Button.inline("❌ Cancel", b"fw_cancel")]
    ]
    
    await event.reply(
        f"📱 **Device Info Confirmed**\n"
        f"Model: `{model}`\n"
        f"CSC: `{csc}`\n"
        f"Region: `{region}`\n\n"
        "🛠️ **Customization Options:**\n"
        "Select what you want to customize:",
        buttons=buttons
    )
    
    # Store builder instance (in production, use proper session storage)
    BOT._firmware_builders = getattr(BOT, '_firmware_builders', {})
    BOT._firmware_builders[event.sender_id] = builder


@BOT.on(events.CallbackQuery(pattern=b"custom_(.*)"))
async def customization_selected(event):
    """Handle customization option selection"""
    option = event.data.decode().split('_', 1)[1]
    user_id = event.sender_id
    
    builder = BOT._firmware_builders.get(user_id)
    if not builder:
        await event.answer("❌ Session expired. Please start over with /create_firmware")
        return
    
    if option == "ui":
        buttons = [
            [Button.inline("🌙 Dark Theme", b"ui_dark_theme")],
            [Button.inline("🎨 Custom Icons", b"ui_custom_icons")],
            [Button.inline("📐 UI Scaling", b"ui_scaling")],
            [Button.inline("🔙 Back", b"back_to_main")]
        ]
        await event.edit("🎨 **UI Customization Options:**", buttons=buttons)
        
    elif option == "performance":
        buttons = [
            [Button.inline("🚀 CPU Overclock", b"perf_cpu_oc")],
            [Button.inline("🔋 Battery Optimization", b"perf_battery")],
            [Button.inline("💾 RAM Management", b"perf_ram")],
            [Button.inline("🔙 Back", b"back_to_main")]
        ]
        await event.edit("⚡ **Performance Tweaks:**", buttons=buttons)
        
    elif option == "security":
        buttons = [
            [Button.inline("🔐 Root Access", b"sec_root")],
            [Button.inline("🛡️ SELinux Mods", b"sec_selinux")],
            [Button.inline("🔒 Encryption", b"sec_encryption")],
            [Button.inline("🔙 Back", b"back_to_main")]
        ]
        await event.edit("🔒 **Security Modifications:**", buttons=buttons)
        
    elif option == "apps":
        buttons = [
            [Button.inline("🗑️ Remove Bloatware", b"apps_debloat")],
            [Button.inline("📦 Add Custom Apps", b"apps_custom")],
            [Button.inline("🔧 System Mods", b"apps_system")],
            [Button.inline("🔙 Back", b"back_to_main")]
        ]
        await event.edit("📱 **System Apps Management:**", buttons=buttons)
        
    elif option == "advanced":
        buttons = [
            [Button.inline("🔧 Build.prop Mods", b"adv_buildprop")],
            [Button.inline("🗂️ File System Tweaks", b"adv_filesystem")],
            [Button.inline("🌐 Network Mods", b"adv_network")],
            [Button.inline("🔙 Back", b"back_to_main")]
        ]
        await event.edit("🔧 **Advanced Options:**", buttons=buttons)


@BOT.on(events.CallbackQuery(pattern=b"start_build"))
async def start_firmware_build(event):
    """Start the firmware building process"""
    user_id = event.sender_id
    builder = BOT._firmware_builders.get(user_id)
    
    if not builder:
        await event.answer("❌ Session expired. Please start over with /create_firmware")
        return
    
    await event.edit("🔄 **Starting firmware build process...**\n\nThis may take several minutes.")
    
    try:
        # Start the build process
        progress_msg = await event.respond("📊 **Build Progress:**\n▱▱▱▱▱▱▱▱▱▱ 0%")
        
        async def progress_callback(step, percentage):
            progress_bar = "▰" * (percentage // 10) + "▱" * (10 - percentage // 10)
            await progress_msg.edit(f"📊 **Build Progress:**\n{progress_bar} {percentage}%\n\n🔧 {step}")
        
        # Build the firmware
        firmware_path = await builder.build_firmware(progress_callback)
        
        if firmware_path and os.path.exists(firmware_path):
            await progress_msg.edit("✅ **Firmware build completed successfully!**")
            
            # Upload the firmware file
            await event.respond(
                "📦 **Custom Firmware Ready!**\n\n"
                f"Device: {builder.model}\n"
                f"Build: Custom-{builder.get_build_id()}\n"
                f"Size: {get_file_size(firmware_path)}\n\n"
                "⚠️ **Warning:** Flash at your own risk!\n"
                "Make sure to backup your device before flashing.",
                file=firmware_path
            )
            
            # Cleanup
            os.remove(firmware_path)
            
        else:
            await progress_msg.edit("❌ **Build failed!** Please try again or contact support.")
            
    except Exception as e:
        TG_LOGGER.error(f"Firmware build error: {e}")
        await event.respond(f"❌ **Build Error:** {str(e)}")
    
    finally:
        # Cleanup builder instance
        if user_id in BOT._firmware_builders:
            del BOT._firmware_builders[user_id]


@BOT.on(events.NewMessage(pattern='/firmware_help'))
async def firmware_help(event):
    """Show firmware creation help"""
    help_text = """
🚀 **Samsung Custom Firmware Creator Help**

**Commands:**
• `/create_firmware` - Start creating custom firmware
• `/device_info MODEL CSC REGION` - Set device information
• `/firmware_help` - Show this help message

**Supported Features:**
🎨 **UI Customization:**
- Dark themes and custom icons
- UI scaling and layout modifications
- Custom boot animations

⚡ **Performance Tweaks:**
- CPU overclocking profiles
- Battery optimization
- RAM management improvements
- I/O scheduler optimizations

🔒 **Security Modifications:**
- Root access integration
- SELinux policy modifications
- Custom encryption settings

📱 **System Apps:**
- Bloatware removal
- Custom app integration
- System-level modifications

🔧 **Advanced Options:**
- Build.prop modifications
- File system tweaks
- Network optimizations
- Kernel modifications

**Supported Devices:**
- Galaxy S series (S10+)
- Galaxy Note series (Note 9+)
- Galaxy A series (A50+)
- More devices being added regularly

**Requirements:**
- Original firmware files
- Device bootloader must be unlocked
- Basic knowledge of Android flashing

⚠️ **Disclaimer:**
Custom firmware flashing can brick your device. Always backup your device and proceed at your own risk.
"""
    
    await event.reply(help_text)


def get_fw_type_name(fw_type):
    """Get human-readable firmware type name"""
    types = {
        'custom_rom': 'Custom ROM',
        'stock_mod': 'Stock Firmware Modification',
        'performance': 'Performance Firmware',
        'security': 'Security Firmware'
    }
    return types.get(fw_type, 'Unknown')


def get_file_size(file_path):
    """Get human-readable file size"""
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


# Additional callback handlers for specific customizations
@BOT.on(events.CallbackQuery(pattern=b"ui_(.*)"))
async def ui_customization(event):
    """Handle UI customization options"""
    option = event.data.decode().split('_', 1)[1]
    user_id = event.sender_id
    builder = BOT._firmware_builders.get(user_id)
    
    if not builder:
        await event.answer("❌ Session expired")
        return
    
    if option == "dark_theme":
        builder.add_customization('ui', 'dark_theme', True)
        await event.answer("✅ Dark theme enabled")
    elif option == "custom_icons":
        builder.add_customization('ui', 'custom_icons', True)
        await event.answer("✅ Custom icons enabled")
    elif option == "scaling":
        builder.add_customization('ui', 'scaling', 'optimized')
        await event.answer("✅ UI scaling optimized")


@BOT.on(events.CallbackQuery(pattern=b"perf_(.*)"))
async def performance_customization(event):
    """Handle performance customization options"""
    option = event.data.decode().split('_', 1)[1]
    user_id = event.sender_id
    builder = BOT._firmware_builders.get(user_id)
    
    if not builder:
        await event.answer("❌ Session expired")
        return
    
    if option == "cpu_oc":
        builder.add_customization('performance', 'cpu_overclock', True)
        await event.answer("✅ CPU overclock enabled")
    elif option == "battery":
        builder.add_customization('performance', 'battery_optimization', True)
        await event.answer("✅ Battery optimization enabled")
    elif option == "ram":
        builder.add_customization('performance', 'ram_management', 'aggressive')
        await event.answer("✅ RAM management optimized")


@BOT.on(events.CallbackQuery(pattern=b"sec_(.*)"))
async def security_customization(event):
    """Handle security customization options"""
    option = event.data.decode().split('_', 1)[1]
    user_id = event.sender_id
    builder = BOT._firmware_builders.get(user_id)
    
    if not builder:
        await event.answer("❌ Session expired")
        return
    
    if option == "root":
        builder.add_customization('security', 'root_access', True)
        await event.answer("✅ Root access enabled")
    elif option == "selinux":
        builder.add_customization('security', 'selinux_permissive', True)
        await event.answer("✅ SELinux set to permissive")
    elif option == "encryption":
        builder.add_customization('security', 'force_encryption', False)
        await event.answer("✅ Encryption disabled")


@BOT.on(events.CallbackQuery(pattern=b"apps_(.*)"))
async def apps_customization(event):
    """Handle apps customization options"""
    option = event.data.decode().split('_', 1)[1]
    user_id = event.sender_id
    builder = BOT._firmware_builders.get(user_id)
    
    if not builder:
        await event.answer("❌ Session expired")
        return
    
    if option == "debloat":
        builder.add_customization('apps', 'remove_bloatware', True)
        await event.answer("✅ Bloatware removal enabled")
    elif option == "custom":
        builder.add_customization('apps', 'add_custom_apps', True)
        await event.answer("✅ Custom apps will be added")
    elif option == "system":
        builder.add_customization('apps', 'system_modifications', True)
        await event.answer("✅ System modifications enabled")


@BOT.on(events.CallbackQuery(pattern=b"back_to_main"))
async def back_to_main_menu(event):
    """Return to main customization menu"""
    buttons = [
        [Button.inline("🎨 UI Customization", b"custom_ui")],
        [Button.inline("⚡ Performance Tweaks", b"custom_performance")],
        [Button.inline("🔒 Security Mods", b"custom_security")],
        [Button.inline("📱 System Apps", b"custom_apps")],
        [Button.inline("🔧 Advanced Options", b"custom_advanced")],
        [Button.inline("✅ Start Building", b"start_build")],
        [Button.inline("❌ Cancel", b"fw_cancel")]
    ]
    
    await event.edit("🛠️ **Customization Options:**\nSelect what you want to customize:", buttons=buttons)

