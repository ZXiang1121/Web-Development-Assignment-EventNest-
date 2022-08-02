import uuid
class Payment:

    customer_order = []
    
    def __init__(self, order_history):
        self.__payment_id = uuid.uuid4()
        self.__order_history = order_history
    
    def get_payment_id(self):
        return self.__payment_id

    def get_order_history(self):
        return self.__order_history

    
    def set_payment_id(self):
        return self.__payment_id


    def set_order_history(self, order_history):
        self.__order_history = order_history