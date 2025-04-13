# cli-p-assistant
CLI-P Assistant : a console-based application to work with address book and notes

**CLI-P Assistant** is a command-line personal assistant built in Python using the **MVC (Model-View-Controller)** architectural pattern. It combines the functionality of an **address book** and a **note manager**, allowing users to efficiently organize everyday information in one convenient interface.

[🇺🇦 Switch to Ukrainian README](README.md)

---

### 🧠 Uniqueness & Advantages

CLI-P Assistant stands out with:

- 🤝 **User-friendly command structure** for easy interaction without needing to remember complex instructions
- 🧠 **Intelligent input handling**: helpful suggestions for incorrect/incomplete input
- 🏷️ **Flexible note management**, including tagging, searching, editing, and sorting
- 👥 **Comprehensive contact support**: names, phones, emails, addresses, birthdays
- 💾 **Local data storage** that persists between sessions
- 🧩 **Scalable MVC architecture**: easy to extend and maintain

---

## ⚙️ Features Overview

| ⚙️ Feature                        | 💬 Description                                                                 |
|----------------------------------|-------------------------------------------------------------------------------|
| 👥 Manage Contacts               | Add, edit, delete contacts with name, phones, emails, address, birthday      |
| 🔍 Search                        | Find contacts and notes by keywords                                           |
| 📝 Note Management               | Add, edit, delete, tag, and search notes                                     |
| 🎂 Birthday Tracking             | Store and display upcoming birthdays                                         |
| 💾 Persistent Storage            | Data saved locally and restored across sessions                              |
| ✅ Input Validation              | Friendly error messages for invalid input                                    |
| 📚 Command Help                  | Show help and available commands                                             |

---

## 💻 How to Use

| 💻 Command                            | 📌 Description                                         |
|--------------------------------------|--------------------------------------------------------|
| `add contact`                        | ➕ Add a new contact                                   |
| `edit contact`                       | 📝 Edit existing contact                              |
| `delete contact`                     | ❌ Delete a contact                                   |
| `search contact <query>`            | 🔍 Find contact by name, phone, or email              |
| `show all contacts`                 | 📇 Display all saved contacts                         |
| `add phone <name> <phone>`          | 📞 Add phone number to contact                        |
| `edit phone <name> <old> <new>`     | ✏️ Edit a phone number                                |
| `delete phone <name> <phone>`       | 🗑️ Remove phone number                                |
| `add email <name> <email>`          | 📧 Add email to contact                               |
| `edit email <name> <old> <new>`     | ✏️ Edit email address                                 |
| `delete email <name> <email>`       | 🗑️ Remove email address                               |
| `add address <name> <address>`      | 🏠 Add address to contact                             |
| `edit address <name> <address>`     | ✏️ Edit address                                       |
| `delete address <name>`             | 🗑️ Remove address                                     |
| `add birthday <name> <date>`        | 🎂 Add birthday to contact                            |
| `edit birthday <name> <date>`       | ✏️ Edit birthday                                      |
| `delete birthday <name>`            | 🗑️ Remove birthday                                    |
| `show birthday <name>`              | 🎉 Show birthday                                      |
| `show upcoming birthdays <days>`    | 📅 Show birthdays in upcoming days                   |
| `add note`                          | 📝 Create new note                                    |
| `edit note <id>`                    | ✏️ Edit note by ID                                    |
| `delete note <id>`                  | 🗑️ Delete note by ID                                  |
| `clear notes`                       | ❌ Delete all notes                                   |
| `search notes <query>`              | 🔍 Search notes by text or tag                        |
| `show notes by tag <tag>`           | 🏷️ Filter notes by tag                                |
| `sort notes by tag`                 | 🧾 Sort notes alphabetically by tag                   |
| `sort notes by date`                | 📆 Sort notes by creation date                        |
| `help`                              | 🆘 Show available commands                            |
| `exit` / `close` / `bye`            | 🚪 Exit the assistant                                 |

---

## 🗂 Project Structure

| 📁 File / Folder   | 📌 Description                                 |
|-------------------|-----------------------------------------------|
| `main.py`         | 🚀 Entry point, CLI launch logic               |
| `models/`         | 📦 Data models: contact, note, and collections |
| `views/`          | 👁️ CLI outputs and user interaction messages   |
| `controllers/`    | 🧠 Command handlers and logic                  |
| `utils/`          | 🛠️ Utilities: parsers, helpers                 |
| `.env`            | ⚙️ Configuration and environment variables     |
| `README.md`       | 📖 Documentation in Ukrainian                  |
| `README_EN.md`    | 📖 Documentation in English                    |

---

## 📦 Installation

```bash
git clone https://github.com/voksus/cli-p-assistant.git
cd cli-p-assistant
pip install -r requirements.txt
python main.py
```

