import json
from pathlib import Path
import logging
from datetime import datetime
from typing import List, Set, Dict, Any
import shutil

logger = logging.getLogger('QuantumChat.Utils')

class ChatOrderManager:
    def __init__(self):
        self.order_file = Path('chat_order.json')
        self.order: List[str] = []
        self.favorites: Set[str] = set()
        self.load_order()

    def load_order(self) -> None:
        """Load chat order and favorites from file"""
        try:
            if self.order_file.exists():
                with open(self.order_file, 'r') as f:
                    data = json.load(f)
                    self.order = data.get('order', [])
                    self.favorites = set(data.get('favorites', []))
                logger.info("Chat order loaded successfully")
            else:
                self.save_order()
                
        except Exception as e:
            logger.error(f"Error loading chat order: {str(e)}")
            self.order = []
            self.favorites = set()

    def save_order(self) -> None:
        """Save current chat order and favorites"""
        try:
            with open(self.order_file, 'w') as f:
                json.dump({
                    'order': self.order,
                    'favorites': list(self.favorites),
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
            logger.info("Chat order saved successfully")
        except Exception as e:
            logger.error(f"Error saving chat order: {str(e)}")

    def add_chat(self, chat_id: str) -> None:
        """Add new chat to order"""
        if chat_id not in self.order:
            self.order.insert(0, chat_id)
            self.save_order()

    def remove_chat(self, chat_id: str) -> None:
        """Remove chat from order and favorites"""
        if chat_id in self.order:
            self.order.remove(chat_id)
        if chat_id in self.favorites:
            self.favorites.remove(chat_id)
        self.save_order()

    def toggle_favorite(self, chat_id: str) -> None:
        """Toggle favorite status of chat"""
        if chat_id in self.favorites:
            self.favorites.remove(chat_id)
        else:
            self.favorites.add(chat_id)
        self.save_order()

    def get_ordered_chats(self) -> List[str]:
        """Get chats in order (favorites first)"""
        favorite_chats = [chat_id for chat_id in self.order if chat_id in self.favorites]
        regular_chats = [chat_id for chat_id in self.order if chat_id not in self.favorites]
        return favorite_chats + regular_chats

    def move_chat(self, chat_id: str, direction: str) -> None:
        """Move chat up or down in the order"""
        if chat_id not in self.order:
            return
            
        current_index = self.order.index(chat_id)
        if direction == 'up' and current_index > 0:
            self.order.insert(current_index - 1, self.order.pop(current_index))
            self.save_order()
        elif direction == 'down' and current_index < len(self.order) - 1:
            self.order.insert(current_index + 1, self.order.pop(current_index))
            self.save_order()

class BackupManager:
    def __init__(self, backup_dir: str = 'backups'):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)

    def create_backup(self) -> None:
        """Create backup of all chat data"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"backup_{timestamp}"
            backup_path.mkdir(exist_ok=True)
            
            # Backup chats
            chat_dir = Path('chats')
            if chat_dir.exists():
                shutil.copytree(chat_dir, backup_path / 'chats')
            
            # Backup settings
            settings_file = Path('settings.json')
            if settings_file.exists():
                shutil.copy2(settings_file, backup_path)
            
            # Backup chat order
            order_file = Path('chat_order.json')
            if order_file.exists():
                shutil.copy2(order_file, backup_path)
                
            logger.info(f"Backup created successfully: {backup_path}")
            
        except Exception as e:
            logger.error(f"Error creating backup: {str(e)}")
            raise

    def restore_backup(self, backup_timestamp: str) -> None:
        """Restore from backup"""
        try:
            backup_path = self.backup_dir / f"backup_{backup_timestamp}"
            if not backup_path.exists():
                raise ValueError(f"Backup not found: {backup_timestamp}")
            
            # Restore chats
            chat_dir = Path('chats')
            if (backup_path / 'chats').exists():
                if chat_dir.exists():
                    shutil.rmtree(chat_dir)
                shutil.copytree(backup_path / 'chats', chat_dir)
            
            # Restore settings
            settings_file = backup_path / 'settings.json'
            if settings_file.exists():
                shutil.copy2(settings_file, 'settings.json')
            
            # Restore chat order
            order_file = backup_path / 'chat_order.json'
            if order_file.exists():
                shutil.copy2(order_file, 'chat_order.json')
                
            logger.info(f"Backup restored successfully: {backup_timestamp}")
            
        except Exception as e:
            logger.error(f"Error restoring backup: {str(e)}")
            raise

class Logger:
    """Utility class for logging"""
    
    @staticmethod
    def setup_logging() -> None:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('quantum_chat.log'),
                logging.StreamHandler()
            ]
        )