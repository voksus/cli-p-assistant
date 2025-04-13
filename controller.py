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
operation_cache: dict = {} # For storing temporary data between steps

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
    global is_running # Allow modification and access
    v.display_success("goodbye")
    is_running = False

# ================ Handler Stubs ================
# These methods will contain the logic for each command.
# They interact with the View to get input and display results,
# and with the Model to perform operations and handle data.
def handle_menu_back():
    """Handles the 'menu' command to go up one level."""
    global current_path, operation_cache
    if current_path:
        current_path.pop()
        operation_cache = {} # Clear the cache
    else:
        v.display_warning("already_at_main_menu") # Add message key

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
    global current_path, address_book, notebook

    # Ask user for deletion choice (contact or note)
    choice = v.get_input("com_prompt_main_remove").lower()

    if choice == 'contact':
        if not address_book:  # Check if there are contacts
            v.display_error("not_found")
            return

        v.display_contacts(address_book)

        try:
            # Ask user to select a contact by number
            contact_index = v.get_input_int("com_prompt_contact_index") - 1
        except ValueError:
            v.display_error("invalid_number")
            return

        # Validate contact index
        if contact_index < 0 or contact_index >= len(address_book):
            v.display_error("invalid_contact_id")
            return

        # Get the contact to delete
        contact = list(address_book.values())[contact_index]

        # Confirm deletion
        if v.get_confirmation("confirm_prompt", info=v.get_short_contact_info(contact)):
            address_book.remove(contact)
            v.display_success("contact_deleted", name=contact.name)
        else:
            v.display_info("deletion_cancelled")

    elif choice == 'note':
        if not notebook:  # Check if there are notes
            v.display_error("no_notes_found")
            return

        v.display_notes(notebook)

        try:
            # Ask user to select a note by number
            note_index = v.get_input_int("com_prompt_note_index") - 1
        except ValueError:
            v.display_error("invalid_number")
            return

        # Validate note index
        if note_index < 0 or note_index >= len(notebook):
            v.display_error("invalid_note_id")
            return

        # Get the note to delete
        note = notebook[note_index]

        # Confirm deletion
        if v.get_confirmation("confirm_prompt", info=v.get_short_note_info(note)):
            notebook.remove(note)
            v.display_success("note_deleted", title=note.title)
        else:
            v.display_info("deletion_cancelled")

    else:
        v.display_error("invalid_command")

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
    commands = {} # Create the dictionary
    state = tuple(current_path) # Make sure there is tuple conversion for comparison

    # Help messages depend on the program state
    if not state:
         commands = { # Main help commands
              "add": "Add a new contact or note",
              "change": "Modify an existing contact or note",
              "remove": "Delete a contact or note",
              "find": "Search contacts or notes",
              "birthdays": "Show upcoming birthdays",
              "help": "Show this help message",
              "exit/quit/q": "Save data and exit"
         }
    elif state == ("add",): commands = {"contact": "Add a contact", "note": "Add a note", "menu": "Back"}
    elif state == ("change",): commands = {"contact": "Change a contact", "note": "Change a note", "menu": "Back"}
    elif state == ("remove",): commands = {"contact": "Remove a contact", "note": "Remove a note", "menu": "Back"}
    elif state == ("find",): commands = {"contact": "Find contacts", "note": "Find notes", "menu": "Back"}
    elif len(state) >= 2 and state[0] == "change" and state[1] not in ("note", "contact"): # changing a contact - all options
        commands = {
            "add phone <phone>": "Add a phone (10 digits)",
            "change phone <index> <new_phone>": "Change a phone",
            "remove phone <index>": "Remove a phone",
            "add email <email>": "Add an email",
            "change email <index> <new_email>": "Change an email",
            "remove email <index>": "Remove an email",
            "birthday <dd.mm.yyyy>": "Set/change birthday (empty to remove)",
            "name <new_name>": "Change contact name",
            "menu": "Finish changing this contact"
        }
    elif len(state) >= 3 and state[0] == "change" and state[1] == "note": # changing a note - all options
        commands = {
            "title <new_title>": "Change note title (4-128 chars)",
            "content <text>": "Replace note content", # Separate task implements multiline
            "add tag <tag>": "Add a tag (letters, numbers, _, 2-16 chars)",
            "remove tag <tag>": "Remove a tag",
            "menu": "Finish changing this note"
        }
    # There would be code for removing too.

    v.display_help()

# ================ Helper/Validation Functions ================

def validate_and_parse_birthday(date_str: str) -> date | None:
    """ Tries to parse DD.MM.YYYY and validates the date. Returns date or raises BirthdayError."""
    # TODO: Implement birthday parsing and validation logic

