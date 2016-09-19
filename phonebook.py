import pickle
import collections


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
        if isinstance(other, str):     # TODO: при вызове "in" первый раз приходит 2 класса после расчета хеша приходит
            return self.name == other  # TODO: класс и сторка
        if 'name' in other.__dict__:
            return self.name == other.name
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, str):
            return self.name < other
        if 'name' in other.__dict__:
            return self.name < other.name
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
        self._contacts[name]._change_phone(phone) # TODO важно что поле может изменять только через контейнер
        self.save_all()                           # TODO так как оно может быть не сохранено

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


class Controller:
    def __init__(self, view, file_storage):
        self.view = view
        self._contacts = Contacts(file_storage)
        # noinspection PyArgumentList
        self._commands = collections.OrderedDict([
            ('c', self.create_new_contact),
            ('u', self.update_contact),
            ('d', self.delete_contact),
            ('s', self.find_contact),
            ('l', self.find_all),
            ('h', self.help)
        ])

    def create_new_contact(self):
        """Create new contact in phone book"""
        name = self.view.input('name')
        phone = self.view.input('phone')
        new_contact = Contact(name, phone)
        try:
            self._contacts.append(new_contact)
            view.show('Contact successfully created.')
            view.show(self._contacts[name])
        except ExContactAlreadyExist as E:
            self.view.show_error(E)

    def update_contact(self):
        """Change phone number by contact name"""
        name = view.input('name')
        try:
            c = self._contacts[name]
            phone = view.input('phone')
            self._contacts.change_phone(name, phone)
            view.show('Contact successfully updated.')
            view.show(self._contacts[name])
        except ExContactDoesNotExist as E:
            view.show_error(E)

    def delete_contact(self):
        """Delete item from phone book"""
        name = view.input('name')
        try:
            self._contacts.delete_item(name)
            view.show('Contact {} successfully removed.'.format(name))
        except ExContactDoesNotExist as E:
            view.show_error(E)

    def find_contact(self):
        """Find contact in phone book by his name"""
        name = view.input('name')
        try:
            c = self._contacts[name]
            view.show(c)
        except ExContactDoesNotExist as E:
            view.show_error(E)

    def find_all(self):
        """Display all contacts"""
        if self._contacts:
            for contact in self._contacts:
                self.view.show(contact)
        else:
            self.view.show('Phone book is empty.')

    def _default(self):
        self.view.show_error('Incorrect command!\n{}'.format(self.get_help()))

    def help(self):
        """Show help"""
        view.show(self.get_help())

    def get_help(self):
        return '\n'.join("Use '{}' -> {}".format(key, self._commands[key].__doc__)for key in self._commands)

    def run(self):
        self.help()
        while True:
            command = view.get_input()
            if command == 'q':
                view.show("Have a nice day!")
                break
            else:
                self._commands.get(command, self._default)()


class View:
    def __init__(self):
        self.ERROR_FORMAT = "ERROR! {}"

    @staticmethod
    def check_name(self, name):
        return bool(name)

    @staticmethod
    def check_phone(self, phone):
        return bool(phone)

    def input(self, key):
        if key == 'name':
            while True:
                tmp = input('Please enter a name: ')
                if self.check_name(tmp):
                    return tmp
                else:
                    print('Please Enter correct name')

        elif key =='phone':
             while True:
                tmp = input('Please enter a phone: ')
                if self.check_phone(tmp):
                    return tmp
                else:
                    print('Please Enter correct phone number')

    def show_error(self, error):
        print(self.ERROR_FORMAT.format(error))

    @staticmethod
    def show(self, message):
        print(message)

    @staticmethod
    def get_input(self):
        return input('Enter a command (c, u, d, s, l, h) or q for exit: \n')


if __name__ == '__main__':
    view = View()
    controller = Controller(view, 'storage.pickle')
    controller.run()