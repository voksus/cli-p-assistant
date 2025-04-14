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
     return [
        contact for contact in self.contacts
        if any(part in field for field in field_getter(contact))
    ]

    def find_contacts(self, part: str) -> list[Contact]:
     return self._search_contacts(part, self._contact_search_fields)

    def find_contact_by_name(self, name_part: str) -> list[Contact]:
     return self._search_contacts(name_part, lambda c: [c.name.lower()])

    def find_contact_by_phone(self, phone_part: str) -> list[Contact]:
     return self._search_contacts(phone_part, lambda c: [p for p in c.phones])

    def find_contact_by_email(self, email_part: str) -> list[Contact]:
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
        
        birthday_this_year = contact.birthday.replace(year=today.year)
        
        if birthday_this_year < today:
           birthday_this_year = birthday_this_year.replace(year=today.year + 1)
        
        days_until_birthday = (birthday_this_year - today).days
        
        if 0 < days_until_birthday <= days:
           celebration_date = None  

           if birthday_this_year.weekday() == 5:  # Saturday
                celebration_date = birthday_this_year + timedelta(days=2)  
           elif birthday_this_year.weekday() == 6:  # Sunday
                celebration_date = birthday_this_year + timedelta(days=1) 

           result.append((contact, celebration_date))
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

    # Change contact phone number by index (0-based)
    def change_phone(self, contact: Contact, phone_index: int, new_phone_number: str):
        self._validate_phone(contact, new_phone_number)
        if not 0 <= phone_index - 1 < len(contact.phones):
            raise IndexError("invalid_phone_index")
        contact.phones[phone_index - 1] = new_phone_number

    # Remove contact phone number by index (0-based)
    def remove_phone(self, contact: Contact, phone_index: int):
        if not 0 <= phone_index - 1 < len(contact.phones):
            raise IndexError("invalid_phone_index")
        contact.phones.pop(phone_index - 1)


    # ================ Email methods ================
    # Add contact email
    def _validate_email(contact: Contact, email: str) -> None | EmailError:
     if not EMAIL_REGEX.fullmatch(email):
        raise EmailError("invalid_email_format")
     if email in contact.emails:
        raise EmailError("duplicate_email")
    
    def add_email(self, contact: Contact, email: str):
        self._validate_email(contact, email)
        contact.emails.append(email)

    # Change contact email by index (0-based)
    def change_email(self, contact: Contact, email_index: int, new_email: str):
        self._validate_email(contact, new_email)
        if not 0 <= email_index - 1 < len(contact.emails):
            raise IndexError("invalid_email_index")
        contact.emails[email_index - 1] = new_email

    # Remove contact email by index (0-based)
    def remove_email(self, contact: Contact, email_index: int):
       if not 0 <= email_index - 1 < len(contact.emails):
           raise IndexError("invalid_email_index")
       contact.emails.pop(email_index - 1)


    # ================ Birthday methods ================
    # Change contact birthday (pass None to remove)
    def change_birthday(self, contact: Contact, new_birthday: date | None):
        # Input validation (format DD.MM.YYYY, valid date, range) should happen in the Controller before converting.
        if new_birthday is not None:
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
    TAG_PATTERN = re.compile(r"^[a-zA-Z0-9]+$") #validation for letters and numbers only.
    
    #Id_counter - IMPORTANT:
    # Its value should be set by the load_data_from_file function
    # after loading the data (e.g. max(note.id for note in notes) + 1).
    # The class itself does not manage the persistence of the counter.
    id_counter = 0 # Consider loading/saving this counter as well

    def __init__(self, title: str):
        # --- Implementing name validation ---              
        if not (Note.MIN_TITLE_LEN <= len(title) <= Note.MAX_TITLE_LEN):
            # Error key with parameters
            raise TitleError("invalid_title_length", min=Note.MIN_TITLE_LEN, max=Note.MAX_TITLE_LEN)
        self.__id    : int = Note.id_counter
        self.title   : str = title
        self.content : str = ""
        self.tags    : list[str] = []
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
        self.autosave_callback = autosave_callback # Save callback'у
        
    # --- Private method to call autosave ---
    def _autosave(self):
        """Calls the autosave callback if it's set."""
        if self.autosave_callback and callable(self.autosave_callback):
           self.autosave_callback()

    # ================ Note CRUD methods ================
    # Add note to notebook
    def add_note(self, note: Note):
        # --- Implementing duplicate name checking ---
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

        # Check for duplicates (ignoring the current note)
        new_title_lower = new_title.lower()
        for existing_note in self.notes:
            if existing_note.id != note.id and existing_note.title.lower() == new_title_lower:
                 raise NoteError("duplicate_title", title=new_title) # Error key
        note.title = new_title
        self._autosave() # Call autosave

    def change_note_content(self, note: Note, new_content: str):
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
        # If the tag length is not within the defined limits, raise an error with parameters
            raise TagError("invalid_tag_length", min=Note.MIN_TAG_LEN, max=Note.MAX_TAG_LEN)
        if not Note.TAG_PATTERN.match(tag_clean):
        # If the tag format doesn't match the defined pattern, raise an error
            raise TagError("invalid_tag_format")  # Error key

        tag_lower = tag_clean.lower()  # Convert the tag to lowercase for case-insensitive comparison

    # --- Check for duplicate tags ---
    # Find any existing tags in the note that match the given tag
        tags_repeat = [existing_tag for existing_tag in note.tags if existing_tag == tag_lower]

        if tags_repeat:
        # If the tag already exists, don't raise an error; instead, issue a warning
            v.display_warning("tags_already_exist", tags_repeat=tags_repeat)

    # If the tag is not already in the note, add it
        if tag_lower not in note.tags:
            note.tags.append(tag_lower)
            note.tags.sort()  # Sort tags alphabetically for consistency

    def remove_tag_from_note(self, note: Note, tag: str):
    # --- Implementing tag removal error handling ---
        tag = tag.lower()
        try:
             # Check if the tag exists before deleting
             if tag not in note.tags:
                 raise ValueError # Raise an error if the tag is missing
             note.tags.remove(tag)
             self._autosave() # Call autosave AFTER successful deletion
        except ValueError:
            # Generate an error with the key if the tag is not in the note
            raise NotFoundError("tag_not_found_in_note", tag, title=note.title) # Error key

    # ================ Note search methods ================
    def find_notes(self, part: str) -> list[Note]:
        part = part.lower()
        return [ note for note in self.notes if part in note.title.lower() or part in note.content.lower() ]

    def find_note_by_title(self, part: str) -> list[Note]:
        part = part.lower()
        return [ note for note in self.notes if part in note.title.lower() ]

    def find_note_by_content(self, part: str) -> list[Note]:
        part = part.lower()
        return [ note for note in self.notes if part in note.content.lower() ]

    def find_note_by_tag(self, part: str) -> list[Note]:
        part = part.lower()
        return [ note for note in self.notes if part in note.tags ]


