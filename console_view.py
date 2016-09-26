__all__ = ['View']

class View:
    def __init__(self):
        self.ERROR_FORMAT = "ERROR!!! {}"

    @staticmethod
    def check_name(name):
        return bool(name)

    @staticmethod
    def check_phone(phone):
        return bool(phone)

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

    @staticmethod
    def show(message):
        print(message)

    @staticmethod
    def get_input():
        return input('Enter a command (c, u, d, s, l, h) or q for exit: \n')