class Event:
    def __init__(self, event_name, num_seatCat, num_ticket, event_date, event_time, event_price, event_img, event_desc):
        # Not sure of ticket id
        self.__event_name = event_name
        self.__num_seatCat = num_seatCat
        self.__num_ticket = num_ticket
        self.__event_date = event_date
        self.__event_time = event_time
        self.__event_price = event_price
        self.__event_img = event_img
        self.__event_desc = event_desc

    def get_event_name(self):
        return self.__event_name

    def get_num_seatCat(self):
        return self.__num_seatCat

    def get_num_ticket(self):
        return self.__num_ticket
    
    def get_event_date(self):
        return self.__event_date
    
    def get_event_time(self):
        return self.__event_time
    
    def get_event_price(self):
        return self.__event_price
    
    def get_event_img(self):
        return self.__event_img

    def get_event_desc(self):
        return self.__event_desc

    
    def set_event_name(self, event_name):
        self.__event_name = event_name

    def set_num_seatCat(self, num_seatCat):
        self.__num_seatCat = num_seatCat
    
    def set_num_ticket(self, num_ticket):
        self.__num_ticket = num_ticket

    def set_event_date(self, event_date):
        self.__event_date = event_date
    
    def set_event_time(self, event_time):
        self.__event_time = event_time

    def set_event_price(self, event_price):
        self.__event_price = event_price

    def set_event_img(self, event_img):
        self._event_img = event_img
    def set_event_desc(self, event_desc):
        self._event_desc = event_desc


