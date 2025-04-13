# Controller file by MVC pattern
# This file contains the controller of the app
# It contains the logic of the app and the interaction with the model and the view

import model as m
import view as v
from datetime import date, datetime # Added date

# ================ Module-Level State ================
# Store application state at the module level since Controller is utility-like
address_book: m.AdressBook = None
notebook: m.Notebook = None
current_path: list[str] = [] # Tracks the user's location in the menu e.g., ["add", "contact"]
is_running: bool = False

def initialize():
    """Loads data and sets initial state."""
    global address_book, notebook, is_running, current_path
    address_book, notebook = m.load_data_from_file()
    # TODO: Check if id_counters need to be loaded/saved and restored in Contact/Note classes
    current_path = []
    is_running = True
    v.display_success("welcome")

def get_path_string() -> str:
    """Returns the current menu path as a string for display."""
    global current_path
    return v.MESSAGES["input_path_separator"].join(current_path)

def parse_input(user_input: str) -> tuple[str, list[str]]:
    """Parses user input into a command and arguments."""
    parts = user_input.strip().split()
    command = parts[0].lower() if parts else ""
    args = parts[1:]
    return command, args

def quit_application():
    """Saves data and sets the flag to stop the main loop."""
    global is_running, address_book, notebook # Allow modification and access
    m.save_data_to_file(address_book, notebook)
    is_running = False

# ================ Handler Stubs ================
# These methods will contain the logic for each command.
# They interact with the View to get input and display results,
# and with the Model to perform operations and handle data.
def handle_menu_back():
    """Handles the 'menu' command to go up one level."""
    global current_path
    if current_path:
        current_path.pop()
    pass

def handle_add_base(args: list[str]):
    """Handles the 'add' command to add a contact or note."""
    global current_path
    if len(args) == 0:
        choice = v.get_input("What would you like to add? (contact/note): ").strip().lower()
        if choice == "contact":
            handle_add_contact()
        elif choice == "note":
            handle_add_note()
        else:
            v.display_error("Invalid choice. Please select 'contact' or 'note'.")
    else:
        v.display_error("Too many arguments. Use 'add' to begin adding.")
    pass

def handle_add_contact():
    """Handles the addition of a new contact."""
    global current_path, address_book
    current_path.append("contact")

    name = v.get_input("Enter contact name: ")
    phone = v.get_input("Enter contact phone: ")
    email = v.get_input("Enter contact email: ")

    # Add contact to address book
    new_contact = m.Contact(name, phone, email)
    address_book.add_contact(new_contact)

    v.display_success(f"Contact '{name}' added successfully.")
    current_path.pop()  # Go back to the previous level in menu
    pass

def handle_add_note():
    """Handles the addition of a new note."""
    global current_path, notebook
    current_path.append("note")

    title = v.get_input("Enter note title: ")
    content = v.get_input("Enter note content: ")
    tags = v.get_input("Enter tags (comma-separated): ").split(',')

    new_note = m.Note(title, content, tags)
    notebook.add_note(new_note)

    v.display_success(f"Note '{title}' added successfully.")
    current_path.pop()
    pass

def handle_change_base(args: list[str]):
    global current_path # Allow modification
    # TODO: Ask "contact" or "note"? Find item, display list, get index.
    """Handles the 'change' command to modify a contact or note."""
    if len(args) == 0:
        choice = v.get_input("What would you like to change? (contact/note): ").strip().lower()
        if choice == "contact":
            handle_change_contact_base()
        elif choice == "note":
            handle_change_note_base()
        else:
            v.display_error("Invalid choice. Please select 'contact' or 'note'.")
    else:
        v.display_error("Too many arguments. Use 'change' to begin changing.")

