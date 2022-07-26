class Seat:

    # def __init__(self, event_name,event_category, seat_type, ticket_available, seat_price, event_location, event_date, event_time, event_image, event_desc):
    def __init__(self, seat_type, seat_available, seat_price):
        # seating_plan = []
        self.__seat_type = seat_type
        self.__seat_available = seat_available
        self.__seat_price = seat_price



    def get_seat_type(self):
        return self.__seat_type

    def get_seat_available(self):
        return self.__seat_available

    def get_seat_price(self):
        return self.__seat_price



    def set_seat_type(self, seat_type):
        self.__seat_type = seat_type
    
    def set_seat_available(self, seat_available):
        self.__seat_available = seat_available

    def set_seat_price(self, seat_price):
        self.__seat_price = seat_price

    # def retrieve_seat_plan(self):
    #     seating_plan.append()
    #     return 

