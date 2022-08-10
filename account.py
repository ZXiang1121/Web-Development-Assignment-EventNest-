import uuid

class Account:

 

    def __init__(self, name, email, password, birthdate):

        self.__user_id = str(uuid.uuid4())
        self.__name = name
        self.__email = email
        self.__password = password
        self.__birthdate = birthdate
        self.__order_item = None

        self.__payment = []
        self.__cart_item = []
        self.__paid_item = []


        
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



    def get_cart_item(self):
        return self.__cart_item
        
    def set_cart_item(self, cart_item):
        self.__cart_item.append(cart_item)

    def get_payment(self):
        return self.__payment
    
    def set_payment(self,payment):
        self.__payment.append(payment)
    def get_paid_item(self):
        return self.__paid_item
    
    def set_paid_item(self, paid_item):
        self.__paid_item.append(paid_item)
