# filename: controller.py
# Controller file by MVC pattern
# This file contains the controller of the app
# It contains the logic of the app and the interaction with the model and the view

import model as m
import view as v
from datetime import date, datetime

# ================ Module-Level State ================
# Store application state at the module level
address_book: m.AdressBook | None = None
notebook: m.Notebook | None = None
current_path: list[str] = [] # Tracks the user's location in the menu e.g., ["add", "contact"]
is_running: bool = False
operation_cache: dict = {} # For storing temporary data between steps (e.g., contact being edited)

# ================ Initialization and State ================

def initialize():
    """Loads data and sets initial state."""
    global address_book, notebook, is_running, current_path, operation_cache
    # Load data, which now also sets up autosave in the model's load function
    address_book, notebook = m.load_data_from_file()
    current_path = []
    operation_cache = {} # Clear cache on init
    is_running = True
    v.display_success("welcome") # Use success for welcome

def get_path_string() -> str:
    """Returns the current menu path as a string for display."""
    global current_path
    # Use view's separator for consistency
    return v.MESSAGES["input_path_separator"].join(current_path) if current_path else ""

def parse_input(user_input: str) -> tuple[str, list[str]]:
    """Parses user input into a command and arguments."""
    parts = user_input.strip().split()
    command = parts[0].lower() if parts else ""
    args = parts[1:]
    return command, args

def quit_application():
    """Sets the flag to stop the main loop. Autosave handles saving."""
    global is_running
    # No explicit save call needed here due to autosave in model
    v.display_success("goodbye") # Use success for goodbye
    is_running = False

# ================ Navigation and Cache ================

def handle_menu_back():
    """Handles the 'menu' command to go up one level or clear context."""
    global current_path, operation_cache
    if current_path:
        current_path.pop()
        operation_cache = {} # Clear the cache when going back
    else:
        v.display_warning("already_at_main_menu")

# ================ Command Handlers (State Changers / Action Initiators) ================
# These functions primarily change the state (current_path) or initiate actions
# that will then require further input (handled within the action function or run loop).

def handle_add_base(args: list[str]):
    """Sets state for adding or prompts if type not specified."""
    global current_path
    if args:
        choice = args[0].lower()
        if choice in ["contact", "note"]:
            current_path.append("add")
            current_path.append(choice)
            # Now the run loop will see the new state and expect data input via specific handlers
            if choice == "contact":
                handle_add_contact_input() # Directly call the input handler
            elif choice == "note":
                handle_add_note_input() # Directly call the input handler
        else:
            v.display_error("invalid_type") # Invalid type like 'add something_else'
    else:
        # No args, just enter the 'add' menu level
        current_path.append("add")
        # The run loop will now prompt with "prompt_add_type"

def handle_find_base(args: list[str]):
    """Sets state for finding or prompts if type not specified."""
    global current_path
    if args:
        choice = args[0].lower()
        if choice in ["contact", "note"]:
            current_path.append("find")
            current_path.append(choice)
            # Now the run loop will expect the search term via specific handlers
            if choice == "contact":
                handle_find_contact_input()
            elif choice == "note":
                handle_find_note_input()
        else:
            v.display_error("invalid_type")
    else:
        # No args, enter the 'find' menu level
        current_path.append("find")
        # The run loop will now prompt with "prompt_find_type"

def handle_birthdays_base(args: list[str]):
    """Sets state for birthday search."""
    global current_path
    current_path.append("birthdays")
    # The run loop will now expect the number of days via handle_birthdays_input

# TODO: Implement handle_change_base, handle_remove_base similarly if needed
# For now, let's focus on making add, find, birthdays work.

# ================ Input Handlers (Data Collectors / Action Performers) ================
# These functions are called AFTER the state is set and are responsible
# for getting specific user input and performing the action.

