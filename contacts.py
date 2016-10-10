import pickle
from abc import ABC, abstractmethod

__all__ = ['ExContactBookEmpty','ExContactAlreadyExist', 'ExContactDoesNotExist', 'Contact', 'Contacts', 'FileCRUD',
           'DBCRUD']


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


class ExContactBookEmpty(ExPhoneBook):
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

    @phone.deleter
    def phone(self):
        raise KeyError('Readonly attribute')

    @name.deleter
    def name(self):
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


class DBContacts:
    def __init__(self, db_name):
        import sqlite3
        import collections
        self.connection = sqlite3.connect(database='{}.sqlite3'.format(db_name))
        self.User = collections.namedtuple('User', 'name, phone')
        import atexit
        atexit.register(self.close)

    def close(self):
        self.connection.close()

    def append(self, p_object):
        rows = self.connection.execute("select * from phones  where name = '{}'".format(p_object.name))
        if rows.fetchone():
            raise ExContactAlreadyExist('Contact {} already exist', p_object.name)
        self.connection.execute("insert into phones (name, phone) values ('{}', '{}')".format(p_object.name, p_object.phone))
        self.connection.commit()

    def delete_item(self, name):
        rows = self.connection.execute("select * from phones  where name = '{}'".format(name))
        u = self.User._make(rows.fetchone())
        if u:
            self.connection.execute("delete from phones where name = '{}'".format(name))
            self.connection.commit()
        else:
            raise ExContactDoesNotExist('Contact {} does not exist', name)

    def __getitem__(self, name):
        rows = self.connection.execute("select * from phones  where name = '{}'".format(name))
        u = self.User._make(rows.fetchone())
        if u:
            return Contact(u.name, u.phone)
        else:
            raise ExContactDoesNotExist('Contact {} does not exist', name)

    def __contains__(self, item):
        rows = self.connection.execute("select * from phones  where name = '{}'".format(item.name))
        u = self.User._make(rows.fetchone())
        if u:
            return True
        else:
            return False

    def __bool__(self):
        rows = self.connection.execute("select * from phones")
        if rows.fetchone():
            return True
        return False

    def __iter__(self):
        rows = self.connection.execute("select * from phones")
        rows = rows.fetchall()
        for u in rows:
            t = self.User._make(u)
            yield Contact(t.name, t.phone)


class AbstractCRUD(ABC):
    _contacts = {}

    def create(self, name, phone):
        new_contact = Contact(name, phone)
        self._contacts.append(new_contact)
        return str(self._contacts[name])

    def update(self, name, inputer):
        c = self._contacts[name]
        phone = inputer('phone')
        new = Contact(c.name, phone)
        self._contacts.delete_item(c.name)
        self._contacts.append(new)
        return self._contacts[name]

    def delete(self, name):
        self._contacts.delete_item(name)

    def find(self, name):
        c = self._contacts[name]
        return str(c)

    def find_all(self):
        if self._contacts:
            res = []
            for contact in sorted(self._contacts):
                res.append(str(contact))
            return tuple(res)
        else:
            raise ExContactBookEmpty('Phone book is empty.')


class FileCRUD(AbstractCRUD):
    def __init__(self, file_storage):
        self._contacts = Contacts(file_storage)



class DBCRUD(AbstractCRUD):
    def __init__(self):
        self._contacts = DBContacts('phonebook')



