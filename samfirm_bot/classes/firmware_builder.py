""" Samsung Firmware Builder Class """

import os
import asyncio
import tempfile
import zipfile
import shutil
import hashlib
import json
from pathlib import Path
from datetime import datetime
import subprocess
import xml.etree.ElementTree as ET

from samfirm_bot import TG_LOGGER


class FirmwareBuilder:
    """Samsung Custom Firmware Builder"""
    
    def __init__(self, model, csc, region):
        self.model = model
        self.csc = csc
        self.region = region
        self.customizations = {
            'ui': {},
            'performance': {},
            'security': {},
            'apps': {},
            'advanced': {}
        }
        self.build_id = self._generate_build_id()
        self.temp_dir = None
        
    def _generate_build_id(self):
        """Generate unique build ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        device_hash = hashlib.md5(f"{self.model}_{self.csc}_{self.region}".encode()).hexdigest()[:8]
        return f"{timestamp}_{device_hash}"
    
    def add_customization(self, category, option, value):
        """Add customization option"""
        if category in self.customizations:
            self.customizations[category][option] = value
            TG_LOGGER.info(f"Added customization: {category}.{option} = {value}")
    
    def get_build_id(self):
        """Get build ID"""
        return self.build_id
    
    async def build_firmware(self, progress_callback=None):
        """Build custom firmware"""
        try:
            # Create temporary directory
            self.temp_dir = tempfile.mkdtemp(prefix=f"firmware_build_{self.build_id}_")
            TG_LOGGER.info(f"Created temp directory: {self.temp_dir}")
            
            if progress_callback:
                await progress_callback("Initializing build environment", 5)
            
            # Step 1: Download base firmware
            base_firmware_path = await self._download_base_firmware()
            if not base_firmware_path:
                raise Exception("Failed to download base firmware")
            
            if progress_callback:
                await progress_callback("Base firmware downloaded", 15)
            
            # Step 2: Extract firmware
            extracted_path = await self._extract_firmware(base_firmware_path)
            if progress_callback:
                await progress_callback("Firmware extracted", 25)
            
            # Step 3: Apply customizations
            await self._apply_customizations(extracted_path, progress_callback)
            
            # Step 4: Build custom firmware
            if progress_callback:
                await progress_callback("Building custom firmware", 80)
            
            custom_firmware_path = await self._build_custom_firmware(extracted_path)
            
            if progress_callback:
                await progress_callback("Firmware build completed", 100)
            
            return custom_firmware_path
            
        except Exception as e:
            TG_LOGGER.error(f"Build error: {e}")
            raise e
        finally:
            # Cleanup temp directory
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    async def _download_base_firmware(self):
        """Download base firmware for the device"""
        TG_LOGGER.info(f"Downloading base firmware for {self.model}")
        
        # In a real implementation, this would download from Samsung servers
        # For demo purposes, we'll create a mock firmware structure
        base_fw_dir = os.path.join(self.temp_dir, "base_firmware")
        os.makedirs(base_fw_dir, exist_ok=True)
        
        # Create mock firmware files
        mock_files = [
            "AP_G973FXXU3ASL2_G973FOXM3ASL2_MQB63658442_REV00_user_low_ship_MULTI_CERT.tar.md5",
            "BL_G973FXXU3ASL2_G973FOXM3ASL2_MQB63658442_REV00_user_low_ship_MULTI_CERT.tar.md5",
            "CP_G973FXXU3ASL2_G973FOXM3ASL2_MQB63658442_REV00_user_low_ship_MULTI_CERT.tar.md5",
            "CSC_OXM_G973FOXM3ASL2_MQB63658442_REV00_user_low_ship_MULTI_CERT.tar.md5"
        ]
        
        for filename in mock_files:
            file_path = os.path.join(base_fw_dir, filename)
            with open(file_path, 'w') as f:
                f.write(f"# Mock firmware file for {self.model}\n")
                f.write(f"# Build ID: {self.build_id}\n")
                f.write("# This is a demonstration file\n")
        
        return base_fw_dir
    
    async def _extract_firmware(self, firmware_path):
        """Extract firmware files"""
        TG_LOGGER.info("Extracting firmware files")
        
        extracted_dir = os.path.join(self.temp_dir, "extracted")
        os.makedirs(extracted_dir, exist_ok=True)
        
        # Create directory structure for extracted firmware
        dirs_to_create = [
            "system", "vendor", "boot", "recovery", "modem", "bootloader"
        ]
        
        for dir_name in dirs_to_create:
            os.makedirs(os.path.join(extracted_dir, dir_name), exist_ok=True)
        
        # Create mock extracted files
        mock_extracted_files = {
            "system/build.prop": self._generate_build_prop(),
            "system/framework/framework-res.apk": "# Mock framework file",
            "boot/boot.img": "# Mock boot image",
            "recovery/recovery.img": "# Mock recovery image",
            "vendor/build.prop": "# Mock vendor build.prop",
            "modem/modem.bin": "# Mock modem binary"
        }
        
        for file_path, content in mock_extracted_files.items():
            full_path = os.path.join(extracted_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)
        
        return extracted_dir
    
    async def _apply_customizations(self, extracted_path, progress_callback=None):
        """Apply user customizations to firmware"""
        TG_LOGGER.info("Applying customizations")
        
        progress_step = 30
        total_categories = len([cat for cat in self.customizations.values() if cat])
        step_increment = 45 / max(total_categories, 1)
        
        # Apply UI customizations
        if self.customizations['ui']:
            await self._apply_ui_customizations(extracted_path)
            progress_step += step_increment
            if progress_callback:
                await progress_callback("Applied UI customizations", int(progress_step))
        
        # Apply performance customizations
        if self.customizations['performance']:
            await self._apply_performance_customizations(extracted_path)
            progress_step += step_increment
            if progress_callback:
                await progress_callback("Applied performance tweaks", int(progress_step))
        
        # Apply security customizations
        if self.customizations['security']:
            await self._apply_security_customizations(extracted_path)
            progress_step += step_increment
            if progress_callback:
                await progress_callback("Applied security modifications", int(progress_step))
        
        # Apply app customizations
        if self.customizations['apps']:
            await self._apply_app_customizations(extracted_path)
            progress_step += step_increment
            if progress_callback:
                await progress_callback("Applied app modifications", int(progress_step))
        
        # Apply advanced customizations
        if self.customizations['advanced']:
            await self._apply_advanced_customizations(extracted_path)
            progress_step += step_increment
            if progress_callback:
                await progress_callback("Applied advanced modifications", int(progress_step))
    
    async def _apply_ui_customizations(self, extracted_path):
        """Apply UI customizations"""
        TG_LOGGER.info("Applying UI customizations")
        
        build_prop_path = os.path.join(extracted_path, "system", "build.prop")
        
        ui_mods = []
        if self.customizations['ui'].get('dark_theme'):
            ui_mods.append("# Dark theme enabled")
            ui_mods.append("ro.config.ui_night_mode=2")
        
        if self.customizations['ui'].get('custom_icons'):
            ui_mods.append("# Custom icons enabled")
            ui_mods.append("ro.config.custom_icons=1")
        
        if self.customizations['ui'].get('scaling'):
            ui_mods.append("# UI scaling optimized")
            ui_mods.append("ro.sf.lcd_density=420")
        
        if ui_mods:
            with open(build_prop_path, 'a') as f:
                f.write("\n# UI Customizations\n")
                f.write("\n".join(ui_mods))
                f.write("\n")
    
    async def _apply_performance_customizations(self, extracted_path):
        """Apply performance customizations"""
        TG_LOGGER.info("Applying performance customizations")
        
        build_prop_path = os.path.join(extracted_path, "system", "build.prop")
        
        perf_mods = []
        if self.customizations['performance'].get('cpu_overclock'):
            perf_mods.append("# CPU overclock enabled")
            perf_mods.append("ro.config.cpu_overclock=1")
        
        if self.customizations['performance'].get('battery_optimization'):
            perf_mods.append("# Battery optimization enabled")
            perf_mods.append("ro.config.low_power_mode=1")
            perf_mods.append("pm.sleep_mode=1")
        
        if self.customizations['performance'].get('ram_management'):
            perf_mods.append("# Aggressive RAM management")
            perf_mods.append("ro.config.low_ram=false")
            perf_mods.append("ro.config.max_starting_bg=8")
        
        if perf_mods:
            with open(build_prop_path, 'a') as f:
                f.write("\n# Performance Customizations\n")
                f.write("\n".join(perf_mods))
                f.write("\n")
    
    async def _apply_security_customizations(self, extracted_path):
        """Apply security customizations"""
        TG_LOGGER.info("Applying security customizations")
        
        build_prop_path = os.path.join(extracted_path, "system", "build.prop")
        
        sec_mods = []
        if self.customizations['security'].get('root_access'):
            sec_mods.append("# Root access enabled")
            sec_mods.append("ro.debuggable=1")
            sec_mods.append("ro.secure=0")
        
        if self.customizations['security'].get('selinux_permissive'):
            sec_mods.append("# SELinux permissive mode")
            sec_mods.append("ro.boot.selinux=permissive")
        
        if not self.customizations['security'].get('force_encryption', True):
            sec_mods.append("# Encryption disabled")
            sec_mods.append("ro.crypto.state=unencrypted")
        
        if sec_mods:
            with open(build_prop_path, 'a') as f:
                f.write("\n# Security Customizations\n")
                f.write("\n".join(sec_mods))
                f.write("\n")
    
    async def _apply_app_customizations(self, extracted_path):
        """Apply app customizations"""
        TG_LOGGER.info("Applying app customizations")
        
        if self.customizations['apps'].get('remove_bloatware'):
            # Create list of bloatware to remove
            bloatware_list = [
                "Facebook", "Instagram", "WhatsApp", "Netflix", 
                "Spotify", "Microsoft", "Google", "Samsung"
            ]
            
            bloatware_file = os.path.join(extracted_path, "system", "remove_bloatware.txt")
            with open(bloatware_file, 'w') as f:
                f.write("# Bloatware removal list\n")
                f.write("\n".join(bloatware_list))
        
        if self.customizations['apps'].get('add_custom_apps'):
            custom_apps_dir = os.path.join(extracted_path, "system", "custom_apps")
            os.makedirs(custom_apps_dir, exist_ok=True)
            
            # Create placeholder for custom apps
            with open(os.path.join(custom_apps_dir, "custom_apps.txt"), 'w') as f:
                f.write("# Custom apps will be installed here\n")
    
    async def _apply_advanced_customizations(self, extracted_path):
        """Apply advanced customizations"""
        TG_LOGGER.info("Applying advanced customizations")
        
        build_prop_path = os.path.join(extracted_path, "system", "build.prop")
        
        advanced_mods = []
        if self.customizations['advanced'].get('buildprop'):
            advanced_mods.append("# Advanced build.prop modifications")
            advanced_mods.append("ro.config.advanced_tweaks=1")
        
        if self.customizations['advanced'].get('filesystem'):
            advanced_mods.append("# File system tweaks")
            advanced_mods.append("ro.config.fs_tweaks=1")
        
        if self.customizations['advanced'].get('network'):
            advanced_mods.append("# Network optimizations")
            advanced_mods.append("net.tcp_buffersize.default=4096,87380,256960,4096,16384,256960")
        
        if advanced_mods:
            with open(build_prop_path, 'a') as f:
                f.write("\n# Advanced Customizations\n")
                f.write("\n".join(advanced_mods))
                f.write("\n")
    
    async def _build_custom_firmware(self, extracted_path):
        """Build the final custom firmware"""
        TG_LOGGER.info("Building custom firmware package")
        
        # Create output directory
        output_dir = os.path.join(self.temp_dir, "output")
        os.makedirs(output_dir, exist_ok=True)
        
        # Create firmware package
        firmware_filename = f"Custom_{self.model}_{self.build_id}.zip"
        firmware_path = os.path.join(output_dir, firmware_filename)
        
        # Create ZIP package
        with zipfile.ZipFile(firmware_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all extracted files to ZIP
            for root, dirs, files in os.walk(extracted_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, extracted_path)
                    zipf.write(file_path, arcname)
            
            # Add build info
            build_info = {
                "model": self.model,
                "csc": self.csc,
                "region": self.region,
                "build_id": self.build_id,
                "build_date": datetime.now().isoformat(),
                "customizations": self.customizations,
                "version": "1.0.0",
                "builder": "Samsung Custom Firmware Bot"
            }
            
            zipf.writestr("build_info.json", json.dumps(build_info, indent=2))
            
            # Add installation instructions
            install_instructions = self._generate_install_instructions()
            zipf.writestr("INSTALL.txt", install_instructions)
        
        TG_LOGGER.info(f"Custom firmware created: {firmware_path}")
        return firmware_path
    
    def _generate_build_prop(self):
        """Generate base build.prop content"""
        return f"""# Build Properties for {self.model}
