class AirlineReservation:

    def __init__(self, flight_no, source, destination, total_seats):
        self.flight_no = flight_no
        self.source = source
        self.destination = destination
        self.total_seats = total_seats
        self.available_seats = total_seats
        self.bookings = {}

    # Flight search
    def search_flight(self):
        print("\n========== FLIGHT DETAILS ==========")
        print("Flight Number      :", self.flight_no)
        print("Source             :", self.source)
        print("Destination        :", self.destination)
        print("Total Seats        :", self.total_seats)
        print("Available Seats    :", self.available_seats)
        print("====================================")

    # Seat availability
    def check_seat_availability(self):
        return self.available_seats

    # Dynamic pricing
    def calculate_fare(
        self,
        travel_date,
        booking_date,
        passenger_type,
        seat_class
    ):

        # Base fare based on class
        if seat_class.lower() == "economy":
            base_fare = 5000

        elif seat_class.lower() == "business":
            base_fare = 10000

        elif seat_class.lower() == "first class":
            base_fare = 20000

        else:
            return None

        # Price increases when seats are low
        if self.available_seats <= 5:
            seat_multiplier = 1.50

        elif self.available_seats <= 10:
            seat_multiplier = 1.25

        else:
            seat_multiplier = 1.00

        # Booking close to travel date
        if booking_date >= travel_date - 7:
            date_multiplier = 1.30

        elif booking_date >= travel_date - 30:
            date_multiplier = 1.15

        else:
            date_multiplier = 1.00

        # Passenger discount
        if passenger_type.lower() == "child":
            passenger_multiplier = 0.75

        elif passenger_type.lower() == "senior":
            passenger_multiplier = 0.90

        elif passenger_type.lower() == "adult":
            passenger_multiplier = 1.00

        else:
            return None

        final_fare = (
            base_fare
            * seat_multiplier
            * date_multiplier
            * passenger_multiplier
        )

        return final_fare

    # Passenger booking
    def book_ticket(
        self,
        passenger_id,
        passenger_name,
        passenger_type,
        seat_class,
        travel_date,
        booking_date
    ):

        print("\n========== BOOKING ==========")

        # Validate passenger
        if not passenger_id or not passenger_name:
            print("Booking Failed: Invalid passenger")
            return False

        # Check duplicate booking
        if passenger_id in self.bookings:
            print("Booking Failed: Passenger already booked")
            return False

        # Check seat availability
        if self.available_seats <= 0:
            print("Booking Failed: Flight is fully booked")
            return False

        # Calculate fare
        fare = self.calculate_fare(
            travel_date,
            booking_date,
            passenger_type,
            seat_class
        )

        if fare is None:
            print("Booking Failed: Invalid passenger type or class")
            return False

        # Create booking
        self.bookings[passenger_id] = {
            "name": passenger_name,
            "type": passenger_type,
            "class": seat_class,
            "fare": fare
        }

        self.available_seats -= 1

        print("Passenger          :", passenger_name)
        print("Passenger ID       :", passenger_id)
        print("Class              :", seat_class)
        print("Passenger Type     :", passenger_type)
        print("Fare               : Rs.", round(fare, 2))
        print("Booking Successful")
        print("============================")

        return True

    # Cancellation and refund
    def cancel_ticket(self, passenger_id):

        print("\n========== CANCELLATION ==========")

        if passenger_id not in self.bookings:
            print("Cancellation Failed: Booking not found")
            return 0

        booking = self.bookings[passenger_id]

        fare = booking["fare"]

        # 90% refund
        refund = fare * 0.90

        del self.bookings[passenger_id]

        self.available_seats += 1

        print("Passenger          :", booking["name"])
        print("Original Fare      : Rs.", round(fare, 2))
        print("Refund Amount      : Rs.", round(refund, 2))
        print("Cancellation Successful")
        print("==================================")

        return refund

    # Baggage charges
    def calculate_baggage_charge(self, baggage_weight):

        free_baggage = 15

        if baggage_weight <= free_baggage:
            charge = 0

        else:
            extra_weight = baggage_weight - free_baggage

            # Rs. 500 per extra kg
            charge = extra_weight * 500

        return charge


# Development execution
if __name__ == "__main__":

    airline = AirlineReservation(
        "AI101",
        "Chennai",
        "Delhi",
        20
    )

    airline.search_flight()

    fare = airline.calculate_fare(
        travel_date=30,
        booking_date=1,
        passenger_type="Adult",
        seat_class="Economy"
    )

    print("\nDynamic Economy Fare: Rs.", round(fare, 2))

    airline.book_ticket(
        "P001",
        "Deepa",
        "Adult",
        "Economy",
        30,
        1
    )

    baggage_charge = airline.calculate_baggage_charge(20)

    print("Baggage Charge: Rs.", baggage_charge)

    airline.search_flight()