def handle_add_contact_input():
    """Gets input for a new contact and adds it."""
    global address_book
    path_str = get_path_string()
    try:
        name = v.get_input("prompt_enter_name", path_info=path_str)
        if not name:
            v.display_warning("input_cancelled")
            handle_menu_back()
            return

        # Use model's validation for name format when creating Contact
        new_contact = m.Contact(name=name) # Raises ContactError on invalid name

        # Basic check for existing contact by name (case-insensitive) in the book
        if any(c.name.lower() == name.lower() for c in address_book.contacts):
             # Use the specific model error key here
             raise m.ContactError("duplicate_contact")

        # --- Get Phones (Optional) ---
        phones_input = v.get_input("prompt_enter_phones", path_info=path_str)
        phones = phones_input.split()
        valid_phones = []
        invalid_phones = []
        temp_contact_for_validation = m.Contact("temp") # Use a dummy for validation context
        for p in phones:
            try:
                # Use model's validation method (or regex directly if preferred)
                address_book._validate_phone(temp_contact_for_validation, p) # Validate format
                if p in valid_phones: # Check for duplicates within input
                    raise m.PhoneError("duplicate_phone") # Reuse error
                valid_phones.append(p)
            except m.PhoneError as phone_err: # Catch specific validation error
                v.display_error(str(phone_err)) # Show specific error
                invalid_phones.append(p)
            except Exception: # Catch other unexpected errors
                invalid_phones.append(p)
        # Display general warning about skipped invalid phones if any
        if invalid_phones:
             v.display_warning("invalid_phone_format", invalid_list=", ".join(invalid_phones)) # Adjust message key if needed

        # --- Get Emails (Optional) ---
        emails_input = v.get_input("prompt_enter_emails", path_info=path_str)
        emails = emails_input.split()
        valid_emails = []
        invalid_emails = []
        for e in emails:
             try:
                 # Use model's validation method
                 address_book._validate_email(temp_contact_for_validation, e) # Validate format
                 e_lower = e.lower()
                 if e_lower in [ve.lower() for ve in valid_emails]: # Check duplicates in input
                     raise m.EmailError("duplicate_email")
                 valid_emails.append(e) # Store original case
             except m.EmailError as email_err:
                 v.display_error(str(email_err)) # Show specific error
                 invalid_emails.append(e)
             except Exception: # Catch other unexpected errors
                 invalid_emails.append(e)
        if invalid_emails:
             v.display_warning("invalid_email_format", invalid_list=", ".join(invalid_emails)) # Adjust message key if needed

        # --- Get Birthday (Optional) ---
        birthday_str = v.get_input("prompt_enter_birthday", path_info=path_str)
        birthday = None
        if birthday_str:
            birthday = validate_and_parse_birthday(birthday_str) # Raises BirthdayError on failure (format/logic)
            # Use model's validation method for range check
            address_book.change_birthday(temp_contact_for_validation, birthday) # Raises BirthdayError on range issue

        # --- Assign validated data and Add Contact ---
        new_contact.phones = valid_phones # Add only valid phones
        new_contact.emails = valid_emails # Add only valid emails
        new_contact.birthday = birthday

        address_book.add_contact(new_contact) # Add the fully formed contact
        v.display_success("contact_added", name=new_contact.name)

    except (m.ContactError, m.PhoneError, m.EmailError, m.BirthdayError) as e:
        # Display specific errors from validation or model
        v.display_error(str(e), **getattr(e, 'kwargs', {})) # Pass the error key and any kwargs
        # Stay in the add contact menu to allow retry? Or go back? Let's go back for simplicity.
        handle_menu_back()
    except Exception as e:
        # Catch unexpected errors during input processing
        v.display_error("generic_error", error_message=str(e))
        handle_menu_back()
    else:
        # Go back only on successful addition
        handle_menu_back()


