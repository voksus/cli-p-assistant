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
    # TODO: Save data before exiting
    # ...
    is_running = False

# ================ Handler Stubs ================
# These methods will contain the logic for each command.
# They interact with the View to get input and display results,
# and with the Model to perform operations and handle data.
def handle_menu_back():
    """Handles the 'menu' command to go up one level."""
    pass

def handle_add_base(args: list[str]):
    global current_path # Allow modification
    # TODO: Ask user "contact" or "note"?
    # ...
    pass

def handle_add_contact():
    global current_path, address_book # Allow access/modification
    current_path.append("contact") # Now path is ["add", "contact"]
    # TODO:
    # ...
    pass

def handle_add_note():
    global current_path, notebook # Allow access/modification
    current_path.append("note") # Path ["add", "note"]
    # TODO: Ask for title, validate, create Note, add to notebook, handle errors, display result
    # ...
    pass

def handle_change_base(args: list[str]):
    global current_path # Allow modification
    # TODO: Ask "contact" or "note"? Find item, display list, get index.
    # ...
    pass

def handle_change_contact(contact: m.Contact):
    global current_path, address_book, notebook # Allow access
    # Path is ["change", contact.name]
    # TODO: Loop asking what to change (phone, email, birthday, name?)
    # ...
    pass

def handle_change_note(note: m.Note):
    global current_path, notebook, address_book # Allow access
    # Path is ["change", "note", note.title]
    # TODO: Loop asking what to change (title, content, tags?)
    # Handle sub-commands, call model, validate, handle errors, save, display results
    pass

def handle_remove_base(args: list[str]):
    global current_path, address_book, notebook # Allow access/modification
    # TODO: Ask "contact" or "note"? Find item, display list, get index, confirm.
    # ...
    pass

def handle_find_base(args: list[str]):
    global current_path, address_book, notebook # Allow access
    # TODO: Ask "contact" or "note"? Ask search term.
    # ...
    pass

def handle_birthdays(args: list[str]):
    global address_book # Allow access
    # TODO: Ask for number of days (n)
    # ...
    pass

def handle_help():
    global current_path # Allow access
    # TODO: Define the structure for commands based on current_path
    # ...
    v.display_help()

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