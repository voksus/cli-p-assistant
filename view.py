# View file by MVC pattern
# This file contains the view of the app

from datetime import date

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
    "welcome"                  : f"{GREEN}👋 Welcome to the Assistant Bot!{RESET}",
    "goodbye"                  : f"{YELLOW}👋 Goodbye! See you next time.{RESET}",
    "command_prompt"           : f"Enter command", # Prompt text only, path added separately
    "invalid_command"          : f"{RED}❌ Invalid command. Type 'help' to see available commands.{RESET}",
    "confirm_prompt"           : f"{YELLOW}❔ Are you sure? (yes/no): {RESET}",
    "yes"                      : "yes", # Expected confirmation input
    "no"                       : "no",   # Expected rejection input
    "input_cancelled"          : f"{YELLOW}Input cancelled.{RESET}",
    "already_at_main_menu"     : f"{YELLOW}You are already at the main menu.{RESET}",
    "invalid_command_for_state": f"{RED}❌ Command not applicable in this context. Type 'help' or 'menu'.{RESET}",

    # --- Input Prompts (Keys used by Controller, value is the specific question/prompt part) ---
    "prompt_add_type"          : "Add 'contact' or 'note'?",
    "prompt_change_type"       : "Change 'contact' or 'note'?",
    "prompt_remove_type"       : "Remove 'contact' or 'note'?",
    "prompt_find_type"         : "Find 'contact' or 'note'?",
    "prompt_enter_name"        : "Enter contact name",
    "prompt_enter_phones"      : "Enter phone numbers (10 digits, space-separated)",
    "prompt_enter_emails"      : "Enter email addresses (space-separated)",
    "prompt_enter_birthday"    : "Enter birthday (DD.MM.YYYY, optional)",
    "prompt_enter_title"       : "Enter note title",
    "prompt_enter_content"     : "Enter note content (press Enter twice to finish)", # Example for multiline
    "prompt_enter_tags"        : "Enter tags (space-separated, letters/numbers/_)",
    "prompt_enter_search_term" : "Enter search term",
    "prompt_enter_days"        : "Enter number of days for upcoming birthdays (1-365)",
    "prompt_select_index_to_change" : "Enter number of item to change",
    "prompt_select_index_to_remove" : "Enter number of item to remove",
    "prompt_what_to_change_contact" : "What to change? (name, phone, email, birthday, menu)", # Simplified
    "prompt_what_to_change_note"    : "What to change? (title, content, tag, menu)", # Simplified

    # --- Input Path Formatting ---
    "input_prompt_default" : "{path}{separator}{prompt}: ", # Combined path and prompt
    "input_path_separator" : " > ",

    # --- Success Messages ---
    "contact_added"   : f"{GREEN}✅ Contact '{{name}}' added successfully!{RESET}",
    "note_added"      : f"{GREEN}📝 Note '{{title}}' added successfully!{RESET}",
    "contact_deleted" : f"{GREEN}🗑️ Contact '{{name}}' deleted.{RESET}",
    "note_deleted"    : f"{GREEN}🗑️ Note '{{title}}' deleted.{RESET}",
    "data_updated"    : f"{GREEN}✅ Data updated successfully.{RESET}",
    "phone_added"     : f"{GREEN}✅ Phone '{{phone}}' added to contact '{{name}}'.{RESET}",
    "phone_changed"   : f"{GREEN}✅ Phone changed to '{{phone}}' for contact '{{name}}'.{RESET}",
    "phone_removed"   : f"{GREEN}✅ Phone removed from contact '{{name}}'.{RESET}",
    "email_added"     : f"{GREEN}✅ Email '{{email}}' added to contact '{{name}}'.{RESET}",
    "email_changed"   : f"{GREEN}✅ Email changed to '{{email}}' for contact '{{name}}'.{RESET}",
    "email_removed"   : f"{GREEN}✅ Email removed from contact '{{name}}'.{RESET}",
    "birthday_set"    : f"{GREEN}✅ Birthday set to {{birthday}} for contact '{{name}}'.{RESET}",
    "birthday_removed": f"{GREEN}✅ Birthday removed for contact '{{name}}'.{RESET}",
    "title_changed"   : f"{GREEN}✅ Note title changed to '{{title}}'.{RESET}",
    "content_changed" : f"{GREEN}✅ Note content updated for '{{title}}'.{RESET}",
    "tag_added"       : f"{GREEN}✅ Tag '{{tag}}' added to note '{{title}}'.{RESET}",
    "tag_removed"     : f"{GREEN}✅ Tag '{{tag}}' removed from note '{{title}}'.{RESET}",

    # --- Info/Title Messages ---
    "no_contacts_found"     : f"{YELLOW}📭 No contacts found.{RESET}",
    "no_notes_found"        : f"{YELLOW}📭 No notes to display.{RESET}",
    "no_upcoming_birthdays" : f"{YELLOW}🎂 No upcoming birthdays in the specified period.{RESET}",
    "birthdays_found_title" : f"{BLUE}🎉 Upcoming Birthdays:{RESET}",
    "contacts_list_title"   : f"{BLUE}📇 Contact List:{RESET}",
    "notes_list_title"      : f"{BLUE}📒 Notes List:{RESET}",
    "help_title"            : f"{BLUE}🔧 Available commands:{RESET}", # Changed key from help_intro
    "contacts_found_title"  : "Contacts found: {count}",
    "notes_found_title"     : "Notes found: {count}",

    # --- Warning Messages ---
    "field_required"   : f"{YELLOW}⚠️ This field is required!{RESET}",
    "confirm_deletion" : f"{YELLOW}⚠️ Are you sure you want to delete this entry?{RESET}", # Maybe add item info
    "duplicate_entry"  : f"{YELLOW}⚠️ This entry already exists.{RESET}", # Generic, specific below
    "tags_already_exist": f"{YELLOW}⚠️ Tag(s) {{tags_repeat}} already exist in the note.{RESET}", # Example for tag warning

    # --- Error Messages (using keys from Model Exceptions where possible) ---
    "not_found"                : f"{RED}❌ Entry not found.{RESET}", # Generic
    "contact_not_found"        : f"{RED}❌ Contact not found.{RESET}",
    "note_not_found"           : f"{RED}❌ Note '{{title}}' not found.{RESET}",
    "tag_not_found_in_note"    : f"{RED}❌ Tag '{{tag}}' not found in note '{{title}}'.{RESET}",
    "contact_not_found_in_list": f"{RED}❌ Contact could not be removed (not found in list).{RESET}",
    "empty_input"              : f"{RED}❌ Empty input provided where value is required.{RESET}",
    "invalid_date"             : f"{RED}❌ Invalid date format. Use DD.MM.YYYY.{RESET}",
    "invalid_date_logic"       : f"{RED}❌ Invalid date logic (e.g., Feb 31).{RESET}", # For strptime errors
    "invalid_days_range"       : f"{RED}❌ Number of days must be between 1 and 365.{RESET}",
    "invalid_number"           : f"{RED}❌ Invalid input, please enter a number.{RESET}",
    # *** FIXED: generic_error now includes the error message ***
    "generic_error"            : f"{RED}❌ An unexpected error occurred: {{error_message}}{RESET}",
    "invalid_choice"           : f"{RED}❌ Invalid choice. Please try again.{RESET}",
    "invalid_yes_no"           : f"{RED}❌ Please enter 'yes' or 'no'.{RESET}",
    "invalid_type"             : f"{RED}❌ Invalid type. Enter 'contact' or 'note'.{RESET}",
    "message_formatting_error" : f"{RED}❌ Error formatting message '{{key}}': Missing key {{error_key}}.{RESET}",
    "generic_formatting_error" : f"{RED}❌ Error formatting message '{{key}}': {{error}}{RESET}",

    # --- Contact Specific Errors ---
    "invalid_name_format"     : f"{RED}❌ Invalid name format. Use letters, spaces, hyphens, apostrophes.{RESET}",
    "duplicate_contact"       : f"{RED}❌ A contact with this name already exists.{RESET}",
    "invalid_phone_format"    : f"{RED}❌ Invalid phone format. Must be 10 digits.{RESET}",
    "duplicate_phone"         : f"{RED}❌ This phone number already exists for this contact.{RESET}",
    "invalid_phone_index"     : f"{RED}❌ Invalid phone number index.{RESET}",
    "invalid_email_format"    : f"{RED}❌ Invalid email format.{RESET}",
    "duplicate_email"         : f"{RED}❌ This email address already exists for this contact.{RESET}",
    "invalid_email_index"     : f"{RED}❌ Invalid email index.{RESET}",
    "invalid_birthday_format" : f"{RED}❌ Invalid birthday format. Use DD.MM.YYYY.{RESET}", # Used by controller validation
    "invalid_birthday_range"  : f"{RED}❌ Birthday year must be between 1900 and today.{RESET}",
    "invalid_birthday_object" : f"{RED}❌ Internal error: Invalid birthday data.{RESET}", # Should not happen normally

    # --- Note Specific Errors ---
    "invalid_title_length"  : f"{RED}❌ Title length must be between {{min}} and {{max}} characters.{RESET}",
    "duplicate_title"       : f"{RED}❌ A note with title '{{title}}' already exists.{RESET}",
    "invalid_tag_length"    : f"{RED}❌ Tag length must be between {{min}} and {{max}} characters.{RESET}",
    "invalid_tag_format"    : f"{RED}❌ Invalid tag format. Use letters, numbers, or underscore.{RESET}",
    "duplicate_tag_in_note" : f"{RED}❌ Tag '{{tag}}' already exists in note '{{title}}'.{RESET}",

    # --- Contact Display ---
    "contact_list_title"       : f"{BLUE}📇 Contact List:{RESET}",
    "contact_list_item"        : "{bold_index}. Contact: {cyan_name}{reset}", # Less used now
    "contact_list_item_simple" : "{bold_index}. {cyan_name}{reset}",
    "contact_phones"           : " Phones: {phones}",
    "contact_no_phones"        : " Phones: No phone numbers",
    "contact_emails"           : " Emails: {emails}",
    "contact_no_emails"        : " Emails: No email addresses",
    "contact_birthday"         : " Birthday: {birthday}",
    "contact_no_birthday"      : " Birthday: No birthday specified",
    "phone_with_index"         : f"{CYAN}[{{index}}]{RESET}: {{phone}}",
    "email_with_index"         : f"{CYAN}[{{index}}]{RESET}: {{email}}", # Added for consistency

    # --- Note Display ---
    "notes_list_title"      : f"{BLUE}📒 Notes List:{RESET}",
    "note_item_detailed"    : "{bold_index}. Title: {green_title}{reset}",
    "note_tags_detailed"    : "     Tags: {yellow_tags}{reset}",
    "note_content_detailed" : "     Content: {content_preview}",

    # --- Birthday Display ---
    "birthdays_found_title"         : f"{BLUE}🎉 Upcoming Birthdays:{RESET}",
    "birthday_celebration_adjusted" : "{name}'s birthday is on {bday} ({bday_weekday}), celebrating on {celeb_day} ({celeb_weekday}).",
    "birthday_celebration_on_day"   : "{name}'s birthday is on {bday} ({bday_weekday}).",
}

