# View file by MVC pattern
# This file contains the view of the app

from datetime import date
from model import Contact, Note

# ================ ANSI Color Codes ================
# (Can be expanded or made OS-dependent if needed)
RESET   = '\033[0m'
BOLD    = '\033[1m'
RED     = '\033[91m'
GREEN   = '\033[92m'
YELLOW  = '\033[93m'
BLUE    = '\033[94m'
MAGENTA = '\033[95m'
CYAN    = '\033[96m'

# ================ Message Dictionary ================
# Stores message templates. Keys are used by Controller, values are displayed by View.
# Include emojis and ANSI codes directly here.
MESSAGES: dict[str, str] = {
    # --- General Messages ---
    "welcome"               : f"{GREEN}👋 Welcome to the Assistant Bot!{RESET}",
    "goodbye"               : f"{YELLOW}👋 Goodbye! See you next time.{RESET}",
    "command_prompt"        : f"{CYAN}Enter command: {RESET}",
    "invalid_command"       : f"{RED}❌ Invalid command. Type 'help' to see available commands.{RESET}",
    "confirm_prompt"        : f"{YELLOW}❔ Are you sure? (yes/no): {RESET}",
    "yes": "yes", # Expected confirmation input
    "no": "no",   # Expected rejection input

    # --- Input Prompts (using .format(path=path_info)) ---
    "input_prompt_default": "{path} / {prompt}: ",
    "input_path_separator": " > ",

   # --- Success Messages ---
"contact_added"          : f"{GREEN}✅ Contact added successfully!{RESET}",
"note_saved"             : f"{GREEN}📝 Note saved successfully!{RESET}",
"contact_deleted"        : f"{GREEN}🗑️ Contact deleted.{RESET}",
"note_deleted"           : f"{GREEN}🗑️ Note deleted.{RESET}",
"data_updated"           : f"{GREEN}✅ Data updated successfully.{RESET}",

# --- Info/Title Messages ---
"no_notes_found"         : f"{YELLOW}📭 No notes to display.{RESET}",
"no_upcoming_birthdays"  : f"{YELLOW}🎂 No upcoming birthdays.{RESET}",
"birthdays_found_title"  : f"{BLUE}🎉 Upcoming Birthdays:{RESET}",
"contacts_list_title"    : f"{BLUE}📇 Contact List:{RESET}",
"notes_list_title"       : f"{BLUE}📒 Notes List:{RESET}",
"help_intro"             : f"{BLUE}🔧 Available commands:{RESET}",

# --- Warning Messages ---
"field_required"         : f"{YELLOW}⚠️ This field is required!{RESET}",
"confirm_deletion"       : f"{YELLOW}⚠️ Are you sure you want to delete this entry?{RESET}",
"duplicate_entry"        : f"{YELLOW}⚠️ This entry already exists.{RESET}",

# --- Error Messages ---
"not_found"              : f"{RED}❌ Entry not found.{RESET}",
"empty_input"            : f"{RED}❌ Empty input provided.{RESET}",
"invalid_date"           : f"{RED}❌ Invalid date format. Use DD.MM.YYYY.{RESET}",
"generic_error"          : f"{RED}❌ An error occurred. Please try again.{RESET}",
"invalid_choice"         : f"{RED}❌ Invalid choice. Please try again.{RESET}",
"invalid_yes_no"         : f"{RED}❌ Please enter 'yes' or 'no'.{RESET}",
"eof_exit_warning": f"{RED}👋 Exit signal received. Exiting program.{RESET}",
"keyboard_interrupt_warning": f"{RED}⛔ Program interrupted by user. Exiting...{RESET}",

}

# ================ Display Functions ================

def _get_message(key: str, **kwargs) -> str:
    """Helper to get and format messages from the dictionary."""
    message_template = MESSAGES.get(key, MESSAGES["generic_error"])
    try:
        return message_template.format_map(kwargs)
    except KeyError as e:
        pass

def display_success(message_key: str, **kwargs):
    """Displays a success message."""
    print(_get_message(message_key, **kwargs))