def handle_change_contact_base():
    """Handles the 'change contact' command to modify a specific contact."""
    global current_path, address_book
    current_path.append("contact")

    # Display list of contacts
    contacts = address_book.get_all_contacts()
    if not contacts:
        v.display_error("No contacts available to modify.")
        current_path.pop()  # Go back
        return

    # Show list and ask user to select
    v.display_success("Available contacts to change:")
    for idx, contact in enumerate(contacts, start=1):
        v.display_info(f"{idx}. {contact.name} - {contact.phone} - {contact.email}")

    choice = v.get_input("Enter the number of the contact to modify: ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(contacts):
            handle_change_contact(contacts[index])
        else:
            v.display_error("Invalid contact number.")
    except ValueError:
        v.display_error("Invalid input. Please enter a valid number.")

    current_path.pop()  # Go back

def handle_change_contact(contact: m.Contact):
    """Handles the modification of a single contact's details."""
    global current_path, address_book
    current_path.append(contact.name)

    # Ask what to change
    field_to_change = v.get_input("What would you like to change? (name/phone/email): ").strip().lower()

    if field_to_change == "name":
        new_name = v.get_input("Enter new name: ")
        contact.name = new_name
        v.display_success(f"Contact name changed to {new_name}")
    elif field_to_change == "phone":
        new_phone = v.get_input("Enter new phone number: ")
        contact.phone = new_phone
        v.display_success(f"Contact phone changed to {new_phone}")
    elif field_to_change == "email":
        new_email = v.get_input("Enter new email: ")
        contact.email = new_email
        v.display_success(f"Contact email changed to {new_email}")
    else:
        v.display_error("Invalid field. Please select 'name', 'phone', or 'email'.")

    address_book.save_to_file()  # Save the updated data
    current_path.pop()  # Go back


def handle_change_note_base():
    """Handles the 'change note' command to modify a specific note."""
    global current_path, notebook
    current_path.append("note")

    # Display list of notes
    notes = notebook.get_all_notes()
    if not notes:
        v.display_error("No notes available to modify.")
        current_path.pop()  # Go back
        return

    # Show list and ask user to select
    v.display_success("Available notes to change:")
    for idx, note in enumerate(notes, start=1):
        v.display_info(f"{idx}. {note.title} | Tags: {note.tags}")

    choice = v.get_input("Enter the number of the note to modify: ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(notes):
            handle_change_note(notes[index])
        else:
            v.display_error("Invalid note number.")
    except ValueError:
        v.display_error("Invalid input. Please enter a valid number.")

    current_path.pop()  # Go back


def handle_change_note(note: m.Note):
    """Handles the modification of a single note's details."""
    global current_path, notebook
    current_path.append(note.title)

    # Ask what to change
    field_to_change = v.get_input("What would you like to change? (title/content/tags): ").strip().lower()

    if field_to_change == "title":
        new_title = v.get_input("Enter new title: ")
        note.title = new_title
        v.display_success(f"Note title changed to {new_title}")
    elif field_to_change == "content":
        new_content = v.get_input("Enter new content: ")
        note.content = new_content
        v.display_success(f"Note content changed.")
    elif field_to_change == "tags":
        new_tags = v.get_input("Enter new tags (comma-separated): ").split(',')
        note.tags = new_tags
        v.display_success(f"Note tags updated.")
    else:
        v.display_error("Invalid field. Please select 'title', 'content', or 'tags'.")

    notebook.save_to_file()  # Save the updated data
    current_path.pop()  # Go back
    pass

def handle_remove_base(args: list[str]):
    """Handles the 'remove' command to delete a contact or note."""
    global current_path
    if len(args) == 0:
        choice = v.get_input("What would you like to remove? (contact/note): ").strip().lower()
        if choice == "contact":
            handle_remove_contact_base()
        elif choice == "note":
            handle_remove_note_base()
        else:
            v.display_error("Invalid choice. Please select 'contact' or 'note'.")
    else:
        v.display_error("Too many arguments. Use 'remove' to begin removing.")

def handle_remove_contact_base():
    """Handles the 'remove contact' command to delete a specific contact."""
    global current_path, address_book
    current_path.append("contact")

    # Display list of contacts
    contacts = address_book.get_all_contacts()
    if not contacts:
        v.display_error("No contacts available to remove.")
        current_path.pop()  # Go back
        return

    # Show list and ask user to select
    v.display_success("Available contacts to remove:")
    for idx, contact in enumerate(contacts, start=1):
        v.display_info(f"{idx}. {contact.name} - {contact.phone} - {contact.email}")

    choice = v.get_input("Enter the number of the contact to remove: ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(contacts):
            confirm = v.get_input(f"Are you sure you want to remove {contacts[index].name}? (yes/no): ").strip().lower()
            if confirm == "yes":
                address_book.remove_contact(contacts[index])
                address_book.save_to_file()  # Save after removing
                v.display_success(f"Contact {contacts[index].name} removed.")
            else:
                v.display_info("Removal cancelled.")
        else:
            v.display_error("Invalid contact number.")
    except ValueError:
        v.display_error("Invalid input. Please enter a valid number.")

    current_path.pop()  # Go back


def handle_remove_note_base():
    """Handles the 'remove note' command to delete a specific note."""
    global current_path, notebook
    current_path.append("note")

    # Display list of notes
    notes = notebook.get_all_notes()
    if not notes:
        v.display_error("No notes available to remove.")
        current_path.pop()  # Go back
        return

    # Show list and ask user to select
    v.display_success("Available notes to remove:")
    for idx, note in enumerate(notes, start=1):
        v.display_info(f"{idx}. {note.title} | Tags: {note.tags}")

    choice = v.get_input("Enter the number of the note to remove: ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(notes):
            confirm = v.get_input(
                f"Are you sure you want to remove the note '{notes[index].title}'? (yes/no): ").strip().lower()
            if confirm == "yes":
                notebook.remove_note(notes[index])
                notebook.save_to_file()  # Save after removing
                v.display_success(f"Note '{notes[index].title}' removed.")
            else:
                v.display_info("Removal cancelled.")
        else:
            v.display_error("Invalid note number.")
    except ValueError:
        v.display_error("Invalid input. Please enter a valid number.")

    current_path.pop()  # Go back

def handle_find_base(args: list[str]):
    """Handles the 'find' command to search for contacts or notes."""
    global current_path, address_book, notebook
    if len(args) == 0:
        search_term = v.get_input("Enter search term: ").strip()

        # Search in contacts
        found_contacts = address_book.search_contacts(search_term)
        if found_contacts:
            v.display_success("Found contacts:")
            for contact in found_contacts:
                v.display_info(f"{contact.name} - {contact.phone} - {contact.email}")
        else:
            v.display_error("No contacts found.")

        # Search in notes
            found_notes = notebook.search_notes(search_term)
            if found_notes:
                v.display_success("Found notes:")
                for note in found_notes:
                    v.display_info(f"Title: {note.title} | Tags: {note.tags}")
            else:
                v.display_error("No notes found.")
    else:
        v.display_error("Too many arguments. Use 'find' to search.")
    pass

def handle_birthdays(args: list[str]):
    """Handles the 'birthdays' command to check upcoming birthdays."""
    global address_book
    if len(args) == 0:
        days_in_advance = v.get_input("Enter number of days to check for birthdays: ").strip()
        try:
            days_in_advance = int(days_in_advance)
            upcoming_birthdays = address_book.get_upcoming_birthdays(days_in_advance)

            if upcoming_birthdays:
                v.display_success(f"Upcoming birthdays in the next {days_in_advance} days:")
                for contact in upcoming_birthdays:
                    v.display_info(f"{contact.name} - {contact.birthday.strftime('%d.%m.%Y')}")
            else:
                v.display_error(f"No birthdays in the next {days_in_advance} days.")
        except ValueError:
            v.display_error("Invalid input. Please enter a valid number.")
    else:
        v.display_error("Too many arguments. Use 'birthdays' to check birthdays.")
    pass

def handle_help():
    """Displays help based on the current path."""
    global current_path
    if not current_path:  # Root menu
        v.display_help("Available commands: add, change, remove, find, birthdays, help, quit")
    elif "add" in current_path:
        v.display_help("Use 'contact' or 'note' to specify what you want to add.")
    elif "change" in current_path:
        v.display_help("Use 'contact' or 'note' to change a specific item.")
    elif "remove" in current_path:
        v.display_help("Use 'contact' or 'note' to remove a specific item.")
    elif "find" in current_path:
        v.display_help("Search for contacts or notes by a keyword.")
    elif "birthdays" in current_path:
        v.display_help("Check upcoming birthdays for the next n days.")
    else:
        v.display_error("No help available for this section.")

# ================ Helper/Validation Functions ================

def validate_and_parse_birthday(date_str: str) -> date | None:
    """ Tries to parse DD.MM.YYYY and validates the date. Returns date or raises BirthdayError."""
    # TODO: Implement birthday parsing and validation logic

def run():
    """Main application loop."""
    global is_running, current_path

    initialize() # Load data and set initial state

    while is_running:
        path_str = get_path_string()
        # TODO: Determine the correct prompt key based on the current state/path
        current_prompt_key = "command_prompt" # Default prompt

        user_input = v.get_input(current_prompt_key, path_info=path_str)
        command, args = parse_input(user_input)

        # TODO: Implement command handling based on current_path and command
        # This will involve a large dispatch mechanism (if/elif or dict mapping)
        # that calls appropriate handler methods.

        # Basic command handling (Top Level)
        if not current_path: # If at the root menu
            if command == "add":
                handle_add_base(args)
            elif command == "change":
                handle_change_base(args)
            elif command == "remove":
                handle_remove_base(args)
            elif command == "find":
                    handle_find_base(args)
            elif command == "birthdays":
                handle_birthdays(args)
            elif command == "help":
                handle_help()
            elif command in ["exit", "quit", "q"]:
                quit_application()
            elif command == "": # Empty input
                pass # Just show prompt again
            else:
                v.display_error("invalid_command")
        else:
            # TODO: Handle commands within sub-menus (e.g., 'name', 'phone', 'tag', 'menu' commands)
            if command == "menu":
                    handle_menu_back()
            else:
                # Placeholder for sub-command handling
                pass # Sub-menu logic not implemented
                handle_menu_back() # Go back for now


if __name__ == "__main__":
    import main
    main.main()