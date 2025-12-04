import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

# Project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_script(script_name):
    script_path = os.path.join(BASE_DIR, script_name)

    if not os.path.exists(script_path):
        messagebox.showerror("Error", f"Script not found:\n{script_path}")
        return

    try:
        # Hide main window
        root.withdraw()
        
        # Use run_with_venv.sh to ensure virtual environment is active
        venv_script = os.path.join(BASE_DIR, "run_with_venv.sh")
        if os.path.exists(venv_script):
            subprocess.run(["bash", venv_script, script_path], check=True)
        else:
            # Fallback to direct execution
            subprocess.run([sys.executable, script_path], check=True)
        
        # Show main window again
        root.deiconify()
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Script failed with error code {e.returncode}")
        root.deiconify()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run script:\n{e}")
        root.deiconify()

def enroll_user():
    run_script("collect_faces.py")

def train_system():
    run_script("train_lbph.py")

def start_attendance():
    run_script("recognize_attendance.py")

def manage_users():
    run_script("manage_users.py")

def setup_telegram():
    run_script("setup_telegram.py")

def exit_application(root):
    """Properly exit the application with confirmation"""
    if messagebox.askyesno("Exit", "Are you sure you want to exit the Face Attendance System?"):
        print("Exiting Face Attendance System...")
        root.destroy()
        sys.exit(0)

def main():
    global root
    root = tk.Tk()
    root.title("Face Attendance System")
    root.attributes('-fullscreen', True)  # Fullscreen mode
    root.configure(bg="#1e1e1e")
    
    # Bind ESC to exit fullscreen
    root.bind('<Escape>', lambda e: root.attributes('-fullscreen', False))

    title = tk.Label(root, text="Face Attendance System",
                     font=("Arial", 20, "bold"), bg="#1e1e1e", fg="white")
    title.pack(pady=15)

    btn_manage = tk.Button(root, text="Manage Users",
                          font=("Arial", 14), width=20, height=2,
                          command=manage_users, bg="#9C27B0", fg="white")
    btn_manage.pack(pady=6)

    btn_enroll = tk.Button(root, text="Enroll New User",
                           font=("Arial", 14), width=20, height=2,
                           command=enroll_user, bg="#4CAF50", fg="white")
    btn_enroll.pack(pady=6)

    btn_train = tk.Button(root, text="Train System",
                          font=("Arial", 14), width=20, height=2,
                          command=train_system, bg="#2196F3", fg="white")
    btn_train.pack(pady=6)

    btn_attendance = tk.Button(root, text="Start Attendance",
                               font=("Arial", 14), width=20, height=2,
                               command=start_attendance, bg="#FF5722", fg="white")
    btn_attendance.pack(pady=6)
    
    btn_telegram = tk.Button(root, text="Setup Telegram Bot",
                            font=("Arial", 14), width=20, height=2,
                            command=setup_telegram, bg="#0088cc", fg="white")
    btn_telegram.pack(pady=6)
    
    btn_exit = tk.Button(root, text="Exit",
                        font=("Arial", 14), width=15, height=2,
                        command=lambda: exit_application(root), bg="#f44336", fg="white")
    btn_exit.pack(pady=15)

    root.mainloop()

if __name__ == "__main__":
    main()

import tkinter as tk
import subprocess
import sys
import os

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Attendance System")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#1e1e1e")
        
        # Bind ESC to exit
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        
        # Title
        title = tk.Label(root, text="Face Attendance System",
                        font=("Arial", 24, "bold"), bg="#1e1e1e", fg="white")
        title.pack(pady=40)
        
        # Button frame
        btn_frame = tk.Frame(root, bg="#1e1e1e")
        btn_frame.pack(expand=True)
        
        buttons = [
            ("Collect Faces", "collect_faces.py", "#4CAF50"),
            ("Train System", "train_lbph.py", "#2196F3"),
            ("Mark Attendance", "recognize_attendance.py", "#FF9800"),
            ("Manage Users", "manage_users.py", "#9C27B0"),
            ("Setup Telegram", "setup_telegram.py", "#00BCD4"),
            ("Exit", None, "#f44336")
        ]
        
        for text, script, color in buttons:
            btn = tk.Button(btn_frame, text=text, font=("Arial", 16),
                           width=20, height=2, bg=color, fg="white",
                           command=lambda s=script: self.run_script(s))
            btn.pack(pady=10)
    
    def run_script(self, script):
        if script is None:
            self.root.destroy()
            return
        
        self.root.destroy()
        subprocess.run([sys.executable, script])

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()