def handle_add_note_input():
    """Gets input for a new note and adds it."""
    global notebook
    path_str = get_path_string()
    try:
        title = v.get_input("prompt_enter_title", path_info=path_str)
        if not title:
            v.display_warning("input_cancelled")
            handle_menu_back()
            return

        # Model's __init__ validates length. Duplicate check is in notebook.add_note
        new_note = m.Note(title=title)

        # --- Get Content (Optional, example multiline) ---
        # print("Enter content (press Enter twice to finish):") # Use view message?
        # content_lines = []
        # while True:
        #     line = input()
        #     if not line:
        #         break
        #     content_lines.append(line)
        # new_note.content = "\n".join(content_lines)
        # Simple single line content for now:
        content_input = v.get_input("prompt_enter_content", path_info=path_str)
        new_note.content = content_input # Assign content


        # --- Get Tags (Optional) ---
        tags_input = v.get_input("prompt_enter_tags", path_info=path_str)
        tags = tags_input.split()
        added_tags = []
        # Add tags one by one using the model's method which includes validation
        for t in tags:
             try:
                 # Temporarily add to the note's list for validation context within add_tag_to_note
                 # This isn't ideal as the note isn't in the notebook yet.
                 # A better approach might be a separate validation function.
                 # Let's simulate validation using model logic directly here before adding to notebook.
                 tag_clean = t.strip()
                 if not (m.Note.MIN_TAG_LEN <= len(tag_clean) <= m.Note.MAX_TAG_LEN):
                     raise m.TagError("invalid_tag_length", min=m.Note.MIN_TAG_LEN, max=m.Note.MAX_TAG_LEN)
                 if not m.Note.TAG_PATTERN.match(tag_clean):
                     raise m.TagError("invalid_tag_format")

                 tag_lower = tag_clean.lower()
                 if tag_lower in added_tags: # Check against already added tags in this input session
                     raise m.TagError("duplicate_tag_in_note", tag=tag_lower, title=title)

                 added_tags.append(tag_lower) # Add validated, lowercased tag

             except m.TagError as tag_e:
                  v.display_error(str(tag_e), **getattr(tag_e, 'kwargs', {})) # Show specific error immediately
             # Continue processing other tags even if one is invalid

        new_note.tags = sorted(added_tags) # Assign validated tags

        # --- Add Note ---
        notebook.add_note(new_note) # Model handles duplicate title check and autosave
        v.display_success("note_added", title=new_note.title)

    except (m.TitleError, m.NoteError) as e:
        # Errors from Note init or notebook.add_note
        v.display_error(str(e), **getattr(e, 'kwargs', {}))
        handle_menu_back()
    except Exception as e:
        v.display_error("generic_error", error_message=str(e))
        handle_menu_back()
    else:
         # Go back only on success
         handle_menu_back()

def handle_find_contact_input():
    """Gets search term, finds contacts, displays them."""
    global address_book
    path_str = get_path_string()
    try:
        term = v.get_input("prompt_enter_search_term", path_info=path_str)
        if not term:
            v.display_warning("input_cancelled")
            handle_menu_back()
            return

        results = address_book.find_contacts(term) # Use the general find method
        v.display_info("contacts_found_title", count=len(results))
        # display_contacts handles the case where results is empty
        v.display_contacts(results, show_indices=False) # Don't show indices for search results

    except Exception as e:
        v.display_error("generic_error", error_message=str(e))
    finally:
        # Always go back after search attempt
        handle_menu_back()

def handle_find_note_input():
    """Gets search term, finds notes, displays them."""
    global notebook
    path_str = get_path_string()
    try:
        term = v.get_input("prompt_enter_search_term", path_info=path_str)
        if not term:
            v.display_warning("input_cancelled")
            handle_menu_back()
            return

        # Search across title, content, and tags
        results_title_content = notebook.find_notes(term) # Searches title and content
        results_tag = notebook.find_note_by_tag(term)

        # Combine results and remove duplicates using Note's hash implementation
        combined_results_map = {note.id: note for note in results_title_content + results_tag}
        combined_results = list(combined_results_map.values())

        v.display_info("notes_found_title", count=len(combined_results))
        # display_notes handles the case where combined_results is empty
        v.display_notes(combined_results, show_indices=False) # Don't show indices for search results

    except Exception as e:
        v.display_error("generic_error", error_message=str(e))
    finally:
        # Always go back after search attempt
        handle_menu_back()

