# Model file by MVC pattern
# This file contains the model of the app
# It contains the data and the logic of the app

import pickle
from datetime import date,timedelta
import re

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
    id_counter = 0 # Consider loading/saving this counter as well

    def __init__(self, title: str):
        # TODO: Add validation for title length/format here or ensure it's done before creating Note
        self.__id    : int = Note.id_counter
        self.title   : str = title
        self.content : str = ""
        self.tags    : list[str] = []
        Note.id_counter += 1

    @property
    def id(self) -> int:
        return self.__id

    def __str__(self) -> str:
        # Basic string representation
        return f"Note(ID: {self.__id}, Title: {self.title})"

    def __repr__(self) -> str:
        # Representation useful for developers/debugging
        return f"Note(id={self.__id}, title='{self.title}', content='{self.content[:20]}...', tags={self.tags})"


# ================ Notebook Class ================
class Notebook:
    def __init__(self):
        self.notes : list[Note] = []

    # ================ Note CRUD methods ================
    # Add note to notebook
    def add_note(self, note: Note):
        # TODO: Check for duplicate notes? (e.g., by title) - Define policy
        self.notes.append(note)

    # Change note title
    def change_note_title(self, note: Note, new_title: str):
        # Validation (length 4-128) should happen in Controller/before call.
        # TODO: Add validation here as a safeguard?
        # ...
        note.title = new_title

    # Change note content
    def change_note_content(self, note: Note, new_content: str):
        # No validation specified for content, just assign
        note.content = new_content

    # Remove note from notebook by the note object itself
    def remove_note(self, note: Note):
        # TODO: Handle case where note is not in list?
        try:
            self.notes.remove(note)
        except ValueError:
            raise NotFoundError("note_not_found_in_list")

    # ================ Tag methods ================
    def add_tag_to_note(self, note: Note, tag: str):
        """Adds a validated and lowercased tag to the note if not present."""
        # Validation (format, length 2-16) and lowercasing should happen in Controller/before call.
        # Assume tag is pre-validated and just needs lowercasing
        # TODO: Add validation here as a safeguard?
        # ...
        #     raise TagError("duplicate_tag")

    def remove_tag_from_note(self, note: Note, tag: str):
        """Removes a tag from the note (case-insensitive)."""
        # TODO: Handle case where tag is not found
        tag_lower = tag.lower()
        try:
            note.tags.remove(tag_lower)
        except ValueError:
             raise NotFoundError("tag_not_found_in_note")

    # ================ Note search methods ================
    # Find note by partial data: title or content
    def find_notes(self, part: str) -> list[Note]:
        result : list[Note] = []
        part = part.lower()
        for note in self.notes:
            if part in note.title.lower() or part in note.content.lower():
                result.append(note)
        return result

    # Find note by title (partial or full)
    def find_note_by_title(self, title_part: str) -> list[Note]:
        result : list[Note] = []
        title_part = title_part.lower()
        for note in self.notes:
            if title_part in note.title.lower():
                result.append(note)
        return result

    # Find note by content (partial or full)
    def find_note_by_content(self, content_part: str) -> list[Note]:
        result : list[Note] = []
        content_part = content_part.lower()
        for note in self.notes:
            if content_part in note.content.lower():
                result.append(note)
        return result

    # Find note by tag (exact match, case-insensitive)
    def find_note_by_tag(self, tag: str) -> list[Note]:
        result : list[Note] = []
        tag = tag.lower()
        for note in self.notes:
            if any(tag in t for t in note.tags):
                result.append(note)
        return result


# ================ Data Persistence ================
# Load data from file and return AdressBook and Notebook objects
def load_data_from_file(file_path: str = FILE_PATH) -> tuple[AdressBook, Notebook]:
    try:
        with open(file_path, "rb") as f:
            # TODO: Consider adding versioning or more robust error handling for pickle
            address_book, notebook = pickle.load(f)
            # TODO: Potentially load and restore id_counters for Contact and Note here
            # ...
        return address_book, notebook
    except FileNotFoundError:
        return AdressBook(), Notebook()
    except (pickle.UnpicklingError, EOFError, ImportError, IndexError, AttributeError) as e:
        # Handle corrupted or incompatible pickle file
        # TODO: Log the error e for debugging
        # ...
        return AdressBook(), Notebook()
    except Exception as e:
        # TODO: Log the error e for debugging
        return AdressBook(), Notebook()

# Save AdressBook and Notebook objects to file
def save_data_to_file(address_book: AdressBook, notebook: Notebook, file_path: str = FILE_PATH):
    try:
        with open(file_path, "wb") as f:
            # TODO: Potentially save id_counters here as well
            pickle.dump((address_book, notebook), f)
            print(f"Data saved to {file_path}")
    except (pickle.PicklingError, IOError) as e:
        # Handle errors during saving
        pass
    except Exception as e:
        pass


if __name__ == "__main__":
    import main
    main()