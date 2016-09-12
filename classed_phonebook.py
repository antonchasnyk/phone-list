import functools


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

    def __eq__(self, other):
        if 'name' in other.__dict__:
            return self.name == other.name
        return NotImplemented

    def __lt__(self, other):
        if 'name' in other.__dict__:
            return self.name < other.name
        return NotImplemented

    def