def handle_birthdays_input():
    """Gets number of days, finds birthdays, displays them."""
    global address_book
    path_str = get_path_string()
    days_str = v.get_input("prompt_enter_days", path_info=path_str) # Get input first
    if not days_str:
        v.display_warning("input_cancelled")
        handle_menu_back()
        return

    try:
        # Attempt conversion and validation
        days = int(days_str)
        # Validation of days range (1-365)
        if not (0 < days <= 365):
            # Use specific error key from messages
            raise ValueError("invalid_days_range") # Raise ValueError to be caught below

        # If days are valid, proceed to get results
        results = address_book.get_birthdays_in_next_days(days)
        v.display_birthdays(results) # View handles empty list message

    except ValueError as e:
         # Handle non-integer input or range error
         # Use the specific error key if it's our custom ValueError, else generic invalid_number
         error_key = str(e) if str(e) == "invalid_days_range" else "invalid_number"
         v.display_error(error_key)
         # Stay in the same state to allow retry? Or go back? Let's stay for retry.
         # handle_menu_back() # Remove this to allow retry without re-typing 'birthdays'
         return # Exit this attempt, loop will prompt again

    except Exception as e:
        # Catch any unexpected errors during processing
        v.display_error("generic_error", error_message=str(e))
        handle_menu_back() # Go back on unexpected error
    else:
        # Go back only on successful display of birthdays
        handle_menu_back()


# ================ Help Handler ================

def handle_help():
    """Displays context-sensitive help."""
    global current_path
    commands = {} # Default empty
    state = tuple(current_path)

    # --- Define help messages based on state ---
    if not state:
         commands = { # Main menu commands
              "add [contact|note]": "Add a new contact or note.",
              "find [contact|note]": "Search contacts or notes.",
              "birthdays": "Show upcoming birthdays.",
              "change [contact|note]": "Modify an existing contact or note (Not fully implemented).",
              "remove [contact|note]": "Delete a contact or note (Not fully implemented).",
              "help": "Show this help message.",
              "menu": "Go back (no effect here).",
              "exit / quit / q": "Save data and exit."
         }
    elif state == ("add",):
        commands = {
            "contact": "Start adding a new contact.",
            "note": "Start adding a new note.",
            "menu": "Go back to the main menu.",
            "help": "Show this help message."
            }
    elif state == ("find",):
        commands = {
            "contact": "Search for contacts.",
            "note": "Search for notes.",
            "menu": "Go back to the main menu.",
            "help": "Show this help message."
            }
    # Add more states as needed (e.g., change, remove, specific edit contexts)
    # elif state == ("change",): ...
    # Contexts like ("add", "contact") are handled by input prompts, not direct commands here
    # elif state == ("add", "contact"):
    #    commands = {"menu": "Cancel adding contact."}
    # elif state == ("find", "contact"):
    #    commands = {"menu": "Cancel search."}
    elif state == ("birthdays",): # User is prompted for days
       commands = {
           "[number 1-365]": "Enter the number of days for upcoming birthdays.",
           "menu": "Cancel birthday search."
           }


    # Pass the generated commands map to the view
    v.display_help(commands)

# ================ Helper/Validation Functions ================

def validate_and_parse_birthday(date_str: str) -> date:
    """ Tries to parse DD.MM.YYYY and validates the date logic. Returns date or raises BirthdayError."""
    try:
        # strptime checks format and basic date validity (e.g., day/month ranges)
        dt_obj = datetime.strptime(date_str, "%d.%m.%Y")
        # Additional check: Don't allow future dates (relative to today)
        if dt_obj.date() > date.today():
            # Reuse range error key? Or create a new one? Let's reuse range.
            raise m.BirthdayError("invalid_birthday_range")
        return dt_obj.date()
    except ValueError:
        # Use a specific key for format/logic errors from strptime
        raise m.BirthdayError("invalid_date_logic")
    # BirthdayError("invalid_birthday_range") is raised above if needed


# ================ Main Loop ================

