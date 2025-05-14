from customtkinter import *
from PIL import Image
import sqlite3
import os

app = CTk(fg_color="#e3e3e3")

def initialize_database():
    if not os.path.exists('data'):
        os.makedirs('data')
    
    conn = sqlite3.connect('data/password_manager.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

initialize_database()

set_appearance_mode("dark")
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

main_width = 900
main_height = 500

center_width = int(screen_width / 2 - main_width / 2)
center_height = int(screen_height / 2 - main_height / 2)

app.geometry(f"{main_width}x{main_height}+{center_width}+{center_height}")
app.title("Password Manager")
app.resizable(False, False)

searchVault = CTkFrame(app, width=300, height=40, corner_radius=0)
searchVault.grid(row=0, column=0, sticky="nsew")

def on_search_change(*args):
    search_term = inputVault.get().lower()
    refresh_accounts_list(search_term)

inputVault = CTkEntry(searchVault,placeholder_text="Search Vault",width=250,height=40,border_color="#c9c9c9",border_width=1)
inputVault.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
inputVault.bind("<KeyRelease>", on_search_change)

def refresh_accounts_list(search_term=None):
    for widget in leftSideFrame.winfo_children():
        widget.destroy()
    
    conn = sqlite3.connect('data/password_manager.db')
    cursor = conn.cursor()
    
    if search_term:
        cursor.execute(
            "SELECT id, url, username FROM accounts WHERE url LIKE ? OR username LIKE ? ORDER BY created_at DESC",
            (f"%{search_term}%", f"%{search_term}%"))
    else:
        cursor.execute("SELECT id, url, username FROM accounts ORDER BY created_at DESC")
    
    accounts = cursor.fetchall()
    conn.close()
    
    for index, account in enumerate(accounts):
        account_id, url, username = account
        create_clickable_item(leftSideFrame,icon_path=os.path.join(os.getcwd(), "url_default.png"),title=url,subtitle=username,index=index,account_id=account_id)
    
    blankFrame = CTkFrame(leftSideFrame, width=599, height=40, fg_color="transparent", corner_radius=0)
    blankFrame.grid(row=len(accounts), column=0, padx=1, sticky="nsew")

def addList():
    dialog = CTkToplevel(app)
    dialog.wm_transient(app)
    dialog.title("Add New Account")
    center_width = int(screen_width / 2 - 400 / 2)
    center_height = int(screen_height / 2 - 300 / 2)
    dialog.geometry(f"400x300+{center_width}+{center_height}")
    dialog.resizable(False, False)
    
    url_label = CTkLabel(dialog, text="Website URL:")
    url_label.pack(pady=(20, 5))
    url_entry = CTkEntry(dialog, width=300, placeholder_text="https://example.com")
    url_entry.pack()
    
    user_label = CTkLabel(dialog, text="Username:")
    user_label.pack(pady=(10, 5))
    user_entry = CTkEntry(dialog, width=300)
    user_entry.pack()
    
    pass_label = CTkLabel(dialog, text="Password:")
    pass_label.pack(pady=(10, 5))
    pass_entry = CTkEntry(dialog, width=300, show="•")
    pass_entry.pack()
    
    def submit():
        url = url_entry.get()
        username = user_entry.get()
        password = pass_entry.get()
        
        if url and username and password:
            conn = sqlite3.connect('data/password_manager.db')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO accounts (url, username, password) VALUES (?, ?, ?)",
                (url, username, password)
            )
            conn.commit()
            conn.close()
            
            refresh_accounts_list()
            
            dialog.destroy()
        else:
            error_label = CTkLabel(dialog, text="Please fill all fields!", text_color="red")
            error_label.pack(pady=5)
    
    submit_btn = CTkButton(dialog, text="Add Account", command=submit)
    submit_btn.pack(pady=10)
    
    dialog.grab_set()
    app.wait_window(dialog)

addVault = CTkButton(searchVault,text="+",width=40,height=40,fg_color="#0084ff",font=("Arial", 20),text_color="#ffffff",hover_color="#0073e6",border_width=0,corner_radius=8,command=addList)
addVault.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

leftSideFrame = CTkScrollableFrame(app, width=300, height=459, corner_radius=0)
leftSideFrame.grid(row=1, column=0, pady=1, sticky="nsew")

rightsideFrame = CTkFrame(app, width=599, height=500, corner_radius=0)
rightsideFrame.grid(row=0, column=1, padx=1, sticky="nsew", rowspan=2)

def propagate_scroll(event):
    leftSideFrame.event_generate('<MouseWheel>', delta=event.delta)

class ClickableFrame(CTkFrame):
    def __init__(self, master, account_id=None, **kwargs):
        super().__init__(master, **kwargs)
        self.account_id = account_id
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.default_bg = self.cget("fg_color")
        self.hover_bg = "#0084ff"
        self.click_callback = None
    
    def on_enter(self, event):
        self.configure(fg_color=self.hover_bg)
    
    def on_leave(self, event):
        self.configure(fg_color=self.default_bg)
    
    def on_click(self, event):
        if self.click_callback:
            self.click_callback()
    
    def set_command(self, command):
        self.click_callback = command

