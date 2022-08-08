import uuid

class Order:
    # count_id = 0




    def __init__(self, event_id, order_name, order_category, event_location, order_image, order_seat_image, event_date, event_time, event_desc, order_seat_type, order_seat_price, order_quantity, order_seating_plan):
        
        
        self.__order_id = uuid.uuid4()
        self.__event_id = event_id
        self.__order_name = order_name
        self.__order_category = order_category
        self.__event_location = event_location
        self.__order_image = order_image
        self.__order_seat_image = order_seat_image
        self.__event_date = event_date
        self.__event_time = event_time
        self.__event_desc = event_desc
        self.__order_seat_type = order_seat_type
        self.__order_seat_price = order_seat_price
        self.__order_quantity = order_quantity
        self.__order_seating_plan = order_seating_plan
        # self.__order_cost = order_cost
    
    def get_order_id(self):
        return self.__order_id
    
    def get_event_id(self):
        return self.__event_id

    def get_order_name(self):
        return self.__order_name

    def get_order_category(self):
        return self.__order_category
    
    def get_event_location(self):
        return self.__event_location

    def get_order_image(self):
        return self.__order_image
    
    def get_order_seat_image(self):
        return self.__order_seat_image
    
    def get_event_date(self):
        return self.__event_date

    def get_event_time(self):
        return self.__event_time
    
    def get_event_desc(self):
        return self.__event_desc

    def get_order_seat_type(self):
        return self.__order_seat_type

    def get_order_seat_price(self):
        return self.__order_seat_price
    
    def get_order_quantity(self):
        return self.__order_quantity

    def get_order_seating_plan(self):
        return self.__order_seating_plan
    
    


    def set_order_id(self, order_id):
        self.__order_id = order_id

    def set_event_id(self, event_id):
         self.__event_id = event_id

    def set_order_name(self, order_name):
        self.__order_name = order_name

    def set_order_category(self, order_category):
        self.__order_category = order_category
    
    def set_event_location(self, event_location):
        self.__event_location = event_location
    
    def set_order_seat_image(self, order_seat_image):
        self.__order_seat_image = order_seat_image
    
    def set_event_time(self, event_time):
        self.__event_time = event_time
    
    def set_event_desc(self, event_desc):
        self.__event_desc = event_desc

    def set_order_image(self, order_image):
        self.__order_image = order_image

    def set_event_date(self, event_date):
        self.__event_date = event_date

    def set_order_seat_type(self, order_seat_type):
        self.__order_seat_type = order_seat_type

    def set_order_seat_price(self, order_seat_price):
        self.__order_seat_price = order_seat_price
    
    def set_order_quantity(self, order_quantity):
        self.__order_quantity = order_quantity

    def set_order_seating_plan(self, order_seating_plan):
        self.__order_seating_plan = order_seating_plan


    def order_cost(self, order_seat_price, order_quantity):
        return int(order_seat_price) * int(order_quantity)


    


    


