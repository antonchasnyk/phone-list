import pickle
FILE_NAME = 'phone_book.pickle'

class ExPhoneBook(Exception):
    pass

class ExNameExist(ExPhoneBook):
    def __init__(self, user_name, phone_number):
        self.name = user_name
        self.phone = phone_number

class ExNameNotExist(ExPhoneBook):
    def __init__(self, user_name):
        self.name = user_name

class ExEmptyList(ExPhoneBook):
    pass


def save_to_file(fn):
    def wrapper(self, *args, **kwargs):
        res = fn(self, *args, **kwargs)
        with open(self.file_name, 'wb') as f:
            pickle.dump(self._contacts, f)
        return res
    return wrapper


def input_user_name():
    user_name = input('Enter a user name:\n')
    return user_name


def input_user_phone():
    phone_number = input('Enter a user phone number:\n')
    return phone_number


class Contacts:

    def __init__(self, file_name):
        self.file_name = file_name
        self._contacts = []

    def load_contacts_from_file(self):
        try:
            with open(self.file_name, 'rb') as f:
                self._contacts = pickle.load(f)
        except (FileNotFoundError, pickle.UnpicklingError):
            self._contacts = {}

    @save_to_file
    def add_contact(self):
        user_name = input_user_name()
        phone_number = input_user_phone()
        if user_name in self._contacts:
            raise ExNameExist(user_name, phone_book[user_name])
        else:
            self._contacts[user_name] = phone_number

    @save_to_file
    def update_contact(self):
        user_name = input_user_name()
        if user_name in self._contacts:
            phone_number = input_user_phone()
            self._contacts[user_name] = phone_number
        else:
            raise ExNameNotExist(user_name)

    @save_to_file
    def delete_record(self):  # cruD
        user_name = input_user_name()
        try:
            self._contacts.pop(user_name)
        except KeyError:
            raise ExNameNotExist(user_name)

    def read_record(self):  # cRud (Model)
        user_name = input_user_name()
        try:
            phone_number = self._contacts[user_name]
            return '{} : {}'.format(user_name, phone_number)
        except KeyError:
            raise ExNameNotExist(user_name)

    def read_all(self):
        if self._contacts:
            for name in self._contacts:
                print('{} : {}'.format(name, self._contacts[name]))
        else:
            raise ExEmptyList()


def default():
    print("Incorrect input")

phone_book = Contacts('phone_book.pickl')

execute = {'c': phone_book.add_contact,
           'u': phone_book.update_contact,
           'd': phone_book.delete_record,
           's': phone_book.read_record,
           'l': phone_book.read_all}

while True:
    command = input('Enter a command (c, u, d, s, l) or q for exit: \n')
    try:
        if command == 'q':
            print("Have a nice day!")
            break
        else:
            execute.get(command, default)()

    except ExNameNotExist as E:
        print('User %s not exist ' % E.name)
    except ExNameExist as E:
        print('User already exist: %s : %s' %(E.name, E.phone))
    except ExEmptyList as E:
        print('Phone list is empty')