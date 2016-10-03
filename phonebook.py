from views import *
from contacts import *
from abc import abstractmethod, ABC

import collections


class AbstractController(ABC):

    def __init__(self, view, crud):
        self.view = view
        self.crud = crud

    @abstractmethod
    def create_new_contact(self):
        pass

    @abstractmethod
    def update_contact(self):
        pass

    @abstractmethod
    def update_contact(self):
        pass

    @abstractmethod
    def delete_contact(self):
        pass

    @abstractmethod
    def find_contact(self):
        pass

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def run(self):
        pass


class Controller(AbstractController):
    def __init__(self, view, file_storage):
        super().__init__(view, file_storage)
        # noinspection PyArgumentList
        self._commands = collections.OrderedDict([
            ('c', self.create_new_contact),
            ('u', self.update_contact),
            ('d', self.delete_contact),
            ('s', self.find_contact),
            ('l', self.find_all)
        ])

    def create_new_contact(self):
        """Create new contact in phone book"""
        name = self.view.input('name')
        phone = self.view.input('phone')
        try:
            res = crud.create(name, phone)
            self.view.show('Contact successfully created.')
            self.view.show(res)
        except ExContactAlreadyExist as E:
            self.view.show_error(E)

    def update_contact(self):
        """Change phone number by contact name"""
        name = view.input('name')
        try:
            res = crud.update(name, view.input)
            self.view.show('Contact successfully updated.')
            self.view.show(res)
        except ExContactDoesNotExist as E:
            view.show_error(E)

    def delete_contact(self):
        """Delete item from phone book"""
        name = view.input('name')
        try:
            crud.delete(name)
            self.view.show('Contact {} successfully removed.'.format(name))
        except ExContactDoesNotExist as E:
            self.view.show_error(E)

    def find_contact(self):
        """Find contact in phone book by his name"""
        name = self.view.input('name')
        try:
            res = crud.find(name)
            self.view.show(res)
        except ExContactDoesNotExist as E:
            self.view.show_error(E)

    def find_all(self):
        """Display all contacts"""
        try:
            res = crud.find_all()
            self.view.show(res)
        except ExContactBookEmpty  as E:
            self.view.show(E)

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
            elif command == 'h':
                self.help()
            else:
                self._commands.get(command, self._default)()


if __name__ == '__main__':
    view = ConsoleView()
    crud = FileCRUD('storage.pickle')
    controller = Controller(view, crud)
    controller.run()
