import functools

class View:
    def check_name(self, name):
        return bool(name)

    def check_phone(self, phone):
        return bool(phone)

    def input(self, key):
        if key == 'name':
            while True:
                tmp = input('Please enter a name: ')
                if self.check_name(tmp):
                    return tmp

        elif key =='phone':
             while True:
                tmp = input('Please enter a phone: ')
                if self.check_phone(tmp):
                    return tmp

class Contact:
    def __init__(self, name, phone):
        self._name = name
        self._phone = phone
        self._hash = hash(self._name)

    @property
    def name(self):
        return self._name

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = value

    @phone.deleter
    def phone(self):
        raise KeyError('Readonly attribute')

    def __eq__(self, other):
        if 'name' in other.__dict__:
            return self.name == other.name
        return NotImplemented

    def __lt__(self, other):
        if 'name' in other.__dict__:
            return self.name < other.name
        return NotImplemented

    def __hash__(self):
        return self._hash