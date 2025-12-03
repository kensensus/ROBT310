try:
    from telegram import Bot
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    Bot = None  # Define as None to prevent NameError

import asyncio
import json
import os

def load_config():
    """Load Telegram bot configuration"""
    config_path = "telegram_config.json"
    if not os.path.exists(config_path):
        return None
    
    with open(config_path, "r") as f:
        return json.load(f)

def format_attendance_message(name, action, time, confidence):
    """Format attendance message for Telegram"""
    status = "Entry" if action == "Entry" else "Exit"
    return f"Name: {name}\nTime: {time}\nStatus: {status}"

class TelegramNotifier:
    def __init__(self, token, chat_id):
        if not TELEGRAM_AVAILABLE:
            raise ImportError("Telegram module not available")
        self.bot = Bot(token=token)
        self.chat_id = chat_id
    
    def send_sync(self, message):
        """Send message synchronously"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.bot.send_message(chat_id=self.chat_id, text=message))
            loop.close()
        except Exception as e:
            print(f"Failed to send Telegram message: {e}")

def send_attendance_notification(name, action, time, confidence):
    """Send attendance notification via Telegram"""
    if not TELEGRAM_AVAILABLE:
        return
    
    config = load_config()
    if not config or not config.get("enabled", False):
        return
    
    token = config.get("bot_token") or config.get("token")  # Support both key names
    chat_id = config.get("chat_id")
    
    if not token or not chat_id:
        print("⚠️ Telegram bot not configured properly")
        return
    
    try:
        notifier = TelegramNotifier(token, chat_id)
        message = format_attendance_message(name, action, time, confidence)
        notifier.send_sync(message)
    except Exception as e:
        print(f"Error sending Telegram notification: {e}")