# ================ Display Functions ================

def _get_message(key: str, **kwargs) -> str:
    """Helper to get and format messages from the dictionary."""
    message_template = MESSAGES.get(key, f"{RED}❌ Unknown message key: '{key}'{RESET}") # Default if key not found

    # Add color codes to kwargs for easy use in templates if needed
    kwargs.update({
        'reset': RESET, 'bold': BOLD, 'red': RED, 'green': GREEN,
        'yellow': YELLOW, 'blue': BLUE, 'magenta': MAGENTA, 'cyan': CYAN
    })

    try:
        # Use format_map which ignores extra keys in kwargs
        return message_template.format_map(kwargs)
    except KeyError as e:
        # This should be less common with format_map, but handle just in case
        return MESSAGES["message_formatting_error"].format(key=key, error_key=e)
    except Exception as e:
        # Catch other potential formatting errors
        return MESSAGES["generic_formatting_error"].format(key=key, error=e)

def display_success(message_key: str, **kwargs):
    """Displays a success message."""
    print(f"✔️ {GREEN}{_get_message(message_key, **kwargs)}{RESET}")

def display_warning(message_key: str, **kwargs):
    """Displays a warning message."""
    print(f"🟡 {YELLOW}{_get_message(message_key, **kwargs)}{RESET}")

