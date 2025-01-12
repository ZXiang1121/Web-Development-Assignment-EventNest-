from Seat import Seat
import uuid

class Event:
    # count_id = 0

    seating_plan = []

    # def __init__(self, event_name,event_category, seat_type, seat_available, seat_price, event_location, event_date, event_time, event_image, event_desc):
    def __init__(self, event_name,event_category, event_location, event_date, event_time, event_poster, seat_image, event_desc):

        # Event.count_id += 1
        self.__event_id = uuid.uuid4()
        self.__event_name = event_name
        self.__event_category = event_category
        self.__event_location = event_location
        self.__event_date = event_date
        self.__event_time = event_time
        self.__event_poster = event_poster
        self.__seat_image = seat_image
        self.__event_desc = event_desc


    def get_event_id(self):
        return self.__event_id

    def get_event_name(self):
        return self.__event_name
    
    def get_event_category(self):
        return self.__event_category

    def get_event_location(self):
        return self.__event_location
    
    def get_event_date(self):
        return self.__event_date
    
    def get_event_time(self):
        return self.__event_time
    
    def get_event_poster(self):
        return self.__event_poster

    def get_seat_image(self):
        return self.__seat_image

    def get_event_desc(self):
        return self.__event_desc
    
    def get_seating_plan(self):
        return self.seating_plan



    def set_event_id(self, event_id):
        self.__event_id = event_id
    
    def set_event_name(self, event_name):
        self.__event_name = event_name
    
    def set_event_category(self, event_category):
        self.__event_category = event_category

    def set_event_location(self, event_location):
        self.__event_location = event_location

    def set_event_date(self, event_date):
        self.__event_date = event_date
    
    def set_event_time(self, event_time):
        self.__event_time = event_time

    def set_event_poster(self, event_poster):
        self.__event_poster = event_poster
        
    def set_seat_image(self, seat_image):
        self.__seat_image = seat_image

    def set_event_desc(self, event_desc):
        self.__event_desc = event_desc

    def set_seating_plan(self, seating_plan):
        self.seating_plan = seating_plan


