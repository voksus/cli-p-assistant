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

SEPARATOR_LINE = "-" * 40
TITLE_SEPARATOR = "-" * 20

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
"message_formatting_error": f"{RED}❌ Error formatting message '{{key}}': Missing key {{error_key}}.{RESET}",
"generic_formatting_error": f"{RED}❌ Error formatting message '{{key}}': {{error}}.{RESET}",

# --- Contact Messages ---
"contact_list_title": f"{BLUE}📇 Contact List:{RESET}",
"contact_list_item": "{bold_index}. Contact: {cyan_name}{reset}",
"contact_list_item_simple": "{bold_index}. {cyan_name}{reset}",
"contact_phones": " Phones: {phones}",
"contact_no_phones": " Phones: No phone numbers",
"contact_emails": " Emails: {emails}",
"contact_no_emails": " Emails: No email addresses",
"contact_birthday": " Birthday: {birthday}",
"contact_no_birthday": " Birthday: No birthday specified",
"invalid_birthday_format": " Birthday: Invalid date format",
"phone_with_index": f"{CYAN}[{{index}}]{RESET}: {{phone}}",

# --- Note Messages ---
"no_notes_found": f"{YELLOW}📭 No notes to display.{RESET}",
"notes_list_title": f"{BLUE}📒 Notes List:{RESET}",
"note_item_detailed": "{bold_index}. Title: {green_title}{reset}",
"note_tags_detailed": "     Tags: {yellow_tags}{reset}",
"note_content_detailed": "     Content: {content_preview}",

# --- Birthday Messages ---
"no_upcoming_birthdays": f"{YELLOW}🎂 No upcoming birthdays.{RESET}",
"birthdays_found_title": f"{BLUE}🎉 Upcoming Birthdays:{RESET}",
"birthday_celebration_adjusted": "{name}'s birthday is on {bday} ({bday_weekday}), celebrating on {celeb_day} ({celeb_weekday}).",
"birthday_celebration_on_day": "{name}'s birthday is on {bday} ({bday_weekday}).",

}

# ================ Display Functions ================

def _get_message(key: str, **kwargs) -> str:
    """Helper to get and format messages from the dictionary."""
    message_template = MESSAGES.get(key, MESSAGES["generic_error"])
    
    try:
        return message_template.format_map(kwargs)
    except KeyError as e:
            return MESSAGES["message_formatting_error"].format(key=key, error_key=e)
    except Exception as e:
        return MESSAGES["generic_formatting_error"].format(key=key, error=e)

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
    """Displays an informational message or title with an emoji."""
    emoji = "ℹ️ "  # Інформаційний емодзі
    count = kwargs.get('count', None)
    print(f"{emoji}{_get_message(message_key, count=count, **kwargs)}")

def display_contacts(contacts: list[Contact]):
    """Displays a list of contacts with 1-based indexing."""
    if not contacts:
        display_info("no_contacts_found")
        return

    display_info("contact_list_title")
    print(SEPARATOR_LINE)
    for index, contact in enumerate(contacts, start=1):
        print(MESSAGES["contact_list_item_simple"].format(
            bold_index=f"{BOLD}{index}",
            cyan_name=f"{CYAN}{contact.name}",
            reset=RESET
        ))
        if contact.phones:
            phones_str = ", ".join(MESSAGES["phone_with_index"].format(index=i + 1, phone=p) for i, p in enumerate(contact.phones))
            print(MESSAGES["contact_phones"].format(phones=phones_str))
        else:
            print(MESSAGES["contact_no_phones"])

        if contact.emails:
            emails_str = ", ".join(contact.emails)
            print(MESSAGES["contact_emails"].format(emails=emails_str))
        else:
            print(MESSAGES["contact_no_emails"])

        if contact.birthday:
            try:
                birthday_str = contact.birthday.strftime('%d.%m.%Y')
                print(MESSAGES["contact_birthday"].format(birthday=birthday_str))
            except AttributeError:
                print(MESSAGES["invalid_birthday_format"])
        else:
            print(MESSAGES["contact_no_birthday"])

    print(SEPARATOR_LINE)
        
                

def display_notes(notes: list[Note]):
    """Displays a list of notes with 1-based indexing."""
    if not notes:
        display_info("no_notes_found")
        return
        
        
    display_info("note_list_title")
    print(SEPARATOR_LINE)
    for index, note in enumerate(notes, start=1):
        print(MESSAGES["note_item_detailed"].format(
            bold_index=f"{BOLD}{index}",
            green_title=f"{GREEN}{note.title}",
            reset=RESET
        ))
        if note.tags:
            tags_str = " ".join([f"#{tag}" for tag in note.tags])
            print(MESSAGES["note_tags_detailed"].format(yellow_tags=f"{YELLOW}{tags_str}", reset=RESET))
        if note.content:
            ## Trim long content for preview
            content_preview = note.content[:100] + ('...' if len(note.content) > 100 else '')
            # Output the content with indentation, possibly handling line breaks
            print(MESSAGES["note_content_detailed"].format(content_preview=content_preview.replace(chr(10), chr(10) + ' ' * 15)))
            
        print(SEPARATOR_LINE)   

def display_birthdays(birthday_results: list[tuple[Contact, date | None]]):
    """Displays upcoming birthdays with celebration dates."""
    if not birthday_results:
        display_info("no_upcoming_birthdays")
        return

    display_info("birthdays_found_title")

    for contact, celebration_date in birthday_results:
        original_bday_str = contact.birthday.strftime('%d.%m')
        weekday_name     = contact.birthday.strftime('%A')

        if celebration_date:
            celebration_day_str = celebration_date.strftime('%d.%m')
            celebration_weekday = celebration_date.strftime('%A')

            message = _get_message(
                "birthday_celebration_adjusted",
                name=contact.name,
                bday=original_bday_str,
                bday_weekday=weekday_name,
                celeb_weekday=celebration_weekday,
                celeb_day=celebration_day_str
            )
        else:
            message = _get_message(
                "birthday_celebration_on_day",
                name=contact.name,
                bday=original_bday_str,
                bday_weekday=weekday_name
            )

        print(f"- {message}")

def display_help(command_map= None): #command structure as an argument
    """Displays available commands and their descriptions."""
    display_info("help_title")
    
    if command_map is None:
        print("  Help information is currently unavailable.")
        return
    print(f"  {YELLOW}Usage: command [arguments...]{RESET}")
    print(SEPARATOR_LINE)
    
    for command, details in command_map.items():
        description = details.get('description', 'No description available.') if isinstance(details, dict) else details
        example = details.get('example', '') if isinstance(details, dict) else ''
        
        print(f"  {BOLD}{command}{RESET}:")
        print(f"    {description}")
        if example:
             print(f"    {CYAN}Example: {example}{RESET}")
        print(TITLE_SEPARATOR)

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