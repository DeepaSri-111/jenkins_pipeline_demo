from AirlineReservationdev import AirlineReservation


print("==========================================")
print(" AIRLINE RESERVATION SYSTEM - QA TESTING")
print("==========================================")


# Create flight
airline = AirlineReservation(
    "AI101",
    "Chennai",
    "Delhi",
    20
)


# ------------------------------------------------
# TEST 1: Successful Booking
# ------------------------------------------------

print("\nTEST 1: SUCCESSFUL BOOKING")

result = airline.book_ticket(
    "P001",
    "Arun",
    "Adult",
    "Economy",
    30,
    1
)

print("Expected Result: Booking Successful")
print("Actual Result  :", result)


# ------------------------------------------------
# TEST 2: Double Booking
# ------------------------------------------------

print("\nTEST 2: DOUBLE BOOKING")

result = airline.book_ticket(
    "P001",
    "Arun",
    "Adult",
    "Economy",
    30,
    1
)

print("Expected Result: Booking Failed")
print("Actual Result  :", result)


# ------------------------------------------------
# TEST 3: Cancellation
# ------------------------------------------------

print("\nTEST 3: CANCELLATION")

refund = airline.cancel_ticket("P001")

print("Expected: Cancellation Successful")
print("Refund Amount:", refund)


# ------------------------------------------------
# TEST 4: Refund Calculation
# ------------------------------------------------

print("\nTEST 4: REFUND")

airline.book_ticket(
    "P002",
    "Priya",
    "Adult",
    "Business",
    30,
    1
)

refund = airline.cancel_ticket("P002")

print("Expected: 90% Refund")
print("Actual Refund: Rs.", round(refund, 2))


# ------------------------------------------------
# TEST 5: Fully Booked Flight
# ------------------------------------------------

print("\nTEST 5: FULLY BOOKED FLIGHT")

small_airline = AirlineReservation(
    "AI202",
    "Chennai",
    "Mumbai",
    2
)

small_airline.book_ticket(
    "P101",
    "Person1",
    "Adult",
    "Economy",
    30,
    1
)

small_airline.book_ticket(
    "P102",
    "Person2",
    "Adult",
    "Economy",
    30,
    1
)

result = small_airline.book_ticket(
    "P103",
    "Person3",
    "Adult",
    "Economy",
    30,
    1
)

print("Expected Result: Booking Failed")
print("Actual Result  :", result)


# ------------------------------------------------
# TEST 6: Invalid Passenger
# ------------------------------------------------

print("\nTEST 6: INVALID PASSENGER")

result = airline.book_ticket(
    "",
    "",
    "Adult",
    "Economy",
    30,
    1
)

print("Expected Result: Booking Failed")
print("Actual Result  :", result)


# ------------------------------------------------
# TEST 7: Excess Baggage
# ------------------------------------------------

print("\nTEST 7: EXCESS BAGGAGE")

baggage_charge = airline.calculate_baggage_charge(20)

print("Baggage Weight: 20 kg")
print("Free Weight   : 15 kg")
print("Expected Charge: Rs. 2500")
print("Actual Charge  : Rs.", baggage_charge)


# ------------------------------------------------
# TEST 8: Dynamic Fare Calculation
# ------------------------------------------------

print("\nTEST 8: DYNAMIC FARE CALCULATION")

normal_fare = airline.calculate_fare(
    30,
    1,
    "Adult",
    "Economy"
)

business_fare = airline.calculate_fare(
    30,
    1,
    "Adult",
    "Business"
)

first_class_fare = airline.calculate_fare(
    30,
    1,
    "Adult",
    "First Class"
)

print("Economy Fare    : Rs.", round(normal_fare, 2))
print("Business Fare   : Rs.", round(business_fare, 2))
print("First Class Fare: Rs.", round(first_class_fare, 2))


print("\n==========================================")
print(" ALL AIRLINE QA TESTS COMPLETED")
print("==========================================")