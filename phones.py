class ExNameExist(Exception):
    def __init__(self, user_name, phone_number):
        self.name = user_name
        self.phone = phone_number


class ExNameNotExist(Exception):
    def __init__(self, user_name):
        self.name = user_name


class ExEmptyList(Exception):
    pass


phonelist = {}


def add(user_name, phone_number):
    if user_name in phonelist:
        raise ExNameExist(user_name, phonelist[user_name])
    else:
        phonelist[user_name] = phone_number


def get(user_name):
    try:
        return (user_name, phonelist[user_name])
    except KeyError:
        raise ExNameNotExist(user_name)


def listdir():
    if phonelist:
        return phonelist
    else:
        raise ExEmptyList()


def update(user_name, phone_number):
    if user_name in phonelist:
        phonelist[user_name] = phone_number
    else:
        raise ExNameNotExist(user_name)


def del_user(user_name):
    try:
        phonelist.pop(user_name)
    except KeyError:
        raise ExNameNotExist(user_name)


def inun():
    user_name = input('Enter a user name:\n')
    return user_name

def inup():
    phone_number = input('Enter a user phone number:\n')
    return phone_number

while True:
    command = input('Enter a command (c, u, d, s, l) or exit for exit: \n')
    try:
        if command == 'c':
            add(inun(), inup())
        elif command == 'u':
            update(inun(), inup())
        elif command == 'd':
            del_user(inun())
        elif command == 's':
            print('%s:%s'% get(inun()))
        elif command == 'l':
            l = listdir()
            for name in l:
                print('%s:%s'% (name, l[name]))
        elif command == 'exit':
            print("Have a nice day!")
            break
    except ExNameNotExist as E:
        print('User not %s exist ' % E.name)
    except ExNameExist as E:
        print('User already exist %s:%s' %(E.name, E.phone))
    except ExEmptyList as E:
        print('Phone list is empty')