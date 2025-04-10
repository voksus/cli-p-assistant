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

}

# ================ Display Functions ================

def _get_message(key: str, **kwargs) -> str:
    """Helper to get and format messages from the dictionary."""
    message_template = MESSAGES.get(key, MESSAGES["generic_error"])
    try:
        return message_template.format_map(kwargs)
    except KeyError as e:
        return f"Error formatting message '{key}': Missing key {e} "
    except Exception as e:
        return f"Error formatting message '{key}': {e}"

def display_success(message_key: str, **kwargs):
    """Displays a success message."""
    print(f"{GREEN}{_get_message(message_key, **kwargs)}{RESET}")

def display_warning(message_key: str, **kwargs):
    """Displays a warning message."""
    print(f"{YELLOW}{_get_message(message_key, **kwargs)}{RESET}")

def display_error(message_key: str, **kwargs):
    """Displays an error message."""
    print(f"{RED}{_get_message(message_key, **kwargs)}{RESET}")

def display_info(message_key: str, **kwargs):
    """Displays an informational message or title."""
    # Special handling for titles that might include counts
    count = kwargs.get('count', None)
    print(f"{BLUE}{_get_message(message_key, **kwargs)}{RESET}")

def display_contacts(contacts: list[Contact]):
    """Displays a list of contacts with 1-based indexing."""
    if not contacts:
        display_info("no_contacts_found")
        return
    
    display_info("contact_list_title")
    print("-" * 40) #Separator
    for index, contact in enumerate(contacts, start = 1):
        print(f"{BOLD}{index}.{RESET}{CYAN}[ID: {contact.id}] Name: {contact.name}{RESET}")
        if contact.phones:
            phones_str = ", ".join(contact.phones)
            print(f" Phones:{phones_str}")
        if contact.emails:
            emails_str = ", ".join(contact.emails)
            print(f" Emails:{emails_str}")
        if contact.birthday:
            try:
                birthday_str = contact.birthday.strftime('%d.%m.%Y')
                print(f"  Birthday: {birthday_str}")
            except AttributeError:
                print(f" Birthday: Invalid format date for contact ID {contact.id}")
        print("-" * 40)
        
                

def display_notes(notes: list[Note]):
    """Displays a list of notes with 1-based indexing."""
    if not notes:
        display_info("no_notes_found")
        return
        
        
    display_info("note_list_title")
    print("-" * 40)
    for index, note in enumerate(notes, start=1):
        # Probably use note.__repr__() for now, replace with proper formatting
        print(f"{BOLD}{index}.{RESET}{GREEN}[ID: {note.id}] Title: {note.title}{RESET}")
        if note.tags:
            tags_str = "".join([f"#{tag}" for tag in note.tags])
            print(f"       Tags: {YELLOW}{tags_str}{RESET}")
        if note.content:
            ## Trim long content for preview
            content_preview = note.content[:100] + ('...' if len(note.content) > 100 else '')
            # Output the content with indentation, possibly handling line breaks
            print(f"      Content: {content_preview.replace(chr(10), chr(10) + ' ' * 15)}")
            
        print("-" * 40)   

def display_birthdays(birthday_results: list[tuple[date | None]]):
    """Displays upcoming birthdays with celebration dates."""
    
    if not birthday_results:
        display_info("no_upcoming_birthdays")
        return
    display_info("birthdays_found_title")
    for contact, celebration_date in birthday_results:
        try:
            original_bday_str = contact.birthday.strftime('%d.%m') 
            weekday_name = contact.birthday.strftime('%A')
            
            if celebration_date:
               celebration_day_str = celebration_date.strftime('%d.%m')
               celebration_weekday = celebration_date.strftime('%A') 
               message = _get_message("birthday_celebration_adjusted",
                                      name=contact.name,
                                      bday=original_bday_str,
                                      bday_weekday=weekday_name,
                                      celeb_weekday=celebration_weekday)
               print(f"- {message}")
            else: 
                #use our key from dictionary MESSAGE
                message = _get_message("birthday_celebration_on_day",
                                        name=contact.name,
                                        bday=original_bday_str,
                                        bday_weekday=weekday_name)
                print(f"- {message}")
        except ArithmeticError:
            print(f"- Error processing birthday for contact: {contact.name} (ID: {contact.id})")
            #when we don't have key in MESSAGES
        except KeyError as e:
            print(f"- Error displaying birthday: Missing message key {e}")

def display_help(command_map= None): #command structure as an argument
    """Displays available commands and their descriptions."""
    display_info("help_title")
    
    if command_map is None:
        print("  Help information is currently unavailable.")
        return
    print(f"  {YELLOW}Usage: command [arguments...]{RESET}")
    print("-" * 40)
    
    for command, details in command_map.items():
        description = details.get('description', 'No description available.') if isinstance(details, dict) else details
        example = details.get('example', '') if isinstance(details, dict) else ''
        
        print(f"  {BOLD}{command}{RESET}:")
        print(f"    {description}")
        if example:
             print(f"    {CYAN}Example: {example}{RESET}")
        print("-" * 20)

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