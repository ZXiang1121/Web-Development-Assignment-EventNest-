class Event:
    count_id = 0

    def __init__(self, event_name,event_category, event_location, event_date, event_time, event_image, event_desc):
        # Not sure of ticket id
        Event.count_id += 1
        self.__event_id = Event.count_id
        self.__event_name = event_name
        self.__event_category = event_category
        # self.__seat_type = seat_type
        # self.__num_ticket = num_ticket
        self.__event_location = event_location
        self.__event_date = event_date
        self.__event_time = event_time
        # self.__event_price = event_price
        self.__event_image = event_image
        self.__event_desc = event_desc

    def get_event_id(self):
        return self.__event_id

    def get_event_name(self):
        return self.__event_name
    
    def get_event_category(self):
        return self.__event_category


    # def get_seat_type(self):
    #     return self.__seat_type

    # def get_num_ticket(self):
    #     return self.__num_ticket

    def get_event_location(self):
        return self.__event_location
    
    def get_event_date(self):
        return self.__event_date
    
    def get_event_time(self):
        return self.__event_time
    
    # def get_event_price(self):
    #     return self.__event_price
    
    def get_event_image(self):
        return self.__event_image

    def get_event_desc(self):
        return self.__event_desc



    def set_event_id(self, event_id):
        self.__event_id = event_id
    
    def set_event_name(self, event_name):
        self.__event_name = event_name
    
    def set_event_category(self, event_category):
        self.__event_category = event_category

    # def set_num_seatCat(self, seat_type):
    #     self.__seat_type = seat_type
    
    # def set_num_ticket(self, num_ticket):
    #     self.__num_ticket = num_ticket

    def set_event_location(self, event_location):
        self.__event_location = event_location

    def set_event_date(self, event_date):
        self.__event_date = event_date
    
    def set_event_time(self, event_time):
        self.__event_time = event_time

    # def set_event_price(self, event_price):
    #     self.__event_price = event_price

    def set_event_image(self, event_image):
        self._event_image = event_image


    def set_event_desc(self, event_desc):
        self.__event_desc = event_desc