ro.build.id={self.build_id}
ro.build.display.id=Custom-{self.build_id}
ro.build.version.incremental={self.build_id}
ro.build.version.sdk=30
ro.build.version.release=11
ro.build.date={datetime.now().strftime('%a %b %d %H:%M:%S UTC %Y')}
ro.build.type=user
ro.build.user=builder
ro.build.host=custom-firmware-bot
ro.product.model={self.model}
ro.product.brand=samsung
ro.product.name={self.model.lower()}
ro.product.device={self.model.lower()}
ro.product.board=universal9820
ro.product.manufacturer=samsung
ro.product.locale=en-US
ro.wifi.channels=
ro.board.platform=exynos9820
ro.build.product={self.model.lower()}
ro.build.description={self.model}-user 11 {self.build_id} release-keys
ro.build.fingerprint=samsung/{self.model.lower()}/{self.model.lower()}:11/{self.build_id}:user/release-keys
ro.build.characteristics=default
ro.build.tags=release-keys
ro.build.version.all_codenames=REL
ro.build.version.codename=REL
ro.build.version.release_or_codename=11
"""
    
    def _generate_install_instructions(self):
        """Generate installation instructions"""
        return f"""Samsung Custom Firmware Installation Instructions
=================================================

Device: {self.model}
Build: {self.build_id}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

