from Seat import Seat

class Event:
    count_id = 0

    seating_plan = []

    # def __init__(self, event_name,event_category, seat_type, seat_available, seat_price, event_location, event_date, event_time, event_image, event_desc):
    def __init__(self, event_name,event_category, event_location, event_date, event_time, event_poster, seat_image, event_desc):
        # Not sure of ticket id
        # super().__init__()
        Event.count_id += 1
        

        self.__event_id = Event.count_id
        self.__event_name = event_name
        self.__event_category = event_category
        # self.__seating_plan_entries = seating_plan_entries
        # self.__seat_type = seat_type
        # self.__seat_available = seat_available
        # self.__seat_price = seat_price
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
    
    # def get_seating_plan(self):
    #     return self.__seating_plan

    # def get_seating_plan_entries(self):
    #     return self.__seating_plan_entries

    # def get_seat_type(self):
    #     return self.__seat_type

    # def get_seat_available(self):
    #     return self.__seat_available

    # def get_seat_price(self):
    #     return self.__seat_price

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
    
    # def set_seating_plan_entries(self,seating_plan_entries):
    #     self.__seating_plan_entries = seating_plan_entries

    # def set_seat_type(self, seat_type):
    #     self.__seat_type = seat_type
    
    # def set_seat_available(self, seat_available):
    #     self.__seat_available = seat_available

    # def set_seat_price(self, seat_price):
    #     self.__seat_price = seat_price

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


# create_event1 = {}

# cont = ''

# while cont != 'stop':
#     event_name = input('Enter event name: ')
#     event_category = input('Enter event category: ')
    
#     seat = []
#     seat_plan = {}

#     event_seat_type = input('Enter event seat type: ')
#     event_seat_available = input('Enter event seat available: ')
#     event_seat_price = input('Enter event seat price: ')


#     create_event1['event_name'] = event_name
#     create_event1['event_category'] = event_category

#     seat_plan['event_seat_type'] = event_seat_type
#     seat_plan['event_seatAvailable'] = event_seat_available
#     seat_plan['event_seatPrice'] = event_seat_price

#     seat.append(seat_plan)

#     create_event1['seat'] = seat

#     cont = input('Continue to add seat field? (enter "stop" to break): ')
#     while cont != 'stop':
#         event_seat_type = input('Enter event seat type: ')
#         event_seat_available = input('Enter event seat available: ')
#         event_seat_price = input('Enter event seat price: ')

#         seat_plan['event_seat_type'] = event_seat_type
#         seat_plan['event_seatAvailable'] = event_seat_available
#         seat_plan['event_seatPrice'] = event_seat_price

#         seat.append(seat_plan)

#         create_event1['seat'] = seat

#         cont = input('Continue to add seat field? (enter "stop" to break): ')



# print(create_event1)



# create_event1 = {}
# def seatc():
#     seat = []
#     seat_plan = {}

#     event_seat_type = input('Enter event seat type: ')
#     event_seat_available = input('Enter event seat available: ')
#     event_seat_price = input('Enter event seat price: ')

#     seat_plan['event_seat_type'] = event_seat_type
#     seat_plan['event_seatAvailable'] = event_seat_available
#     seat_plan['event_seatPrice'] = event_seat_price

#     seat.append(seat_plan)

#     create_event1['seat'] = seat


# def test():
#     event_name = input('Enter event name: ')
#     event_category = input('Enter event category: ')
#     create_event1['event_name'] = event_name
#     create_event1['event_category'] = event_category

#     seatc()

#     cont = input('Continue to add seat field? (enter "stop" to break): ')
#     while cont != 'stop':


#         seatc()


#         cont = input('Continue to add seat field? (enter "stop" to break): ')



# test()
# print(create_event1)
