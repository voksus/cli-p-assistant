# Model file by MVC pattern
# This file contains the model of the app
# It contains the data and the logic of the app

import pickle
from datetime import date
import re

FILE_PATH = "data.pkl"  # Path to the data file

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
        # TODO: Add validation for name format here or ensure it's done before creating Contact
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
        # TODO: Check for duplicate contacts
        self.contacts.append(contact)

    # Remove contact by the contact object itself (found previously)
    def remove_contact(self, contact: Contact):
        # TODO: Handle case where contact is not in list? (Shouldn't happen if logic is correct)
        try:
            self.contacts.remove(contact)
        except ValueError:
            raise NotFoundError("contact_not_found_in_list")

    # ================ Find methods ================
    # Find contact by partial data: name, phone or email
    def find_contacts(self, part: str) -> list[Contact]:
        # TODO: Implement search logic across name, phones, and emails (case-insensitive?)
        result : list[Contact] = []
        # ...
        return result

    # Find contact by name (partial or full)
    def find_contact_by_name(self, name_part: str) -> list[Contact]:
        # TODO: Implement search logic by name (case-insensitive?)
        result : list[Contact] = []
        # ...
        return result

    # Find contact by phone (partial or full)
    def find_contact_by_phone(self, phone_part: str) -> list[Contact]:
        # TODO: Implement search logic by phone
        result : list[Contact] = []
        # ...
        return result

    # Find contact by email (partial or full)
    def find_contact_by_email(self, email_part: str) -> list[Contact]:
        # TODO: Implement search logic by email (case-insensitive?)
        result : list[Contact] = []
        # ...
        return result

    # Get contacts with birthdays in the next N days
    def get_birthdays_in_next_days(self, days: int) -> list[tuple[Contact, date | None]]:
        """
        Finds contacts whose birthdays fall within the next 'days' days.
        Calculates the celebration date (next Monday if birthday is on Sat/Sun).
        Returns a list of tuples: (Contact, celebration_date | None).
        None for celebration_date means celebrate on the actual birthday.
        """
        # TODO: Implement birthday calculation logic
        #       - Get today's date
        #       - Iterate through contacts with birthdays
        #       - Check if birthday falls within the range (today + 1 day) to (today + days)
        #       - Handle year wrap-around
        #       - Calculate celebration date (check weekday, adjust if Sat/Sun)
        result: list[tuple[Contact, date | None]] = []
        # ...
        return result


    # ================ Phone methods ================
    # Add contact phone number
    def add_phone(self, contact: Contact, phone_number: str):
        # TODO: Validate phone number format (e.g., 10 digits) using re
        # TODO: Check if phone number already exists for this contact
        # ...
        contact.phones.append(phone_number)

    # Change contact phone number by index (0-based)
    def change_phone(self, contact: Contact, phone_index: int, new_phone_number: str):
        # TODO: Validate new_phone_number format
        # TODO: Check if new_phone_number already exists (optional, based on requirements)
        # TODO: Validate index bounds
        # ...
        contact.phones[phone_index] = new_phone_number

    # Remove contact phone number by index (0-based)
    def remove_phone(self, contact: Contact, phone_index: int):
        # TODO: Validate index bounds
        # ...
        try:
            contact.phones.pop(phone_index)
        except IndexError:
            raise IndexError("invalid_phone_index")


    # ================ Email methods ================
    # Add contact email
    def add_email(self, contact: Contact, email: str):
        # TODO: Validate email format (simple regex)
        # TODO: Check if email already exists for this contact
        # ...
        contact.emails.append(email)

    # Change contact email by index (0-based)
    def change_email(self, contact: Contact, email_index: int, new_email: str):
        # TODO: Validate new_email format
        # TODO: Check if new_email already exists (optional)
        # TODO: Validate index bounds
        # ...
        contact.emails[email_index] = new_email

    # Remove contact email by index (0-based)
    def remove_email(self, contact: Contact, email_index: int):
        # TODO: Validate index bounds
        # ...
        try:
            contact.emails.pop(email_index)
        except IndexError:
            raise IndexError("invalid_email_index")


    # ================ Birthday methods ================
    # Change contact birthday (pass None to remove)
    def change_birthday(self, contact: Contact, new_birthday: date | None):
        # Input validation (format DD.MM.YYYY, valid date, range) should happen in the Controller before converting.
        # TODO: Potentially add checks here if date object could be invalid (e.g., range check bethween 1900 and today)
        # ...
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
        # TODO: Implement search logic across title and content with ignore case
        result : list[Note] = []
        # ...
        return result

    # Find note by title (partial or full)
    def find_note_by_title(self, title_part: str) -> list[Note]:
        # TODO: Implement search logic by title with ignore case
        result : list[Note] = []
        # ...
        return result

    # Find note by content (partial or full)
    def find_note_by_content(self, content_part: str) -> list[Note]:
        # TODO: Implement search logic by content with ignore case
        result : list[Note] = []
        # ...
        return result

    # Find note by tag (exact match, case-insensitive)
    def find_note_by_tag(self, tag: str) -> list[Note]:
        # Search should be case-insensitive as tags are stored  with ignore case
        # TODO: Implement search logic by tag
        result : list[Note] = []
        # ...
        return result


# ================ Data Persistence ================
def save_data_to_file(address_book: AdressBook, notebook: Notebook, file_path: str = FILE_PATH):
    try:
        # Backup the current data
        if os.path.exists(file_path):
            backup_path = file_path + ".bak"
            shutil.copy(file_path, backup_path)
            print(f"Backup saved to {backup_path}")

        # Data to be saved
        data = {
            "address_book": address_book,
            "notebook": notebook,
            "contact_id_counter": Contact.id_counter,
            "note_id_counter": Note.id_counter,
            "version": 1
        }

        # Save the data
        with open(file_path, "wb") as f:
            pickle.dump(data, f)
            print(f"Data saved to {file_path}")

    except (pickle.PicklingError, IOError) as e:
        print(f"Error saving data: {e}")
    except Exception as e:
        print(f"Unexpected error saving data: {e}")


def reset_data(file_path: str = FILE_PATH):
    """Completely clears the data and saves empty objects."""
    Contact.id_counter = 0
    Note.id_counter = 0
    address_book = AdressBook()
    notebook = Notebook()
    save_data_to_file(address_book, notebook, file_path)
    print("Data has been reset.")


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