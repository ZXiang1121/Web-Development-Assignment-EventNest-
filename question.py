class Qn:
    count_id = 0

    def __init__(self, first_name, last_name, email, number, comments):
        Qn.count_id +=1
        self.__qn_id = Qn.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__number = number
        self.__comments = comments



    def get_qn_id(self):
        return self.__qn_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_email(self):
        return self.__email

    def get_number(self):
        return self.__number

    def get_comments(self):
        return self.__comments





    def set_qn_id(self, qn_id):
        self.__qn_id = qn_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name =last_name

    def set_email(self, email):
        self.__email = email

    def set_number(self, number):
        self.__number = number

    def set_comments(self, comments):
        self.__comments = comments