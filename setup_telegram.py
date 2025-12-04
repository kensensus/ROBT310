import tkinter as tk
from tkinter import messagebox
import json
import os
import sys

# Check if telegram is available AFTER tkinter is loaded
def check_telegram_available():
    try:
        from telegram import Bot
        import asyncio
        return True, Bot, asyncio
    except ImportError:
        return False, None, None

# Hardcoded configuration (no external file needed)
TELEGRAM_CONFIG = {
    "bot_token": "8355843167:AAE_NQLuWdXqQU4TKRqdUUHfBCfvBSxhra4",
    "chat_id": "434909602",
    "enabled": True
}

def save_config_to_file():
    """Save config to JSON file for other modules to use"""
    with open("telegram_config.json", "w") as f:
        json.dump(TELEGRAM_CONFIG, f, indent=2)

def get_config():
    """Return the telegram configuration"""
    return TELEGRAM_CONFIG

async def test_connection(Bot, chat_id, token):
    """Test if Telegram bot is working"""
    try:
        bot = Bot(token=token)
        await bot.send_message(
            chat_id=chat_id,
            text="Telegram Bot Connected!\nFace Attendance System is ready."
        )
        return True, "Test message sent successfully!"
    except Exception as e:
        return False, str(e)

def test_telegram_connection():
    """Test connection and show result"""
    TELEGRAM_AVAILABLE, Bot, asyncio = check_telegram_available()
    
    if not TELEGRAM_AVAILABLE:
        messagebox.showerror("Error", "python-telegram-bot not installed!\n\nRun in terminal:\nsource ~/face_attendance_env/bin/activate\npip3 install python-telegram-bot")
        return
    
    # Save config first
    save_config_to_file()
    
    success, message = asyncio.run(test_connection(Bot, TELEGRAM_CONFIG["chat_id"], TELEGRAM_CONFIG["bot_token"]))
    
    if success:
        messagebox.showinfo("Success", f"{message}\n\nCheck your Telegram for the test message.")
    else:
        messagebox.showerror("Error", f"Connection failed:\n{message}")

def disable_telegram():
    """Disable Telegram notifications"""
    TELEGRAM_CONFIG["enabled"] = False
    save_config_to_file()
    messagebox.showinfo("Success", "Telegram notifications disabled")

def enable_telegram():
    """Enable Telegram notifications"""
    TELEGRAM_CONFIG["enabled"] = True
    save_config_to_file()
    messagebox.showinfo("Success", "Telegram notifications enabled")

def main():
    # Check telegram availability
    TELEGRAM_AVAILABLE, Bot, asyncio = check_telegram_available()
    
    root = tk.Tk()
    root.title("Telegram Bot Configuration")
    root.attributes('-fullscreen', True)
    root.configure(bg="#1e1e1e")
    root.bind('<Escape>', lambda e: root.destroy())
    
    # Title
    tk.Label(root, text="Telegram Bot Configuration", font=("Arial", 24, "bold"),
             bg="#1e1e1e", fg="white").pack(pady=30)
    
    if not TELEGRAM_AVAILABLE:
        tk.Label(root, text="Telegram Module Not Available", 
                font=("Arial", 20, "bold"),
                bg="#1e1e1e", fg="#ff0000").pack(pady=30)
        
        tk.Label(root, text="Please run in terminal:", 
                font=("Arial", 14, "bold"),
                bg="#1e1e1e", fg="#aaaaaa").pack(pady=10)
        
        tk.Label(root, text="source ~/face_attendance_env/bin/activate", 
                font=("Arial", 12),
                bg="#1e1e1e", fg="#00ff00").pack(pady=5)
        
        tk.Label(root, text="pip3 install python-telegram-bot", 
                font=("Arial", 12),
                bg="#1e1e1e", fg="#00ff00").pack(pady=5)
        
        tk.Button(root, text="Close", font=("Arial", 14), width=15,
                 bg="#f44336", fg="white",
                 command=root.destroy).pack(pady=30)
        root.mainloop()
        return
    
    # Configuration info
    info_frame = tk.Frame(root, bg="#2e2e2e", relief=tk.RAISED, bd=2)
    info_frame.pack(pady=20, padx=50, fill=tk.X)
    
    tk.Label(info_frame, text="Current Configuration", font=("Arial", 16, "bold"),
             bg="#2e2e2e", fg="white").pack(pady=10)
    
    tk.Label(info_frame, text=f"Bot Token: {TELEGRAM_CONFIG['bot_token'][:20]}...", 
             font=("Arial", 12),
             bg="#2e2e2e", fg="#aaaaaa").pack(pady=5)
    
    tk.Label(info_frame, text=f"Chat ID: {TELEGRAM_CONFIG['chat_id']}", 
             font=("Arial", 12),
             bg="#2e2e2e", fg="#aaaaaa").pack(pady=5)
    
    status_text = "Enabled" if TELEGRAM_CONFIG['enabled'] else "Disabled"
    tk.Label(info_frame, text=f"Status: {status_text}", 
             font=("Arial", 14, "bold"),
             bg="#2e2e2e", fg="#00ff00" if TELEGRAM_CONFIG['enabled'] else "#ff0000").pack(pady=10)
    
    # Buttons
    btn_frame = tk.Frame(root, bg="#1e1e1e")
    btn_frame.pack(pady=30)
    
    tk.Button(btn_frame, text="Test Connection", font=("Arial", 14), width=18,
              bg="#4CAF50", fg="white",
              command=test_telegram_connection).grid(row=0, column=0, padx=10, pady=10)
    
    tk.Button(btn_frame, text="Enable Notifications", font=("Arial", 14), width=18,
              bg="#2196F3", fg="white",
              command=enable_telegram).grid(row=0, column=1, padx=10, pady=10)
    
    tk.Button(btn_frame, text="Disable Notifications", font=("Arial", 14), width=18,
              bg="#FF9800", fg="white",
              command=disable_telegram).grid(row=1, column=0, padx=10, pady=10)
    
    tk.Button(btn_frame, text="Close", font=("Arial", 14), width=18,
              bg="#f44336", fg="white",
              command=root.destroy).grid(row=1, column=1, padx=10, pady=10)
    
    # Instructions at bottom
    tk.Label(root, text="To change bot token or chat ID, edit setup_telegram.py", 
             font=("Arial", 10),
             bg="#1e1e1e", fg="#888888").pack(side=tk.BOTTOM, pady=10)
    
    # Save config on startup
    save_config_to_file()
    
    root.mainloop()

if __name__ == "__main__":
    main()