def display_error(message_key: str, **kwargs):
    """Displays an error message."""
    # Try to find a specific message, fallback to generic if key unknown or kwargs missing
    if message_key not in MESSAGES:
        # If the key itself is the error message (e.g., from unexpected exception)
        print(f"❌ {RED}{_get_message('generic_error', error_message=message_key)}{RESET}")
    else:
        try:
             # Attempt to format the specific message
             # Ensure the color codes are part of the message template itself
             print(f"❌ {RED}{_get_message(message_key, **kwargs)}{RESET}") # Apply base error color
        except KeyError as e:
             # If formatting fails due to missing kwargs for a known key
             print(MESSAGES["message_formatting_error"].format(key=message_key, error_key=e))
        except Exception as format_e:
             print(MESSAGES["generic_formatting_error"].format(key=message_key, error=format_e))


def display_info(message_key: str, **kwargs):
    """Displays an informational message or title."""
    # No specific color added here, rely on colors within the message template
    print(f"ℹ️ {_get_message(message_key, **kwargs)}")

def display_contacts(contacts: list, show_indices: bool = True):
    """Displays a list of contacts with optional 1-based indexing."""
    if not contacts:
        display_info("no_contacts_found")
        return

    # Use a generic title if just showing search results without list context
    # display_info("contacts_list_title") # Keep this if always displaying the full list context
    print(SEPARATOR_LINE)
    for index, contact in enumerate(contacts, start=1):
        idx_str = f"{BOLD}{index}{RESET}. " if show_indices else ""
        print(f"{idx_str}{CYAN}{contact.name}{RESET}")

        # Display Phones with indices
        if contact.phones:
            phones_str = ", ".join(
                _get_message("phone_with_index", index=i + 1, phone=p)
                for i, p in enumerate(contact.phones)
            )
            print(_get_message("contact_phones", phones=phones_str))
        else:
            print(_get_message("contact_no_phones"))

        # Display Emails with indices (optional, using simple join for now)
        if contact.emails:
            # emails_str = ", ".join(
            #     _get_message("email_with_index", index=i + 1, email=e)
            #     for i, e in enumerate(contact.emails)
            # ) # This might be too verbose, simple join is often fine
            emails_str = ", ".join(contact.emails)
            print(_get_message("contact_emails", emails=emails_str))
        else:
            print(_get_message("contact_no_emails"))

        # Display Birthday
        if contact.birthday:
            try:
                # Ensure birthday is a date object before formatting
                if isinstance(contact.birthday, date):
                    birthday_str = contact.birthday.strftime('%d.%m.%Y')
                    print(_get_message("contact_birthday", birthday=birthday_str))
                else:
                     # Display raw data if not a date object (indicates data corruption)
                     print(f" Birthday: Invalid data ({contact.birthday})")
            except Exception: # Catch potential strftime errors with invalid date objects
                print(f" Birthday: Error formatting date ({contact.birthday})")
        else:
            print(_get_message("contact_no_birthday"))
        print(TITLE_SEPARATOR) # Separator between contacts

    # print(SEPARATOR_LINE) # Removed bottom line, separator is between items now