def delete_account(account_id):
    dialog = CTkToplevel(app)
    dialog.wm_transient(app)
    dialog.title("Delete Account")
    center_width = int(screen_width / 2 - 300 / 2)
    center_height = int(screen_height / 2 - 150 / 2)
    dialog.geometry(f"300x150+{center_width}+{center_height}")
    dialog.resizable(False, False)
    
    confirm_label = CTkLabel(dialog, text="Are you sure you want to delete this account?")
    confirm_label.pack(pady=(20, 5))
    
    def confirm_delete():
        conn = sqlite3.connect('data/password_manager.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
        conn.commit()
        conn.close()
        
        refresh_accounts_list()
        dialog.destroy()
    
    delete_btn = CTkButton(dialog, text="Delete", command=confirm_delete)
    delete_btn.pack(pady=10)
    
    cancel_btn = CTkButton(dialog, text="Cancel", command=dialog.destroy)
    cancel_btn.pack(pady=5)
    
    dialog.grab_set()
    app.wait_window(dialog)
def edit_account(account_id):
    dialog = CTkToplevel(app)
    dialog.wm_transient(app)
    dialog.title("Edit Account")

    center_width = int(screen_width / 2 - 400 / 2)
    center_height = int(screen_height / 2 - 300 / 2)
    dialog.geometry(f"400x300+{center_width}+{center_height}")

    dialog.resizable(False, False)
    
    conn = sqlite3.connect('data/password_manager.db')
    cursor = conn.cursor()
    cursor.execute("SELECT url, username, password FROM accounts WHERE id = ?", (account_id,))
    account = cursor.fetchone()
    conn.close()
    
    if account:
        url, username, password = account
        
        url_label = CTkLabel(dialog, text="Website URL:")
        url_label.pack(pady=(20, 5))
        url_entry = CTkEntry(dialog, width=300, placeholder_text="https://example.com")
        url_entry.insert(0, url)
        url_entry.pack()
        
        user_label = CTkLabel(dialog, text="Username:")
        user_label.pack(pady=(10, 5))
        user_entry = CTkEntry(dialog, width=300)
        user_entry.insert(0, username)
        user_entry.pack()
        
        pass_label = CTkLabel(dialog, text="Password:")
        pass_label.pack(pady=(10, 5))
        pass_entry = CTkEntry(dialog, width=300, show="•")
        pass_entry.insert(0, password)
        pass_entry.pack()
        
        def submit():
            new_url = url_entry.get()
            new_username = user_entry.get()
            new_password = pass_entry.get()
            
            if new_url and new_username and new_password:
                conn = sqlite3.connect('data/password_manager.db')
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE accounts SET url=?, username=?, password=? WHERE id=?",
                    (new_url, new_username, new_password, account_id)
                )
                conn.commit()
                conn.close()
                
                refresh_accounts_list()
                
                dialog.destroy()
            else:
                error_label = CTkLabel(dialog, text="Please fill all fields!", text_color="red")
                error_label.pack(pady=5)
        
        submit_btn = CTkButton(dialog, text="Update Account", command=submit)
        submit_btn.pack(pady=10)
    else:
        error_label = CTkLabel(dialog, text="Account not found!", text_color="red")
        error_label.pack(pady=5)

def create_clickable_item(parent, icon_path, title, subtitle, index, account_id=None):
    outer_frame = CTkFrame(parent,height=60,fg_color="transparent",)
    outer_frame.grid(row=index, column=0, sticky="ew", padx=10, pady=5)

    frame = ClickableFrame(outer_frame,height=60,fg_color="transparent",account_id=account_id)
    frame.pack(fill="both", expand=True)
    
    def show_account_details():
        if account_id:
            conn = sqlite3.connect('data/password_manager.db')
            cursor = conn.cursor()
            cursor.execute("SELECT url, username, password FROM accounts WHERE id = ?", (account_id,))
            account = cursor.fetchone()
            conn.close()
            
            if account:
                url, username, password = account
                
                for widget in rightsideFrame.winfo_children():
                    widget.destroy()

                header_label = CTkLabel(rightsideFrame, text="Account Details", width=600, font=("Arial", 25, "bold"))
                header_label.pack(pady=(20, 10), padx=20)
                
                url_label = CTkLabel(rightsideFrame, text=f"URL: {url}", font=("Arial", 18))
                url_label.pack(pady=(20, 5), padx=20, anchor="w")
                
                user_label = CTkLabel(rightsideFrame, text=f"Username: {username}", font=("Arial", 18))
                user_label.pack(pady=5, padx=20, anchor="w")

                user_label_copy = CTkButton(rightsideFrame, text="Copy Username", command=lambda: app.clipboard_clear() or app.clipboard_append(username))
                user_label_copy.pack(pady=5, padx=20, anchor="w")
                
                pass_label = CTkLabel(rightsideFrame, text=f"Password: {password}", font=("Arial", 18))
                pass_label.pack(pady=5, padx=20, anchor="w")
                pass_label_copy = CTkButton(rightsideFrame, text="Copy Password", command=lambda: app.clipboard_clear() or app.clipboard_append(password))
                pass_label_copy.pack(pady=5, padx=20, anchor="w")

                delete_button = CTkButton(rightsideFrame, text="Delete Account", command=lambda: delete_account(account_id))
                delete_button.pack(pady=(20, 10), padx=20)

                edit_button = CTkButton(rightsideFrame, text="Edit Account", command=lambda: edit_account(account_id))
                edit_button.pack(pady=(20, 10), padx=20)
    
    frame.set_command(show_account_details)
    
    icon_img = CTkImage(Image.open(icon_path), size=(30, 30))
    
    icon_label = CTkLabel(frame,image=icon_img,text="")
    icon_label.grid(row=0, column=0, rowspan=2, padx=(30, 15), sticky="w")
    
    title_label = CTkLabel(frame,text=title,font=("Arial", 14, "bold"),text_color="#ffffff",anchor="w")
    title_label.grid(row=0, column=1, padx=15, sticky="w")
    
    subtitle_label = CTkLabel(frame,text=subtitle,font=("Arial", 12),text_color="#f4f4f4",anchor="w")
    subtitle_label.grid(row=1, column=1, padx=15, sticky="w")
    
    frame.grid_columnconfigure(1, weight=1)
    
    return frame

refresh_accounts_list()
app.mainloop()