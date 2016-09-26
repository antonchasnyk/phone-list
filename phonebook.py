from console_view import *
from contacts import *

import collections


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
            self.view.show('Contact successfully created.')
            self.view.show(self._contacts[name])
        except ExContactAlreadyExist as E:
            self.view.show_error(E)

    def update_contact(self):
        """Change phone number by contact name"""
        name = view.input('name')
        try:
            c = self._contacts[name]
            phone = view.input('phone')
            self._contacts.change_phone(name, phone)
            self.view.show('Contact successfully updated.')
            self.view.show(self._contacts[name])
        except ExContactDoesNotExist as E:
            view.show_error(E)

    def delete_contact(self):
        """Delete item from phone book"""
        name = view.input('name')
        try:
            self._contacts.delete_item(name)
            self.view.show('Contact {} successfully removed.'.format(name))
        except ExContactDoesNotExist as E:
            self.view.show_error(E)

    def find_contact(self):
        """Find contact in phone book by his name"""
        name = self.view.input('name')
        try:
            c = self._contacts[name]
            self.view.show(c)
        except ExContactDoesNotExist as E:
            self.view.show_error(E)

    def find_all(self):
        """Display all contacts"""
        if self._contacts:
            print(self._contacts)
            print(self._contacts['Vas'] < self._contacts['anton'])
            for contact in sorted(self._contacts):
                self.view.show(contact)
        else:
            self.view.show('Phone book is empty.')

    def _default(self):
        self.view.show_error('Incorrect command!\n{}'.format(self.get_help()))

    def help(self):
        """Show help"""
        self.view.show(self.get_help())

    def get_help(self):
        return '\n'.join("Use '{}' -> {}".format(key, self._commands[key].__doc__)for key in self._commands)

    def run(self):
        self.help()
        while True:
            command = self.view.get_input()
            if command == 'q':
                self.view.show("Have a nice day!")
                break
            else:
                self._commands.get(command, self._default)()


if __name__ == '__main__':
    view = View()
    controller = Controller(view, 'storage.pickle')
    controller.run()