def display_notes(notes: list, show_indices: bool = True):
    """Displays a list of notes with optional 1-based indexing."""
    if not notes:
        display_info("no_notes_found")
        return

    # display_info("notes_list_title") # Keep if needed
    print(SEPARATOR_LINE)
    for index, note in enumerate(notes, start=1):
        idx_str = f"{BOLD}{index}{RESET}. " if show_indices else ""
        # Correctly pass kwargs for formatting
        print(_get_message("note_item_detailed", bold_index=idx_str.strip(), green_title=f"{GREEN}{note.title}{RESET}", reset=RESET))

        if note.tags:
            tags_str = " ".join([f"#{tag}" for tag in note.tags])
            # Pass tags_str as a kwarg, ensure color is applied
            print(_get_message("note_tags_detailed", yellow_tags=f"{YELLOW}{tags_str}{RESET}", reset=RESET))
        if note.content:
            content_preview = note.content[:100].replace('\n', '\n' + ' ' * 5) + ('...' if len(note.content) > 100 else '')
            # Pass content_preview as a kwarg
            print(_get_message("note_content_detailed", content_preview=content_preview))

        print(TITLE_SEPARATOR) # Separator between notes

    # print(SEPARATOR_LINE) # Removed bottom line

def display_birthdays(birthday_results: list[tuple]): # Type hint fixed
    """Displays upcoming birthdays with celebration dates."""
    if not birthday_results:
        display_info("no_upcoming_birthdays")
        return

    display_info("birthdays_found_title")
    print(SEPARATOR_LINE)

    for contact, celebration_date in birthday_results:
        # Basic check if contact and birthday exist
        if not contact or not contact.birthday or not isinstance(contact.birthday, date):
            print(f"- {RED}Error displaying birthday data for an entry.{RESET}")
            continue

        try:
            # Correct birthday formatting for display
            original_bday_obj_this_year = contact.birthday.replace(year=date.today().year)
            original_bday_str = original_bday_obj_this_year.strftime('%d.%m') # Day and month only
            weekday_name = original_bday_obj_this_year.strftime('%A') # Weekday of the actual birthday this year

            if celebration_date and isinstance(celebration_date, date):
                celebration_day_str = celebration_date.strftime('%d.%m')
                celebration_weekday = celebration_date.strftime('%A') # Weekday of the celebration

                message = _get_message(
                    "birthday_celebration_adjusted",
                    name=contact.name,
                    bday=original_bday_str,
                    bday_weekday=weekday_name,
                    celeb_weekday=celebration_weekday,
                    celeb_day=celebration_day_str
                )
            else:
                # No celebration date adjustment needed or provided
                message = _get_message(
                    "birthday_celebration_on_day",
                    name=contact.name,
                    bday=original_bday_str,
                    bday_weekday=weekday_name
                )
            print(f"- {message}")
        except Exception as e:
            print(f"- {RED}Error formatting birthday for {contact.name}: {e}{RESET}")

    print(SEPARATOR_LINE)

