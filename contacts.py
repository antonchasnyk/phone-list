import pickle

__all__ = ['ExContactAlreadyExist', 'ExContactDoesNotExist', 'Contact', 'Contacts']


class ExPhoneBook(Exception):
    def __init__(self, format_string, name, *args, **kwargs):
        super().__init__(str, *args, **kwargs)
        self.format_string = format_string
        self.name = name

    def __str__(self):
        return self.format_string.format(self.name)


class ExContactAlreadyExist(ExPhoneBook):
    pass


class ExContactDoesNotExist(ExPhoneBook):
    pass


class Contact:
    def __init__(self, name, phone):
        self._name = name
        self._phone = phone

    @property
    def name(self):
        return self._name

    @property
    def phone(self):
        return self._phone

    def _change_phone(self, value):
        self._phone = value

    @phone.deleter
    def phone(self):
        raise KeyError('Readonly attribute')

    def __eq__(self, other):
        if isinstance(other, str):
            return self._name == other
        if 'name' in other.__dict__:
            return self._name == other.name
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, str):
            return self._name < other
        if '_name' in other.__dict__:
            return self._name < other._name
        return NotImplemented

    def __hash__(self):
        return hash(self._name)

    def __repr__(self):
        return "{}('{}', '{}')".format(type(self).__name__, self.name, self.phone)

    def __str__(self):
        return '{:.<20}{:.>20}'.format(self.name, self.phone)


class Contacts:
    def __init__(self, filename):
        self.file_name = filename
        self._contacts = self.load()

    def load(self):
        try:
            with open(self.file_name, 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError, pickle.UnpicklingError):
            return {}

    def save_all(self):
        with open(self.file_name, 'wb') as f:
            pickle.dump(self._contacts, f)

    def append(self, p_object):
        if p_object in self._contacts:
            raise ExContactAlreadyExist('Contact {} already exist', p_object.name)
        self._contacts[p_object.name] = p_object
        self.save_all()

    def change_phone(self, name, phone):
        self.delete_item(name)
        self.append(Contact(name, phone))
        self.save_all()

    def delete_item(self, name):
        try:
            del self._contacts[name]
            self.save_all()
        except KeyError:
            raise ExContactDoesNotExist('Contact {} does not exist', name)

    def __getitem__(self, name):
        try:
            return self._contacts[name]
        except KeyError:
            raise ExContactDoesNotExist('Contact {} does not exist', name)

    def __contains__(self, item):
        return item.name in self._contacts

    def __bool__(self):
        if self._contacts:
            return True
        return False

    def __iter__(self):
        for contact in self._contacts:
            yield self._contacts[contact]

    def __str__(self):
        return str([(name, self._contacts[name].phone) for name in self._contacts])