class Account:
    count_id = 99

    def __init__(self, name, email, password, birthdate):
        Account.count_id += 1

        self.__user_id = Account.count_id
        self.__name = name
        self.__email = email
        self.__password = password
        self.__birthdate = birthdate

    def get_user_id(self):
        return self.__user_id
    def set_user_id(self, user_id):
        self.__user_id = user_id

    def get_name(self):
        return self.__name
    def set_name(self, name):
        self.__name = name

    def get_email(self):
        return self.__email
    def set_email(self, email):
        self.__email = email

    def get_birthdate(self):
        return self.__birthdate
    def set_get_birthdate(self, birthdate):
        self.__birthdate = birthdate

    def get_password(self):
        return self.__password
    def set_password(self, password):
        self.__password = password