# *** FIXED: display_help now accepts and uses command_map ***
def display_help(command_map: dict | None = None): # command structure as an argument
    """Displays available commands and their descriptions for the current context."""
    display_info("help_title") # Use the specific title key

    if not command_map: # Check if the map is None or empty
        print(f"  {YELLOW}No specific commands available in this context. Use 'menu' to go back or 'exit' to quit.{RESET}")
        return

    print(f"  {YELLOW}Usage: command [arguments...]{RESET}")
    print(SEPARATOR_LINE)

    for command, details in command_map.items():
        # Handle both string descriptions and dicts with description/example
        if isinstance(details, dict):
            description = details.get('description', 'No description available.')
            example = details.get('example', '')
        elif isinstance(details, str):
            description = details
            example = ''
        else:
            description = 'Invalid help format for this command.'
            example = ''

        print(f"  {BOLD}{command}{RESET}:")
        print(f"    {description}")
        if example:
             print(f"    {CYAN}Example: {example}{RESET}")
        # print(TITLE_SEPARATOR) # Maybe too much separation

    print(SEPARATOR_LINE)


# ================ Input Functions ================

def get_input(prompt_key: str, path_info: str = "", **prompt_kwargs) -> str:
    """Gets user input with a formatted prompt including the menu path."""
    # Get the specific prompt text (the question) using the key
    prompt_text = _get_message(prompt_key, **prompt_kwargs)

    # Construct the full path display
    path_display = path_info if path_info else "/" # Show '/' for root
    separator = MESSAGES["input_path_separator"] if path_info else "" # No separator if root

    # Combine path and prompt using the default template
    full_prompt = MESSAGES["input_prompt_default"].format(
        path=path_display,
        separator=separator,
        prompt=prompt_text
    )

    try:
        user_input = input(full_prompt)
        return user_input.strip()
    except EOFError:
        # Handle Ctrl+D or similar EOF signals gracefully
        print() # Print newline after EOF
        return "exit" # Treat EOF as exit command

def get_confirmation(prompt_key: str = "confirm_prompt", path_info: str = "", **prompt_kwargs) -> bool | None:
    """
    Gets a 'yes' or 'no' confirmation from the user.
    Returns True for 'yes', False for 'no', None for cancellation/invalid input after retries.
    """
    yes_answer = MESSAGES["yes"].lower()
    no_answer = MESSAGES["no"].lower()
    retries = 2 # Limit retries for invalid input

    while retries > 0:
        # Use the provided prompt_key or the default "confirm_prompt"
        answer = get_input(prompt_key, path_info, **prompt_kwargs).lower()
        if answer == yes_answer:
            return True
        elif answer == no_answer:
            return False
        else:
            display_error("invalid_yes_no")
            retries -= 1

    display_warning("input_cancelled") # Assume cancellation after retries
    return None # Indicate cancellation or failure


if __name__ == "__main__":
    import main
    main.main()