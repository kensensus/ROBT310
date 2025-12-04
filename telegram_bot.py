try:
    from telegram import Bot
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    Bot = None

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
        """Send message synchronously with proper event loop handling"""
        try:
            # Try to get the current event loop
            try:
                loop = asyncio.get_running_loop()
                # If we're already in an event loop, create a new thread
                import threading
                result = {'success': False, 'error': None}
                
                def run_in_thread():
                    try:
                        new_loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(new_loop)
                        new_loop.run_until_complete(
                            self.bot.send_message(chat_id=self.chat_id, text=message)
                        )
                        new_loop.close()
                        result['success'] = True
                    except Exception as e:
                        result['error'] = e
                
                thread = threading.Thread(target=run_in_thread)
                thread.start()
                thread.join(timeout=10)  # 10 second timeout
                
                if not result['success'] and result['error']:
                    raise result['error']
                    
            except RuntimeError:
                # No event loop running, create a new one
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(
                        self.bot.send_message(chat_id=self.chat_id, text=message)
                    )
                finally:
                    loop.close()
                    # Important: Clear the event loop to prevent conflicts
                    asyncio.set_event_loop(None)
                    
            print(f"[TELEGRAM] Message sent successfully: {message[:50]}...")
            
        except Exception as e:
            print(f"[TELEGRAM ERROR] Failed to send message: {e}")
            import traceback
            traceback.print_exc()

def send_attendance_notification(name, action, time, confidence):
    """Send attendance notification via Telegram"""
    if not TELEGRAM_AVAILABLE:
        print("[TELEGRAM] Module not available")
        return
    
    config = load_config()
    if not config or not config.get("enabled", False):
        print("[TELEGRAM] Not enabled in config")
        return
    
    token = config.get("bot_token") or config.get("token")
    chat_id = config.get("chat_id")
    
    if not token or not chat_id:
        print("[TELEGRAM] Bot not configured properly")
        return
    
    try:
        notifier = TelegramNotifier(token, chat_id)
        message = format_attendance_message(name, action, time, confidence)
        notifier.send_sync(message)
    except Exception as e:
        print(f"[TELEGRAM ERROR] Error sending notification: {e}")
        import traceback
        traceback.print_exc()