# ================ Data Persistence ================
# Load data from file and return AdressBook and Notebook objects
def load_data_from_file(file_path: str = FILE_PATH) -> tuple[AdressBook, Notebook]:
    """
    Loads the address book, notebook, and ID counters from the file.
    Returns new empty books if the file is not found or corrupted.
    """
    try:
        with open(file_path, "rb") as f:
            # Attempt to load the data structure
            data = pickle.load(f)
            # Check if the loaded data is the expected tuple format
            if isinstance(data, tuple) and len(data) == 4:
                address_book, notebook, contact_counter, note_counter = data
                # Basic type check for loaded objects
                if isinstance(address_book, AdressBook) and isinstance(notebook, Notebook) \
                   and isinstance(contact_counter, int) and isinstance(note_counter, int):
                    # Restore ID counters
                    Contact.id_counter = contact_counter
                    Note.id_counter = note_counter
                    return address_book, notebook
                else:
                    # Data has incorrect types within the tuple, treat as corrupted
                    # New data will be created
                    return AdressBook(), Notebook()
            else:
                # Data is not the expected 4-element tuple, treat as corrupted
                # New data will be created
                return AdressBook(), Notebook()

    except FileNotFoundError:
        # It's okay if the file doesn't exist, start fresh
        return AdressBook(), Notebook()
    except (pickle.UnpicklingError, EOFError, AttributeError, ImportError, IndexError, TypeError, IOError, Exception) as e:
        # Handle file corruption, I/O errors, or unexpected issues during loading
        # Log the error 'e' here if logging is implemented
        # Return empty books to allow the application to continue
        return AdressBook(), Notebook()

# Save AdressBook and Notebook objects to file
def save_data_to_file(address_book: AdressBook, notebook: Notebook, file_path: str = FILE_PATH):
    """
    Saves the address book, notebook, and current ID counters to the file.
    Standard exceptions (IOError, pickle.PicklingError, etc.) will propagate
    upwards if saving fails, to be handled by the caller (Controller).
    """
    # No try...except block here in the model for saving errors.
    # Let exceptions propagate to the controller which handles the auto-save call.
    with open(file_path, "wb") as f:
        # Prepare data tuple including current ID counters
        data_to_save: tuple = (address_book, notebook, Contact.id_counter, Note.id_counter)
        pickle.dump(data_to_save, f)


if __name__ == "__main__":
    import main
    main()