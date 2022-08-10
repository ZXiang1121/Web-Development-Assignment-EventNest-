class cdash:
    def __init__(self, order_name, price, date, quantity,order_category):        
        self.__order_name = order_name
        self.__order_category = order_category
        self.__event_date = date
        self.__order_seat_price = price
        self.__order_quantity = quantity


    def get_order_name(self):
        return self.__order_name

    def get_order_category(self):
        return self.__order_category
    
    def get_event_date(self):
        return self.__event_date

    def get_event_time(self):
        return self.__event_time

    def get_order_seat_price(self):
        return self.__order_seat_price
    
    def get_order_quantity(self):
        return self.__order_quantity
    

    def set_order_name(self, order_name):
        self.__order_name = order_name

    def set_order_category(self, order_category):
        self.__order_category = order_category

    def set_event_date(self, event_date):
        self.__event_date = event_date

    def set_order_seat_price(self, order_seat_price):
        self.__order_seat_price = order_seat_price
    
    def set_order_quantity(self, order_quantity):
        self.__order_quantity = order_quantity

    def set_order_seating_plan(self, order_seating_plan):
        self.__order_seating_plan = order_seating_plan


    def order_cost(self, order_seat_price, order_quantity):
        return int(order_seat_price) * int(order_quantity)