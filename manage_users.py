import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import json
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

def load_users():
    """Load unique user names from dataset folder"""
    if not os.path.exists(DATASET_DIR):
        return []
    
    users = set()
    for filename in os.listdir(DATASET_DIR):
        if filename.lower().endswith(('.jpg', '.png', '.jpeg')) and '_' in filename:
            name = filename.split('_')[0]
            users.add(name)
    
    return sorted(list(users))

def delete_user(name, user_listbox, root):
    """Delete all images of a user from dataset"""
    if not messagebox.askyesno("Confirm Delete", f"Delete all data for '{name}'?\nThis cannot be undone."):
        return
    
    deleted_count = 0
    for filename in os.listdir(DATASET_DIR):
        if filename.startswith(f"{name}_"):
            try:
                os.remove(os.path.join(DATASET_DIR, filename))
                deleted_count += 1
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete {filename}:\n{e}")
    
    messagebox.showinfo("Success", f"Deleted {deleted_count} images for '{name}'.\nPlease retrain the system.")
    refresh_list(user_listbox)

def rename_user(old_name, user_listbox, root):
    """Rename a user by renaming all their image files"""
    new_name = simpledialog.askstring("Rename User", f"Enter new name for '{old_name}':")
    
    if not new_name or not new_name.strip():
        return
    
    new_name = new_name.strip()
    
    if new_name == old_name:
        return
    
    # Check if new name already exists
    existing_users = load_users()
    if new_name in existing_users:
        messagebox.showerror("Error", f"User '{new_name}' already exists!")
        return
    
    renamed_count = 0
    for filename in os.listdir(DATASET_DIR):
        if filename.startswith(f"{old_name}_"):
            try:
                old_path = os.path.join(DATASET_DIR, filename)
                # Extract the number part after underscore
                parts = filename.split('_', 1)
                if len(parts) == 2:
                    new_filename = f"{new_name}_{parts[1]}"
                    new_path = os.path.join(DATASET_DIR, new_filename)
                    os.rename(old_path, new_path)
                    renamed_count += 1
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rename {filename}:\n{e}")
    
    messagebox.showinfo("Success", f"Renamed {renamed_count} images.\nPlease retrain the system.")
    refresh_list(user_listbox)

def refresh_list(user_listbox):
    """Refresh the user list"""
    user_listbox.delete(0, tk.END)
    users = load_users()
    
    if not users:
        user_listbox.insert(tk.END, "No users found")
    else:
        for user in users:
            user_listbox.insert(tk.END, user)

def main():
    root = tk.Tk()
    root.title("Manage Users")
    root.attributes('-fullscreen', True)
    root.configure(bg="#1e1e1e")
    
    # Bind ESC to exit fullscreen
    root.bind('<Escape>', lambda e: root.attributes('-fullscreen', False))
    
    # Main container with padding
    main_frame = tk.Frame(root, bg="#1e1e1e")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    # Title
    title = tk.Label(main_frame, text="Manage Enrolled Users",
                     font=("Arial", 18, "bold"), bg="#1e1e1e", fg="white")
    title.pack(pady=10)
    
    # Listbox frame (takes most of the space)
    list_frame = tk.Frame(main_frame, bg="#1e1e1e")
    list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    user_listbox = tk.Listbox(list_frame, font=("Arial", 14),
                               bg="#2e2e2e", fg="white",
                               selectmode=tk.SINGLE,
                               yscrollcommand=scrollbar.set,
                               height=15)
    user_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=user_listbox.yview)
    
    # Load initial users
    refresh_list(user_listbox)
    
    # Button frame at bottom (compact layout)
    button_frame = tk.Frame(main_frame, bg="#1e1e1e")
    button_frame.pack(fill=tk.X, pady=5)
    
    # Action buttons in a grid for better space usage
    btn_delete = tk.Button(button_frame, text="Delete User",
                          font=("Arial", 12), width=15,
                          command=lambda: delete_user(
                              user_listbox.get(tk.ACTIVE), user_listbox, root
                          ) if user_listbox.curselection() else messagebox.showwarning("No Selection", "Please select a user first."),
                          bg="#f44336", fg="white")
    btn_delete.grid(row=0, column=0, padx=5, pady=5)
    
    btn_rename = tk.Button(button_frame, text="Rename User",
                          font=("Arial", 12), width=15,
                          command=lambda: rename_user(
                              user_listbox.get(tk.ACTIVE), user_listbox, root
                          ) if user_listbox.curselection() else messagebox.showwarning("No Selection", "Please select a user first."),
                          bg="#2196F3", fg="white")
    btn_rename.grid(row=0, column=1, padx=5, pady=5)
    
    btn_refresh = tk.Button(button_frame, text="Refresh List",
                           font=("Arial", 12), width=15,
                           command=lambda: refresh_list(user_listbox),
                           bg="#4CAF50", fg="white")
    btn_refresh.grid(row=0, column=2, padx=5, pady=5)
    
    btn_close = tk.Button(button_frame, text="Close",
                         font=("Arial", 12), width=15,
                         command=root.destroy,
                         bg="#607D8B", fg="white")
    btn_close.grid(row=0, column=3, padx=5, pady=5)
    
    # Center the buttons
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)
    button_frame.grid_columnconfigure(2, weight=1)
    button_frame.grid_columnconfigure(3, weight=1)
    
    root.mainloop()

if __name__ == "__main__":
    main()
