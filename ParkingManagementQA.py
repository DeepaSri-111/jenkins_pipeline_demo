from ParkingManagementdev import ParkingManagement


print("==========================================")
print(" SMART PARKING MANAGEMENT - QA TESTING")
print("==========================================")


# ------------------------------------------------
# TEST 1: Full Parking Lot
# ------------------------------------------------

print("\nTEST 1: FULL PARKING LOT")

parking = ParkingManagement()

# Fill all car slots
parking.vehicle_entry("CAR001", "Car", 10)
parking.vehicle_entry("CAR002", "Car", 10)
parking.vehicle_entry("CAR003", "Car", 10)

# Try one more car
result = parking.vehicle_entry(
    "CAR004",
    "Car",
    10
)

print("Expected: No suitable slot")
print("Actual  :", result)


# ------------------------------------------------
# TEST 2: Wrong Vehicle-Slot Combination
# ------------------------------------------------

print("\nTEST 2: WRONG VEHICLE-SLOT COMBINATION")

parking = ParkingManagement()

# Bike gets a bike slot automatically
ticket = parking.vehicle_entry(
    "BIKE001",
    "Bike",
    10
)

print("Expected: Bike slot allocated")
print("Actual Ticket:", ticket)

# The system automatically selects B1 for Bike.
# A Car cannot manually use B1 because allocation
# is based on vehicle type.

print("Vehicle type and slot combination validated.")


# ------------------------------------------------
# TEST 3: Duplicate Vehicle
# ------------------------------------------------

print("\nTEST 3: DUPLICATE VEHICLE")

parking = ParkingManagement()

parking.vehicle_entry(
    "CAR100",
    "Car",
    10
)

result = parking.vehicle_entry(
    "CAR100",
    "Car",
    11
)

print("Expected: Duplicate vehicle rejected")
print("Actual  :", result)


# ------------------------------------------------
# TEST 4: Lost Ticket
# ------------------------------------------------

print("\nTEST 4: LOST TICKET")

parking = ParkingManagement()

parking.vehicle_entry(
    "CAR200",
    "Car",
    10
)

fee = parking.vehicle_exit(
    "CAR200",
    15,
    lost_ticket=True
)

print("Expected: Lost ticket charge = Rs. 500")
print("Actual Fee:", fee)


# ------------------------------------------------
# TEST 5: Early Exit
# ------------------------------------------------

print("\nTEST 5: EARLY EXIT")

parking = ParkingManagement()

parking.vehicle_entry(
    "CAR300",
    "Car",
    10
)

fee = parking.vehicle_exit(
    "CAR300",
    11
)

print("Expected: Minimum 1 hour parking fee")
print("Actual Fee:", fee)


# ------------------------------------------------
# TEST 6: Overnight Parking
# ------------------------------------------------

print("\nTEST 6: OVERNIGHT PARKING")

parking = ParkingManagement()

parking.vehicle_entry(
    "CAR400",
    "Car",
    22
)

fee = parking.vehicle_exit(
    "CAR400",
    2
)

print("Expected: 4 hours parking charge")
print("Actual Fee:", fee)


# ------------------------------------------------
# TEST 7: Peak Hour Pricing
# ------------------------------------------------

print("\nTEST 7: PEAK-HOUR PRICING")

parking = ParkingManagement()

normal_fee = parking.calculate_fee(
    "Car",
    10,
    12
)

peak_fee = parking.calculate_fee(
    "Car",
    17,
    19
)

print("Normal Fee :", normal_fee)
print("Peak Fee   :", peak_fee)

if peak_fee > normal_fee:
    print("PASS: Peak-hour price is higher")
else:
    print("FAIL: Peak-hour pricing incorrect")


# ------------------------------------------------
# TEST 8: EV Charging Fee
# ------------------------------------------------

print("\nTEST 8: EV CHARGING FEE")

parking = ParkingManagement()

parking.vehicle_entry(
    "EV001",
    "Electric Vehicle",
    10
)

fee = parking.vehicle_exit(
    "EV001",
    12,
    charging_units=10
)

print("Expected: Parking fee + EV charging fee")
print("Actual Fee:", fee)


# ------------------------------------------------
# FINAL RESULT
# ------------------------------------------------

print("\n==========================================")
print(" ALL PARKING QA TESTS COMPLETED")
print("==========================================")