def run():
    """Main application loop."""
    global is_running, current_path, operation_cache, address_book, notebook

    initialize() # Load data and set initial state

    while is_running:
        path_str = get_path_string()
        state = tuple(current_path)
        current_prompt_key = "command_prompt" # Default prompt

        # --- Determine prompt based on state ---
        # This logic determines WHAT the user should be asked for *if* they are in a choice menu
        if state == ("add",): current_prompt_key = "prompt_add_type"
        elif state == ("find",): current_prompt_key = "prompt_find_type"
        # Other states like ('birthdays',) or ('add', 'contact') are handled
        # by their specific input handlers which use their own prompts via v.get_input

        # Get input from the user using the appropriate prompt for the state
        # Note: Specific input handlers might override this with their own prompts
        user_input = v.get_input(current_prompt_key, path_info=path_str)
        command, args = parse_input(user_input)

        # --- Universal command handling (works in any state) ---
        if command == "menu":
            handle_menu_back()
            continue
        if command in ["exit", "quit", "q"]:
            quit_application()
            continue # is_running will be False, loop terminates
        if command == "help":
            handle_help()
            continue

        # --- State-based command/input handling ---
        try:
            state = tuple(current_path) # Re-evaluate state after potential navigation commands

            # --- Top Level (No current path) ---
            if not state:
                if command == "add": handle_add_base(args)
                elif command == "find": handle_find_base(args)
                elif command == "birthdays": handle_birthdays_base(args); handle_birthdays_input() # Directly ask for days
                # elif command == "change": handle_change_base(args) # TODO
                # elif command == "remove": handle_remove_base(args) # TODO
                elif command == "": pass # Ignore empty input at top level
                else: v.display_error("invalid_command")

            # --- 'add' Menu ---
            elif state == ("add",):
                if command == "contact":
                    current_path.append("contact") # Change state first
                    handle_add_contact_input() # Then call handler to get data
                elif command == "note":
                    current_path.append("note") # Change state first
                    handle_add_note_input() # Then call handler to get data
                elif command == "": pass # Ignore empty input
                else: v.display_error("invalid_type") # Expecting 'contact' or 'note'

            # --- 'find' Menu ---
            elif state == ("find",):
                if command == "contact":
                    current_path.append("contact") # Change state first
                    handle_find_contact_input() # Call handler to get search term
                elif command == "note":
                    current_path.append("note") # Change state first
                    handle_find_note_input() # Call handler to get search term
                elif command == "": pass # Ignore empty input
                else: v.display_error("invalid_type") # Expecting 'contact' or 'note'

            # --- 'birthdays' state ---
            elif state == ("birthdays",):
                # This state is now mostly handled by handle_birthdays_input called from top level
                # If user types something other than 'menu' or 'help', treat it as days input attempt
                 if command not in ["", "menu", "help"]: # Check if it's not handled universally
                    # Re-parse the input in case it was the number
                    handle_birthdays_input() # Let the handler process user_input again
                 elif command == "": pass # Ignore empty input here too
                 # Menu/Help are handled globally

            # --- Add handlers for other states like 'change', 'remove' ---
            # Note: States like ('add', 'contact') are transient; the input handlers
            #       are called directly and manage their own input prompts, then call handle_menu_back().
            #       So, we don't typically need explicit state checks for them in the main loop.

            else:
                # If somehow in an unhandled state, display error
                 if command: # If the user typed something
                     v.display_error("invalid_command_for_state")
                 # If user just pressed Enter (empty command), do nothing

        # --- Error Handling ---
        except (m.ContactError, m.PhoneError, m.EmailError, m.BirthdayError,
                m.TitleError, m.TagError, m.NotFoundError, m.NoteError, IndexError) as e:
            # Model validation errors or logical errors like NotFoundError, IndexError
            error_key = str(e)
            # Attempt to pass kwargs if the exception holds them
            error_kwargs = getattr(e, 'kwargs', {})
            v.display_error(error_key, **error_kwargs)
            # Decide whether to go back after error. Let's generally NOT go back
            # on validation errors to allow user retry without full navigation.
            # handle_menu_back() # Optional: go back after specific errors if desired

        except ValueError as e:
             # Catch errors specifically from controller logic (e.g., int conversion in handle_birthdays_input)
             # These are often displayed within the handler itself now. Re-displaying might be redundant.
             # Check if it's a message key we know.
             error_key = str(e) if str(e) in v.MESSAGES else "invalid_number" # Fallback
             v.display_error(error_key)
             # handle_menu_back() # Optional: go back after error

        except Exception as e: # Catch-all for unexpected errors
             v.display_error("generic_error", error_message=f"{type(e).__name__}: {e}")
             # Go back after an unexpected error to reset state
             handle_menu_back()


if __name__ == "__main__":
    import main
    main.main()