def run():
    """Main application loop."""
    global is_running, current_path, operation_cache

    initialize() # Load data and set initial state

    while is_running:
        path_str = get_path_string()
        current_prompt_key = "command_prompt" # Default prompt

        # --- Determine prompt based on state ---
        state = tuple(current_path)
        if state == ("add",): current_prompt_key = "prompt_add_type"
        elif state == ("add", "contact"): current_prompt_key = "prompt_enter_name"
        elif state == ("add", "note"): current_prompt_key = "prompt_enter_title"
        elif state == ("change",): current_prompt_key = "prompt_change_type"
        elif state == ("change", "contact") and "contact_to_change" in operation_cache: current_prompt_key = "prompt_select_index_to_change"
        elif state == ("change", "note") and "note_to_change" in operation_cache: current_prompt_key = "prompt_select_index_to_change"
        elif len(state) >= 2 and state[0] == "change" and state[1] != "note" and state[1] != "contact": current_prompt_key = "prompt_what_to_change_contact"
        elif len(state) >= 3 and state[0] == "change" and state[1] == "note": current_prompt_key = "prompt_what_to_change_note"
        elif state == ("remove",): current_prompt_key = "prompt_remove_type"
        elif state == ("remove", "contact") and "contact_to_remove" in operation_cache: current_prompt_key = "prompt_select_index_to_remove"
        elif state == ("remove", "note") and "note_to_remove" in operation_cache: current_prompt_key = "prompt_select_index_to_remove"
        elif state == ("find",): current_prompt_key = "prompt_find_type"
        elif state == ("find", "contact"): current_prompt_key = "prompt_enter_search_term"
        elif state == ("find", "note"): current_prompt_key = "prompt_enter_search_term"
        elif state == ("birthdays",): current_prompt_key = "prompt_enter_days"
        # More specific prompts need coordination with handlers

        user_input = v.get_input(current_prompt_key, path_info=path_str)
        command, args = parse_input(user_input) # Assumes parse_input() is defined elsewhere

        # --- Universal command handling ---
        if command == "menu":
            handle_menu_back()
            continue
        if command in ["exit", "quit", "q"]:
            quit_application()
            continue # is_running will be False

        # --- State-based command/input handling ---
        try:
            state = tuple(current_path)

            # Top Level
            if not state:
                if command == "add": handle_add_base(args)
                elif command == "change": handle_change_base(args)
                elif command == "remove": handle_remove_base(args)
                elif command == "find": handle_find_base(args)
                elif command == "birthdays": handle_birthdays(args)
                elif command == "help": handle_help()
                elif command == "": pass
                else: v.display_error("invalid_command")
            # Input handling for specific states (examples)
            elif state == ("add",):
                if command == "contact": handle_add_contact()
                elif command == "note": handle_add_note()
                else: v.display_error("invalid_type")
            elif state == ("find",): # Expecting "contact" or "note"
                if command == "contact": current_path.append("contact")
                elif command == "note": current_path.append("note")
                else: v.display_error("invalid_type")
            elif state == ("find", "contact"): # Expecting search term
                 term = user_input
                 results = address_book.find_contacts(term)
                 v.display_info("contacts_found_title", count=len(results))
                 v.display_contacts(results)
                 handle_menu_back() # Go back after showing results
            elif state == ("find", "note"): # Expecting search term
                 term = user_input
                 results = notebook.find_notes(term)
                 v.display_info("notes_found_title", count=len(results))
                 v.display_notes(results)
                 handle_menu_back()
            elif state == ("birthdays",): # Expecting number of days
                 days_str = user_input
                 try:
                     days = int(days_str)
                     # Validation of days range (1-365) is done here as it's controller logic.
                     if not (0 < days <= 365):
                         raise ValueError("invalid_days_range") # Add message key
                     results = address_book.get_birthdays_in_next_days(days)
                     v.display_birthdays(results)
                 except ValueError as e:
                     # If a conversion to int fails or days are out of range
                     v.display_error(str(e)) # Pass message key from exception
                 handle_menu_back()
            # --- Other states ---
            # Logic for the other states should be implemented in their handlers or needs a more complex dispatch here.
            else:
                 # If the command wasn't recognized for the current state (and it's not 'menu'/'exit')
                 if command:  # If the user typed something that looked like a command
                     v.display_error("invalid_command_for_state") # Add message key

        # Catch errors from Model or Controller
        except (m.ContactError, m.PhoneError, m.EmailError, m.BirthdayError,
                m.TitleError, m.TagError, m.NotFoundError, m.NoteError, IndexError) as e:
            message_key = str(e)
            v.display_error(message_key)
        except ValueError as e:
             # Catch errors that are related to Controller for example days parsing in birthdays
             message_key = str(e)
             v.display_error(message_key)

        except Exception as e: # Unexpected errors
             v.display_error("generic_error", error_message=str(e)) # Pass the error message


if __name__ == "__main__":
    import main
    main.main()