IMPORTANT WARNINGS:
- This is custom firmware. Flashing may void your warranty.
- Ensure your device bootloader is unlocked.
- Make a complete backup before proceeding.
- Flash at your own risk!

REQUIREMENTS:
- Odin (Windows) or Heimdall (Linux/Mac)
- USB drivers for your device
- Device in Download Mode

INSTALLATION STEPS:
1. Extract this ZIP file
2. Boot your device into Download Mode:
   - Power off device
   - Hold Volume Down + Bixby + Power
   - Press Volume Up when prompted
3. Connect device to PC via USB
4. Open Odin
5. Load firmware files:
   - AP: Load AP file
   - BL: Load BL file  
   - CP: Load CP file
   - CSC: Load CSC file
6. Click START to flash
7. Device will reboot automatically

CUSTOMIZATIONS APPLIED:
{self._format_customizations()}

TROUBLESHOOTING:
- If device doesn't boot, try flashing stock firmware
- For bootloop, wipe data in recovery mode
- Join our Telegram group for support

Enjoy your custom firmware!
"""
    
    def _format_customizations(self):
        """Format customizations for display"""
        formatted = []
        for category, options in self.customizations.items():
            if options:
                formatted.append(f"\n{category.upper()}:")
                for option, value in options.items():
                    formatted.append(f"  - {option}: {value}")
        return "\n".join(formatted) if formatted else "  - No customizations applied"

