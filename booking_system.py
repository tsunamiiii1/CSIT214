import datetime

class Flight:
    def __init__(self, flight_number, destination, departure_time):
        self.flight_number = flight_number
        self.destination = destination
        self.departure_time = departure_time
        self.seats = {f"{row}{col}": None for row in "ABCD" for col in range(1, 7)}

    def seat(self):
        return [seat for seat, customer in self.seats.items() if customer is None]

    def customer_seat(self, seat_num, customer):
        if seat_num in self.seats and self.seats[seat_num] is None:
            self.seats[seat_num] = customer
            return True
        return False

class Customer:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class Booking:
    def __init__(self, customer, flight, seat, food, drink, return_flight=None, return_seat=None, return_food=None, return_drink=None):
        self.customer = customer
        self.flight = flight
        self.seat = seat
        self.food = food
        self.drink = drink
        self.return_flight = return_flight
        self.return_seat = return_seat
        self.return_food = return_food
        self.return_drink = return_drink
        self.time = datetime.datetime.now()

    def receipt(self):
        print("\n=== Booking Receipt ===")
        print(f"Name: {self.customer.name}")
        print(f"Email: {self.customer.email}")
        print(f"Flight: {self.flight.flight_number} to {self.flight.destination} at {self.flight.departure_time}")
        print(f"Seat: {self.seat}")
        print(f"Food: {self.food if self.food else 'None'}")
        print(f"Drink: {self.drink if self.drink else 'None'}")
        if self.return_flight:
            print("\n--- Return Flight Details ---")
            print(f"Return Flight: {self.return_flight.flight_number} to {self.return_flight.destination} at {self.return_flight.departure_time}")
            print(f"Seat: {self.return_seat}")
            print(f"Food: {self.return_food if self.return_food else 'None'}")
            print(f"Drink: {self.return_drink if self.return_drink else 'None'}")
        print(f"\nBooking Time: {self.time.strftime('%d-%m-%Y %H:%M:%S')}")

class BookingSystem:
    def __init__(self):
        self.customers = {}
        self.bookings = {}
        self.flights = [
            Flight("ABC114", "Sydney", "01-05-2024 10:00"),
            Flight("XYZ234", "Melbourne", "03-05-2024 12:00"),
            Flight("XYZ123", "Brisbane", "05-05-2024 14:00"),
            Flight("XYZ456", "Perth", "07-05-2024 16:00"),
            Flight("XYZ789", "Adelaide", "09-05-2024 18:00")
        ]
        self.food_menu = ["Sandwich", "Salad", "Chips"]
        self.drink_menu = ["Water", "Juice", "Coffee"]

    def main_menu(self):
        while True:
            print("\n=== FlyDreamAir Booking ===")
            print("1. Book a Flight")
            print("2. View Booking")
            print("3. Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                self.book_flight()
            elif choice == "2":
                self.view_booking()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")

    def book_flight(self):
        name = input("Enter your name: ")
        email = input("Enter your email: ")

        customer = Customer(name, email)
        self.customers[email] = customer

        # Book outgoing flight
        print("\nAvailable Flights:")
        for f in self.flights:
            print(f"{f.flight_number} - {f.destination} at {f.departure_time}")

        flight_number = input("Enter the flight number you want to book: ")
        flight = self.find_flight(flight_number)

        if not flight:
            print("Flight not found.")
            return

        print("\nAvailable Seats:")
        print(flight.seat())
        seat = input("Choose a seat: ")

        if not flight.customer_seat(seat, customer):
            print("Seat not available.")
            return

        food = self.choose_food()
        drink = self.choose_drink()

        return_flight = None
        return_seat = None
        return_food = None
        return_drink = None

        return_choice = input("\nDo you want to book a return flight? (yes/no): ").strip().lower()
        if return_choice == "yes":
            print("\nAvailable Return Flights:")
            for f in self.flights:
                if f.flight_number != flight.flight_number:
                    print(f"{f.flight_number} - {f.destination} at {f.departure_time}")

            return_flight_number = input("Enter the return flight number: ")
            return_flight = self.find_flight(return_flight_number)

            if not return_flight:
                print("Return flight not found.")
                return

            print("\nAvailable Seats for Return Flight:")
            print(return_flight.seat())
            return_seat = input("Choose a return seat: ")

            if not return_flight.customer_seat(return_seat, customer):
                print("Seat not available.")
                return

            return_food = self.choose_food()
            return_drink = self.choose_drink()

        booking = Booking(customer, flight, seat, food, drink, return_flight, return_seat, return_food, return_drink)
        self.bookings[email] = booking

        booking.receipt()
        print("\nBooking successful!")

    def view_booking(self):
        email = input("Enter your email: ")
        booking = self.bookings.get(email)

        if booking:
            booking.receipt()
        else:
            print("No booking found.")

    def choose_food(self):
        print("\nFood Menu:", self.food_menu)
        choice = input("Choose food (or press enter to skip): ")
        return choice if choice in self.food_menu else None

    def choose_drink(self):
        print("\nDrink Menu:", self.drink_menu)
        choice = input("Choose drink (or press enter to skip): ")
        return choice if choice in self.drink_menu else None

    def find_flight(self, flight_number):
        for f in self.flights:
            if f.flight_number == flight_number:
                return f
        return None
    
if __name__ == "__main__":
    booking_system = BookingSystem()
    booking_system.main_menu()
