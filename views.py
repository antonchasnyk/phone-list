import socket
from  abc import ABC, abstractmethod
__all__ = ['ConsoleView', 'IPView']


class AbstractView(ABC):
    def __init__(self):
        self.ERROR_FORMAT = "ERROR!!! {}"

    def check_name(self, name):
        return bool(name)

    def check_phone(self, phone):
        return bool(phone)

    @abstractmethod
    def input(self, key):
        pass

    @abstractmethod
    def show_error(self, error):
        pass

    @abstractmethod
    def show(self, message):
        pass

    @abstractmethod
    def get_input(self):
        pass


class ConsoleView(AbstractView):
    def input(self, key):
        if key == 'name':
            while True:
                tmp = input('Please enter a name: ')
                if self.check_name(tmp):
                    return tmp
                else:
                    print('Please Enter correct name')

        elif key == 'phone':
            while True:
                tmp = input('Please enter a phone: ')
                if self.check_phone(tmp):
                    return tmp
                else:
                    print('Please Enter correct phone number')

    def show_error(self, error):
        print(self.ERROR_FORMAT.format(error))

    def show(self, message):
        print(message)

    def get_input(self):
        return input('Enter a command h for help or q for exit: \n')



class IPView(AbstractView):
    def __init__(self):
        super().__init__()
        s = socket.socket()
        s.bind(('localhost', 5000))
        s.listen(5)
        print('Server started')
        self.c, _ = s.accept()

    def input(self, key):
        if key == 'name':
            while True:
                self.c.sendall("Please input name".encode())
                tmp = self.c.recv(1024).decode()[:-2]
                if self.check_name(tmp):
                    return tmp
                else:
                    self.c.sendall('Please Enter correct name'.encode())

        elif key == 'phone':
            while True:
                self.c.sendall('Please enter a phone: '.encode())
                tmp = self.c.recv(1024).decode()[:-2]
                if self.check_phone(tmp):
                    return tmp
                else:
                    self.c.sendall('Please Enter correct phone number'.encode())

    def show_error(self, error):
        self.c.sendall(self.ERROR_FORMAT.format(str(error)).encode())

    def get_input(self):
        self.c.sendall('Enter a command h for help or q for exit: \n'.encode())
        return self.c.recv(1024).decode()[:-2]

    def show(self, message):
        self.c.sendall(str(message).encode())