# 🔐 Password Manager (Using Python GUI)

## 📌 Description

**Password Manager** is a desktop application built using Python's `customtkinter` library for a modern GUI and `sqlite3` for secure local data storage. It helps users **securely store and manage their login credentials** (URL, username, password) for different websites, all within an intuitive interface.

Data is stored persistently in an SQLite database (`password_manager.db`), ensuring credentials remain available across sessions.

---

## 🎯 Objectives

- Develop a user-friendly GUI application for managing passwords.
- Implement complete **CRUD** (Create, Read, Update, Delete) operations.
- Integrate `customtkinter` with `sqlite3` for persistent storage.
- Provide efficient **search functionality** for quick account retrieval.

---

## ⚙️ Features

- 🔐 **Secure storage** of URLs, usernames, and passwords.
- 🧾 **Add, View, Edit, and Delete** account entries.
- 🔍 **Search bar** for filtering stored accounts in real-time.
- ✅ **Copy to clipboard** buttons for usernames and passwords.
- 💡 **Visual feedback** on list item hover and selection.

---

## 🧠 Function Explanations

### 📁 Initialize Database
- Creates the `./data/` directory and `accounts` table in `password_manager.db` if they don't already exist.

### 🔍 On Search Change
- Listens to search bar input and updates the account list based on the entered term.

### ♻️ Refresh Accounts List
- Reloads the list of stored accounts with optional search filtering.

### ➕ Add List
- Opens a dialog to add a new account to the database.

### 🧱 Clickable Frame
- A custom frame for each account row that responds visually to hover and click events.

### ❌ Delete Account
- Prompts for confirmation before removing an account entry.

### ✏️ Edit Account
- Opens a dialog to edit and update an account's information.

### 🧱 Create Clickable Item
- Constructs each clickable account row in the list and links it to the detail view.

### 📄 Show Account Details
- Displays selected account's full details and offers copy, edit, and delete options.

---

## 🖼️ Layout Design

The application consists of the following UI elements:

- **Left Pane:** Search bar, Add (+) button, scrollable account list.
- **Right Pane:** Account detail viewer with action buttons.

### Example Views:
- Add Account
- View Account Details
- Edit/Delete Account Popups

---

## 🧩 Technologies Used

- `Python 3`
- [`customtkinter`](https://github.com/TomSchimansky/CustomTkinter) - Modern tkinter UI framework.
- `sqlite3` - Lightweight database for local credential storage.
- `Pillow` - For handling icons/images.

---

## 🚀 Getting Started

### 🔧 Prerequisites

Ensure the following Python packages are installed:

```bash
pip install customtkinter pillow
```

### ▶️ Run the Application

```bash
python password_manager.py
```

### 🗂️ Project Structure

```bash
password-manager/
│
├── data/
│   └── password_manager.db         # SQLite database file
│
├── url_default.png                 # Default icon for URLs (optional)
│
├── password_manager.py             # Main application file
│
└── README.md                       # Project documentation
```
