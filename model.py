# Model file by MVC pattern
# This file contains the model of the app
# It contains the data and the logic of the app

import main
import pickle
from datetime import date

FILE_PATH = "data.pkl"  # Path to the data file

class Contact:
    id_counter = 0

    def __init__(self, name: str):
        self.__id     = Contact.id_counter
        self.name     = name
        self.phones   : list[str] = []
        self.emails   : list[str] = []
        self.birthday : date      = None
        Contact.id_counter += 1

    @property
    def id(self) -> int:
        return self.__id


class AdressBook:
    def __init__(self):
        self.contacts : list[Contact] = []

    # ================ Contact methods ================
    # Add contact to address book
    def add_contact(self, contact):
        self.contacts.append(contact)

    # Remove contact
    def remove_contact(self, contact):
        self.contacts.remove(contact)

    # Change contact phone number by index
    def change_phone(self, contact, old_phone_index, new_phone_number):
        # TODO: not implemented yet
        pass

    # Find contact by partial data: name, phone or email
    def find_contacts(self, part: str) -> list[Contact]:
        # TODO: not implemented yet
        result : list[Contact] = []
        for contact in self.contacts:
            if False:
                result.append(contact)
        return result

    # Find contact by name (partial or full)
    def find_contact_by_name(self, name) -> list[Contact]:
        # TODO: not implemented yet
        result : list[Contact] = []
        for contact in self.contacts:
            if False:
                result.append(contact)
        return result

    # Find contact by phone (partial or full)
    def find_contact_by_phone(self, phone) -> list[Contact]:
        # TODO: not implemented yet
        result : list[Contact] = []
        for contact in self.contacts:
            if False:
                result.append(contact)
        return result

    # Find contact by email (partial or full)
    def find_contact_by_email(self, email) -> list[Contact]:
        # TODO: not implemented yet
        result : list[Contact] = []
        for contact in self.contacts:
            if False:
                result.append(contact)
        return result

    # ================ Phone methods ================
    # Add contact phone number
    def add_phone(self, contact, phone_number: str):
        # TODO: not implemented yet
        # Check if it already exists and validate phone number format
        contact.phones.append(phone_number)

    # Change contact phone number
    def change_phone(self, contact, old_phone_index, new_phone_number):
        # TODO: not implemented yet
        # Validate phone number format
        contact.phones[old_phone_index] = new_phone_number

    # Remove contact phone number by index
    def remove_phone(self, contact, phone_index):
        # TODO: not implemented yet
        contact.phones.pop(phone_index)

    # ================ Email methods ================
    # Add contact email
    def add_email(self, contact, email: str):
        # TODO: not implemented yet
        # Check if it already exists and validate email format
        contact.emails.append(email)

    # Change contact email by index
    def change_email(self, contact, old_email_index, new_email):
        # TODO: not implemented yet
        contact.emails[old_email_index] = new_email

    # Remove contact email by index
    def remove_email(self, contact, email_index):
        # TODO: not implemented yet
        contact.emails.pop(email_index)

    # ================ Birthday methods ================
    # Change contact birthday (including removal)
    def change_birthday(self, contact, new_birthday: date = None):
        # TODO: not implemented yet
        contact.birthday = new_birthday


class Note:
    id_counter = 0

    def __init__(self, title: str):
        self.__id    = Note.id_counter
        self.title   = title
        self.content = ""
        self.tags    : list[str] = []
        Note.id_counter += 1

    @property
    def id(self) -> int:
        return self.__id


class Notebook:
    def __init__(self):
        self.notes : list[Note] = []

    # ================ Note CRUD methods ================
    # Add note to notebook
    def add_note(self, note: Note):
        self.notes.append(note)

    # Change note title
    def change_note_title(self, note: Note, new_title: str = None):
        # TODO: not implemented yet
        pass

    # Change note content
    def change_note_content(self, note: Note, new_content: str = None):
        # TODO: not implemented yet
        pass

    # Remove note from notebook
    def remove_note(self, note: Note):
        # TODO: not implemented yet
        self.notes.remove(note)

    # ================ Note search methods ================
    # Find note by partial data: title or content
    def find_notes(self, part: str) -> list[Note]:
        # TODO: not implemented yet
        result : list[Note] = []
        for note in self.notes:
            pass
        return result

    # Find note by title (partial or full)
    def find_note_by_title(self, title: str) -> list[Note]:
        # TODO: not implemented yet
        result : list[Note] = []
        for note in self.notes:
            if False:
                result.append(note)
        return result

    # Find note by content (partial or full)
    def find_note_by_content(self, content: str) -> list[Note]:
        # TODO: not implemented yet
        result : list[Note] = []
        for note in self.notes:
            if False:
                result.append(note)
        return result
    
    # Find note by tag (partial or full)
    def find_note_by_tag(self, tag: str) -> list[Note]:
        # TODO: not implemented yet
        result : list[Note] = []
        for note in self.notes:
            if False:
                result.append(note)
        return result


# Load data from file and return AdressBook and Notebook objects
def load_data_from_file(file_path: str = FILE_PATH) -> tuple[AdressBook, Notebook]:
    # TODO: Add error handling for file exceptions
    with open(file_path, "rb") as f:
        address_book, notebook = pickle.load(f)
    return address_book, notebook

# Save AdressBook and Notebook objects to file
def save_data_to_file(address_book: AdressBook, notebook: Notebook, file_path: str = FILE_PATH):
    # TODO: Add error handling for file exceptions
    with open(file_path, "wb") as f:
        pickle.dump((address_book, notebook), f)


if __name__ == "__main__":
    main.main()