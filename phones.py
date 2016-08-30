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


phone_book = {}


def input_user_name():
    user_name = input('Enter a user name:\n')
    return user_name


def input_user_phone():
    phone_number = input('Enter a user phone number:\n')
    return phone_number


def create_record():  # Crud (Model)
    user_name = input_user_name()
    phone_number = input_user_phone()
    if user_name in phone_book:
        raise ExNameExist(user_name, phone_book[user_name])
    else:
        phone_book[user_name] = phone_number


def read_record():  # cRud (Model)
    user_name = input_user_name()
    try:
        phone_number = phone_book[user_name]
        print('{} : {}'.format(user_name, phone_number))
    except KeyError:
        raise ExNameNotExist(user_name)


def update_record():  # crUd (Model)
    user_name = input_user_name()
    if user_name in phone_book:
        phone_number = input_user_phone()
        phone_book[user_name] = phone_number
    else:
        raise ExNameNotExist(user_name)


def delete_record():  # cruD
    user_name = input_user_name()
    try:
        phone_book.pop(user_name)
    except KeyError:
        raise ExNameNotExist(user_name)


def read_all():
    if phone_book:
        for name in phone_book:
            print('{} : {}'.format(name, phone_book[name]))
    else:
        raise ExEmptyList()


def default():
    print("Incorrect input")

execute = {'c': create_record,
           'u': update_record,
           'd': delete_record,
           's': read_record,
           'l': read_all}

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