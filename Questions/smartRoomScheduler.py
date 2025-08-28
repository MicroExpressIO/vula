
"""
Level 1: Room Inventory and Basic Booking
First, the system needs to know what rooms exist and be able to create a booking for a specific time.

Requirements:

Implement a Scheduler class.
"""

class Scheduler:
    def __init__(self):
        self.rooms = {}
    
    def add_room(self, name, capacity):
        """ add a new conferencd rooom to the system """
        # returns True if the room is added successfully
        # returns False if the room with the name already in exists.
        if name in self.rooms:
            return False
        self.rooms[name] = {
            'capacity': capacity,
            'bookings': []
        }
        return True
    
    def book_room(self, name, start_time, end_time):
        """ Schedules a booking for the room with the given name during the specified time slot. 
            For now, don't worry about booking conflicts; we'll add that in the next level.
            Returns True if the room exists and the booking is created.
            Returns False if the room does not exist.
            Level2: 
            - Modify the book_room(self, name, start_time, end_time) method to reject 
            any new booking that overlaps with an existing booking for that same room.
            - A conflict occurs if the new booking's time range intersects with any existing 
            booking's time range. For example, (900, 1000) conflicts with (930, 1030).
            - Bookings are "inclusive-exclusive," meaning (900, 1000) and (1000, 1100) do not 
            conflict.
            - The method should now return False if a conflict is detected."""
        if name not in self.rooms:
            return False
        for existing_start, existing_end in self.rooms[name]['bookings']:
            if (start_time < existing_end and end_time > existing_start):
                return False

        self.rooms[name]['bookings'].append((start_time, end_time))
        self.rooms[name]['bookings'].sort()
        return True
    

    def get_bookings(self, name): 
        """Returns a list of all bookings for a given room, sorted by their start_time.
            Each booking should be a tuple of (start_time, end_time).
            Returns None if the room does not exist."""
        if name not in self.rooms:
            return None
        
        return self.rooms[name]['bookings']
    
    """Level 3: Find Available Slot
        The most requested feature is to automatically find the next available time 
        for a meeting. This requires you to build on your existing logic to query 
        for open time slots.
    """
    def find_next_available_slot(self, name, duration):
        if name not in self.rooms:
            return None
        default_start = 0

        mybookings = self.rooms[name]['bookings']

        if not mybookings:
            return (default_start, default_start+duration)
        
        for start, end in mybookings:
            if start - default_start >= duration:
                return (default_start, duration)
            default_start = end

        if default_start + duration > 24:
            return None
        return (default_start, default_start + duration) 

        


def main():
    scheduler = Scheduler()
    # Add rooms
    scheduler.add_room("Room A", 10)
    scheduler.add_room("Room B", 20)
    scheduler.add_room("Room C", 30)    

    scheduler.book_room("Room A", 900, 1000)
    scheduler.book_room("Room A", 1100, 1200)
    scheduler.book_room("Room A", 1300, 1400)
    scheduler.book_room("Room B", 900, 1000)

    print("bookings for Room A:", scheduler.get_bookings("Room A"))

if __name__ == "__main__":
    main()