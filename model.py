# Model file by MVC pattern
# This file contains the model of the app
# It contains the data and the logic of the app

import pickle
from datetime import date,timedelta
import re
import view as v

FILE_PATH = "data.pkl"  # Path to the data file
NAME_REGEX = re.compile(r"^[a-zA-Zа-яА-ЯіІїЇєЄґҐʼ'-]+( [a-zA-Zа-яА-ЯіІїЇєЄґҐʼ'-]+)*$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
PHONE_REGEX = re.compile(r"\d{10}")

# ================ Custom Exceptions ================
class ContactError(Exception):
    """Base exception for contact related errors."""
    pass

class PhoneError(ValueError):
    """Exception for phone validation errors."""
    pass

class EmailError(ValueError):
    """Exception for email validation errors."""
    pass

class BirthdayError(ValueError):
    """Exception for birthday validation errors."""
    pass

class TitleError(ValueError):
    """Exception for note title validation errors."""
    pass

class TagError(ValueError):
    """Exception for tag validation errors."""
    pass

class NotFoundError(Exception):
    """Exception when an item is not found."""
    pass

class NoteError(Exception):
    """Base exception class for Note and Notebook errors."""
    def __init__(self, key, **kwargs):
        self.key = key
        self.kwargs = kwargs
        super().__init__(key, **kwargs)  # For internal logging/debugging

# ================ Contact Class ================
class Contact:
    id_counter = 0 # Consider loading/saving this counter as well

    def __init__(self, name: str):
        if not NAME_REGEX.match(name):
            raise ContactError("invalid_name_format")
        self.__id     : int = Contact.id_counter
        self.name     : str = name
        self.phones   : list[str] = []
        self.emails   : list[str] = []
        self.birthday : date = None
        Contact.id_counter += 1

    @property
    def id(self) -> int:
        return self.__id

    def __str__(self) -> str:
        # Basic string representation, View will handle detailed formatting
        return f"Contact(ID: {self.__id}, Name: {self.name})"

    def __repr__(self) -> str:
        # Representation useful for developers/debugging
        return f"Contact(id={self.__id}, name='{self.name}', phones={self.phones}, emails={self.emails}, birthday={self.birthday})"

# ================ AdressBook Class ================
class AdressBook:
    def __init__(self):
        self.contacts : list[Contact] = []

    # ================ Contact CRUD methods ================
    # Add contact to address book
    def add_contact(self, contact: Contact):
        if any(c.name.lower() == contact.name.lower() for c in self.contacts):
            raise ContactError("duplicate_contact")
        self.contacts.append(contact)

    # Remove contact by the contact object itself (found previously)
    def remove_contact(self, contact: Contact):
        if contact not in self.contacts:
            raise NotFoundError("contact_not_found_in_list")
        self.contacts.remove(contact)

    # ================ Find methods ================
    # Find contact by partial data: name, phone or email
    def _contact_search_fields(self, contact: Contact) -> list[str]:
        return [
            contact.name.lower(),
            *[phone.lower() for phone in contact.phones],
            *[email.lower() for email in contact.emails]
    ]

    def _search_contacts(self, part: str, field_getter: callable) -> list[Contact]:
        part = part.lower() # Search case-insensitively
        return [
            contact for contact in self.contacts
            if any(part in field for field in field_getter(contact))
        ]

    def find_contacts(self, part: str) -> list[Contact]:
        part = part.lower() # Search case-insensitively
        return self._search_contacts(part, self._contact_search_fields)

    def find_contact_by_name(self, name_part: str) -> list[Contact]:
        name_part = name_part.lower() # Search case-insensitively
        return self._search_contacts(name_part, lambda c: [c.name.lower()])

    def find_contact_by_phone(self, phone_part: str) -> list[Contact]:
        return self._search_contacts(phone_part, lambda c: [p for p in c.phones])

    def find_contact_by_email(self, email_part: str) -> list[Contact]:
        email_part = email_part.lower() # Search case-insensitively
        return self._search_contacts(email_part, lambda c: [e.lower() for e in c.emails])

    # Get contacts with birthdays in the next N days

    def get_birthdays_in_next_days(self, days: int) -> list[tuple[Contact, date | None]]:
        """
        Finds contacts whose birthdays fall within the next 'days' days.
        Calculates the celebration date (next Monday if birthday is on Sat/Sun).
        Returns a list of tuples: (Contact, celebration_date | None).
        None for celebration_date means celebrate on the actual birthday.
        """
        today = date.today()
        result: list[tuple[Contact, date | None]] = []

        for contact in self.contacts:
            if contact.birthday is None:
                continue

            try:
                birthday_this_year = contact.birthday.replace(year=today.year)

                if birthday_this_year < today:
                   birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                days_until_birthday = (birthday_this_year - today).days

                # Check if birthday is within the range (0 to days inclusive)
                # We include 0 for birthdays today
                if 0 <= days_until_birthday <= days:
                   celebration_date = None

                   # Check weekday (Monday is 0, Sunday is 6)
                   weekday = birthday_this_year.weekday()
                   if weekday == 5:  # Saturday
                        celebration_date = birthday_this_year + timedelta(days=2)
                   elif weekday == 6:  # Sunday
                        celebration_date = birthday_this_year + timedelta(days=1)

                   result.append((contact, celebration_date))
            except ValueError:
                # Handle potential errors like invalid dates (e.g., Feb 29 in a non-leap year)
                # Or log the error for the specific contact
                continue # Skip this contact
        return result


    # ================ Phone methods ================
    # Add contact phone number
    def _validate_phone(self, contact: Contact, phone_number: str) -> None | PhoneError:
        if not PHONE_REGEX.fullmatch(phone_number):
            raise PhoneError("invalid_phone_format")
        if phone_number in contact.phones:
            raise PhoneError("duplicate_phone")

    def add_phone(self, contact: Contact, phone_number: str):
        self._validate_phone(contact, phone_number)
        contact.phones.append(phone_number)

    # Change contact phone number by index (1-based for user input, converted to 0-based internally)
    def change_phone(self, contact: Contact, phone_index: int, new_phone_number: str):
        internal_index = phone_index - 1 # Convert to 0-based index
        if not 0 <= internal_index < len(contact.phones):
            raise IndexError("invalid_phone_index")
        # Validate the new number *before* changing
        self._validate_phone(contact, new_phone_number)
        contact.phones[internal_index] = new_phone_number

    # Remove contact phone number by index (1-based for user input, converted to 0-based internally)
    def remove_phone(self, contact: Contact, phone_index: int):
        internal_index = phone_index - 1 # Convert to 0-based index
        if not 0 <= internal_index < len(contact.phones):
            raise IndexError("invalid_phone_index")
        contact.phones.pop(internal_index)


    # ================ Email methods ================
    # Add contact email
    def _validate_email(self, contact: Contact, email: str) -> None | EmailError:
        # Made this an instance method by adding self
        email_lower = email.lower() # Store and compare emails case-insensitively
        if not EMAIL_REGEX.fullmatch(email_lower):
            raise EmailError("invalid_email_format")
        # Check against lowercased existing emails
        if email_lower in [e.lower() for e in contact.emails]:
            raise EmailError("duplicate_email")

    def add_email(self, contact: Contact, email: str):
        self._validate_email(contact, email)
        contact.emails.append(email) # Store original case, but validation is case-insensitive

    # Change contact email by index (1-based for user input, converted to 0-based internally)
    def change_email(self, contact: Contact, email_index: int, new_email: str):
        internal_index = email_index - 1 # Convert to 0-based index
        if not 0 <= internal_index < len(contact.emails):
            raise IndexError("invalid_email_index")
        # Validate the new email *before* changing
        self._validate_email(contact, new_email)
        contact.emails[internal_index] = new_email

    # Remove contact email by index (1-based for user input, converted to 0-based internally)
    def remove_email(self, contact: Contact, email_index: int):
       internal_index = email_index - 1 # Convert to 0-based index
       if not 0 <= internal_index < len(contact.emails):
           raise IndexError("invalid_email_index")
       contact.emails.pop(internal_index)


    # ================ Birthday methods ================
    # Change contact birthday (pass None to remove)
    def change_birthday(self, contact: Contact, new_birthday: date | None):
        # Input validation (format DD.MM.YYYY) happens in Controller before conversion.
        # Model validates the date object itself.
        if new_birthday is not None:
            # Ensure it's a valid date object before range check
            if not isinstance(new_birthday, date):
                 # This case should ideally not happen if controller parses correctly
                 raise BirthdayError("invalid_birthday_object") # Add message key
            if new_birthday.year < 1900 or new_birthday > date.today():
                raise BirthdayError("invalid_birthday_range")
        contact.birthday = new_birthday


# ================ Note Class ================
class Note:
    #Constants
    MIN_TITLE_LEN = 2
    MAX_TITLE_LEN = 128
    MIN_TAG_LEN = 2
    MAX_TAG_LEN = 16
    TAG_PATTERN = re.compile(r"^[a-zA-Z0-9_]+$") #validation for letters and numbers only.

    #Id_counter - IMPORTANT:
    # Its value should be set by the load_data_from_file function
    # after loading the data (e.g. max(note.id for note in notes) + 1).
    # The class itself does not manage the persistence of the counter.
    id_counter = 0 # Consider loading/saving this counter as well

    def __init__(self, title: str):
        # --- Implementing title validation ---
        if not (Note.MIN_TITLE_LEN <= len(title) <= Note.MAX_TITLE_LEN):
            # Error key with parameters
            raise TitleError("invalid_title_length", min=Note.MIN_TITLE_LEN, max=Note.MAX_TITLE_LEN)
        self.__id    : int = Note.id_counter
        self.title   : str = title
        self.content : str = ""
        self.tags    : list[str] = [] # Tags are stored in lowercase
        Note.id_counter += 1

    @property
    def id(self) -> int:
        return self.__id

    def __repr__(self) -> str:
     # Representation useful for developers/debugging
     content_preview = self.content[:20].replace('\n', '\\n') + ('...' if len(self.content) > 20 else '')
     return f"Note(id={self.__id}, title='{self.title}', content='{content_preview}...', tags={self.tags})"

    # --- The __eq__ and __hash__ methods are required for list.remove() to work correctly ---
    def __eq__(self, other):
        if not isinstance(other, Note):
            return NotImplemented
        return self.__id == other.__id

    def __hash__(self):
        return hash(self.__id)

# ================ Notebook Class ================

class Notebook:
    def __init__(self, autosave_callback=None):
        self.notes : list[Note] = []
        self.autosave_callback = autosave_callback # Save callback
        if autosave_callback:
             self._autosave = autosave_callback # Directly assign if provided
        else:
             self._autosave = lambda: None # No-op if no callback

    # --- Private method to call autosave ---
    def _autosave(self):
        """Calls the autosave callback if it's set."""
        if self.autosave_callback and callable(self.autosave_callback):
           self.autosave_callback()

    # ================ Note CRUD methods ================
    # Add note to notebook
    def add_note(self, note: Note):
        # --- Implementing duplicate title checking (case-insensitive) ---
        title_lower = note.title.lower()
        for existing_note in self.notes:
            if existing_note.title.lower() == title_lower:
                raise NoteError("duplicate_title", title=note.title) # Error key
        self.notes.append(note)
        self._autosave() # Call autosave

    def change_note_title(self, note: Note, new_title: str):
        # --- Implementing new name validation ---
        if not (Note.MIN_TITLE_LEN <= len(new_title) <= Note.MAX_TITLE_LEN):
            raise TitleError("invalid_title_length", min=Note.MIN_TITLE_LEN, max=Note.MAX_TITLE_LEN)

        # Check for duplicates (ignoring the current note, case-insensitive)
        new_title_lower = new_title.lower()
        for existing_note in self.notes:
            if existing_note.id != note.id and existing_note.title.lower() == new_title_lower:
                 raise NoteError("duplicate_title", title=new_title) # Error key
        note.title = new_title
        self._autosave() # Call autosave

    def change_note_content(self, note: Note, new_content: str):
        # No specific validation for content, allow anything including empty
        note.content = new_content
        self._autosave() # Call autosave

    def remove_note(self, note: Note):
        # --- Implementing deletion error handling ---
        try:
            self.notes.remove(note) # Uses Note.__eq__
            self._autosave() # Call autosave AFTER successful deletion
        except ValueError:
             # Generate an error with the key if the note is not in the list
            raise NotFoundError("note_not_found", title=note.title) # Error key

# ================ Tag methods ================
    def add_tag_to_note(self, note: Note, tag: str):
        # --- Implementing tag validation ---
        tag_clean = tag.strip()  # Remove any leading/trailing spaces
        if not (Note.MIN_TAG_LEN <= len(tag_clean) <= Note.MAX_TAG_LEN):
            raise TagError("invalid_tag_length", min=Note.MIN_TAG_LEN, max=Note.MAX_TAG_LEN)
        if not Note.TAG_PATTERN.match(tag_clean):
            raise TagError("invalid_tag_format")  # Error key

        tag_lower = tag_clean.lower()  # Convert the tag to lowercase

        # --- Check for duplicate tags ---
        if tag_lower in note.tags:
            # If the tag already exists, raise an error or warn (currently warns via view)
            # For consistency, let's raise an error from the model
            raise TagError("duplicate_tag_in_note", tag=tag_lower, title=note.title) # Add message key

        # If the tag is not already in the note, add it
        note.tags.append(tag_lower)
        note.tags.sort()  # Sort tags alphabetically for consistency
        self._autosave() # Call autosave

    def remove_tag_from_note(self, note: Note, tag: str):
        # --- Implementing tag removal error handling ---
        tag_lower = tag.lower() # Ensure comparison is case-insensitive
        try:
             # Check if the tag exists before deleting
             if tag_lower not in note.tags:
                 raise ValueError # Raise an error if the tag is missing
             note.tags.remove(tag_lower)
             self._autosave() # Call autosave AFTER successful deletion
        except ValueError:
            # Generate an error with the key if the tag is not in the note
            raise NotFoundError("tag_not_found_in_note", tag=tag_lower, title=note.title) # Error key

    # ================ Note search methods ================
    def find_notes(self, part: str) -> list[Note]:
        part_lower = part.lower() # Search case-insensitively
        return [ note for note in self.notes if part_lower in note.title.lower() or part_lower in note.content.lower() ]

    def find_note_by_title(self, part: str) -> list[Note]:
        part_lower = part.lower() # Search case-insensitively
        return [ note for note in self.notes if part_lower in note.title.lower() ]

    def find_note_by_content(self, part: str) -> list[Note]:
        part_lower = part.lower() # Search case-insensitively
        return [ note for note in self.notes if part_lower in note.content.lower() ]

    def find_note_by_tag(self, part: str) -> list[Note]:
        """Finds notes where any tag contains the search part (case-insensitive)."""
        part_lower = part.lower() # Search case-insensitively
        # *** FIXED: Search for part within each tag ***
        return [ note for note in self.notes if any(part_lower in tag for tag in note.tags) ]


# ================ Data Persistence ================
# Load data from file and return AdressBook and Notebook objects
def load_data_from_file(file_path: str = FILE_PATH) -> tuple[AdressBook, Notebook]:
    """
    Loads the address book, notebook, and ID counters from the file.
    Returns new empty books if the file is not found or corrupted.
    Also sets up the autosave callback for the loaded notebook.
    """
    address_book = AdressBook()
    notebook = Notebook() # Create default empty notebook first

    try:
        with open(file_path, "rb") as f:
            data = pickle.load(f)
            if isinstance(data, tuple) and len(data) == 4:
                loaded_ab, loaded_nb, contact_counter, note_counter = data
                if isinstance(loaded_ab, AdressBook) and isinstance(loaded_nb, Notebook) \
                   and isinstance(contact_counter, int) and isinstance(note_counter, int):
                    # Restore data and ID counters
                    address_book = loaded_ab
                    notebook = loaded_nb # Use loaded notebook
                    Contact.id_counter = contact_counter
                    Note.id_counter = note_counter
                else:
                    # Data has incorrect types, use defaults but log potentially?
                    pass # Using default empty books
            else:
                 # Data is not the expected tuple, use defaults
                 pass # Using default empty books

    except FileNotFoundError:
        # Start fresh, use default empty books
        pass
    except (pickle.UnpicklingError, EOFError, AttributeError, ImportError, IndexError, TypeError, IOError, Exception) as e:
        # Handle various load errors, use defaults
        # Consider logging the error 'e' here
        print(f"[Warning] Error loading data file: {e}. Starting with empty data.") # Simple console warning

    # Save AdressBook and Notebook objects to file
    def actual_save():
        # This function needs access to both address_book and notebook
        # It's slightly awkward here in the model file.
        # Ideally, the controller sets this callback after loading.
        # For now, let's assume save_data_to_file is accessible and works.
        try:
            save_data_to_file(address_book, notebook, file_path)
            # print("Autosave successful.") # Optional debug message
        except Exception as save_error:
            # How to handle autosave errors? Log them? Inform user?
            print(f"[Error] Autosave failed: {save_error}") # Simple console error

    notebook.autosave_callback = actual_save # Set the callback

    return address_book, notebook

# Save AdressBook and Notebook objects to file
def save_data_to_file(address_book: AdressBook, notebook: Notebook, file_path: str = FILE_PATH):
    """
    Saves the address book, notebook, and current ID counters to the file.
    Propagates exceptions upwards if saving fails.
    """
    # No try...except here, let controller handle save errors if needed
    with open(file_path, "wb") as f:
        data_to_save: tuple = (address_book, notebook, Contact.id_counter, Note.id_counter)
        pickle.dump(data_to_save, f)


if __name__ == "__main__":
    import main
    main.main()