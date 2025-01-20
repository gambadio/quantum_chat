import json
from pathlib import Path
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger('QuantumChat.Settings')

class Settings:
    SETTINGS_FILE = 'settings.json'
    
    DEFAULT_SETTINGS = {
        'api_url': "http://localhost:11434/v1",
        'model_settings': {
            'model': 'qwen2.5:14b',
            'temperature': 0.7,
            'max_tokens': 2000,
            'top_p': 0.9,
            'frequency_penalty': 0.0,
            'presence_penalty': 0.0
        },
        'chat_display': {
            'message_spacing': 20,
            'max_width': 800,
            'animate_messages': True,
            'show_timestamps': True,
            'compact_mode': False
        },
        'memory_settings': {
            'buffer_size': 8,
            'summary_enabled': True,
            'summary_interval': 10
        },
        'ui_settings': {
            'font_size': 13,
            'show_avatars': True,
            'theme': 'cyberpunk',
            'custom_css': ''
        },
        'backup_settings': {
            'auto_backup': True,
            'backup_interval': 30,  # minutes
            'max_backups': 5
        }
    }

    @classmethod
    def load_settings(cls) -> Dict[str, Any]:
        """Load settings from file or create default"""
        settings_path = Path(cls.SETTINGS_FILE)
        try:
            if settings_path.exists():
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                    # Update with any missing default settings
                    cls._update_missing_settings(settings)
                    logger.info("Settings loaded successfully")
                    return settings
            else:
                logger.info("No settings file found, creating default settings")
                cls.save_settings(cls.DEFAULT_SETTINGS)
                return cls.DEFAULT_SETTINGS
                
        except Exception as e:
            logger.error(f"Error loading settings: {str(e)}")
            return cls.DEFAULT_SETTINGS

    @classmethod
    def save_settings(cls, settings: Dict[str, Any]) -> None:
        """Save settings to file with backup"""
        try:
            # Create backup of existing settings
            settings_path = Path(cls.SETTINGS_FILE)
            if settings_path.exists():
                backup_path = settings_path.with_suffix(
                    f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                )
                settings_path.rename(backup_path)
            
            # Save new settings
            with open(cls.SETTINGS_FILE, 'w') as f:
                json.dump(settings, f, indent=2)
            
            logger.info("Settings saved successfully")
            
            # Clean up old backups
            cls._cleanup_backups()
            
        except Exception as e:
            logger.error(f"Error saving settings: {str(e)}")
            raise Exception(f"Failed to save settings: {str(e)}")

    @classmethod
    def _update_missing_settings(cls, settings: Dict[str, Any]) -> None:
        """Recursively update settings with missing default values"""
        for key, default_value in cls.DEFAULT_SETTINGS.items():
            if key not in settings:
                settings[key] = default_value
            elif isinstance(default_value, dict):
                if not isinstance(settings[key], dict):
                    settings[key] = {}
                cls._update_missing_settings(settings[key])

    @classmethod
    def _cleanup_backups(cls) -> None:
        """Clean up old backup files"""
        try:
            backup_files = sorted(
                Path().glob(f'{cls.SETTINGS_FILE}.backup_*.json'),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            
            # Keep only the 5 most recent backups
            for backup_file in backup_files[5:]:
                backup_file.unlink()
                
        except Exception as e:
            logger.error(f"Error cleaning up backup files: {str(e)}")

    @classmethod
    def validate_settings(cls, settings: Dict[str, Any]) -> bool:
        """Validate settings structure and values"""
        try:
            required_keys = [
                'api_url',
                'model_settings',
                'chat_display',
                'memory_settings',
                'ui_settings'
            ]
            
            # Check required keys
            for key in required_keys:
                if key not in settings:
                    logger.error(f"Missing required setting: {key}")
                    return False
            
            # Validate model settings
            model_settings = settings['model_settings']
            if not isinstance(model_settings.get('temperature'), (int, float)):
                logger.error("Invalid temperature value")
                return False
            
            if not isinstance(model_settings.get('max_tokens'), int):
                logger.error("Invalid max_tokens value")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating settings: {str(e)}")
            return False