def display_warning(message_key: str, **kwargs):
    """Displays a warning message."""
    print(_get_message(message_key, **kwargs))

def display_error(message_key: str, **kwargs):
    """Displays an error message."""
    print(_get_message(message_key, **kwargs))

def display_info(message_key: str, **kwargs):
    """Displays an informational message or title."""
    # Special handling for titles that might include counts
    count = kwargs.get('count', None)
    print(_get_message(message_key, count=count, **kwargs))


def display_contacts(contacts: list[Contact]):
    """Displays a list of contacts with 1-based indexing."""
    # TODO: Implement detailed contact formatting with colors, fields, and 1-based indices.
    #    ...
    for idx, contact in enumerate(contacts, start=1):
        print(f"{BOLD}{CYAN}{idx}. {contact.name}{RESET}")
        for phone in contact.phones:
            print(f"   📞 Phone: {phone}")
        if contact.email:
            print(f"   📧 Email: {contact.email}")
        if contact.birthday:
            print(f"   🎂 Birthday: {contact.birthday.strftime('%d.%m.%Y')}")
        if contact.address:
            print(f"   🏠 Address: {contact.address}")
        print("-" * 40)


def display_notes(notes: list[Note]):
    """Displays a list of notes with 1-based indexing."""
    # TODO: Implement detailed note formatting with colors, fields, tags, and 1-based indices.
    # Example structure:
    # 1. [ID: 0] Title: Shopping List
    #      Tags: #groceries #urgent
    #      Content: Milk, Bread, Eggs...
    # --------------------
    # 2. [ID: 1] Title: Meeting Notes
    #      ...
    if not notes:
        display_info("no_notes_found")
        return
    for index, note in enumerate(notes, start=1):
        # Probably use note.__repr__() for now, replace with proper formatting
        print(f"{BOLD}{index}.{RESET} {note!r}")
        if note.tags:
            print(f"   🏷️ Tags: {' '.join(f'#{tag}' for tag in note.tags)}")
        print(f"   📄 Content: {note.content}")
        print("-" * 40)


def display_birthdays(birthday_results: list[tuple[date | None]]):
    """Displays upcoming birthdays with celebration dates."""
    # TODO: Implement formatting for birthday list.
    # Example structure:
    # Upcoming Birthdays:
    # - John Doe: 15.08 (Celebration: 15.08)
    # - Jane Smith: 20.08 (Weekend Birthday - Celebration: Monday 22.08)
    if not birthday_results:
        display_info("no_upcoming_birthdays")
        return
    display_info("birthdays_found_title")
    # TODO: Implement the actual display logic
    for name, birth_date, celebration_date in birthday_results:
        orig = birth_date.strftime("%d.%m")
        celebr = celebration_date.strftime("%A %d.%m")
        print(f"🎂 {name}: {orig} (Celebration: {celebr})")


def display_help():
    """Displays available commands and their descriptions."""
    # TODO: Implement formatting for help message
    print(f"{BLUE}Available Commands:{RESET}")
    # ...
    pass

# ================ Input Functions ================

def get_input(prompt_key: str, path_info: str = "", **prompt_kwargs) -> str:
    """Gets user input with a formatted prompt including the menu path."""
    # Construct the prompt with path
    path_display = path_info + MESSAGES["input_path_separator"] if path_info else ""
    prompt_text = _get_message(prompt_key, **prompt_kwargs)
    full_prompt = MESSAGES["input_prompt_default"].format(path=path_display, prompt=prompt_text)

    user_input = input(full_prompt)
    return user_input.strip()

def get_confirmation(prompt_key: str, **prompt_kwargs) -> bool:
    """Gets a 'yes' or 'no' confirmation from the user."""
    # TODO: Add loop for invalid input if needed
    while True:
        answer = get_input(prompt_key, "", **prompt_kwargs).lower()
        if answer == MESSAGES["yes"]:
            return True
        elif answer == MESSAGES["no"]:
            return False
        else:
            display_error("invalid_command") # Or a specific "invalid_yes_no" message



if __name__ == "__main__":
    import main
    main.main()