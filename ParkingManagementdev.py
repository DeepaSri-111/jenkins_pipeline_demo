from datetime import datetime


class ParkingManagement:

    def __init__(self):
        # Slots are categorized by vehicle type
        self.slots = {
            "Bike": ["B1", "B2", "B3"],
            "Car": ["C1", "C2", "C3"],
            "SUV": ["S1", "S2"],
            "Truck": ["T1"],
            "Electric Vehicle": ["E1", "E2"]
        }

        self.occupied = {}
        self.ticket_counter = 1000

    # ------------------------------------------------
    # Find appropriate parking slot
    # ------------------------------------------------
    def allocate_slot(self, vehicle_type):

        if vehicle_type not in self.slots:
            return None

        for slot in self.slots[vehicle_type]:

            if slot not in self.occupied:
                return slot

        return None

    # ------------------------------------------------
    # Vehicle Entry
    # ------------------------------------------------
    def vehicle_entry(
        self,
        vehicle_number,
        vehicle_type,
        entry_hour,
        vip=False
    ):

        print("\n========== VEHICLE ENTRY ==========")

        # Check vehicle type
        if vehicle_type not in self.slots:
            print("Entry Failed: Invalid vehicle type")
            return None

        # Duplicate vehicle check
        if vehicle_number in self.occupied:
            print("Entry Failed: Vehicle already parked")
            return None

        # Allocate slot
        slot = self.allocate_slot(vehicle_type)

        if slot is None:
            print("Entry Failed: No suitable parking slot available")
            return None

        self.ticket_counter += 1

        ticket_id = "T" + str(self.ticket_counter)

        self.occupied[vehicle_number] = {
            "vehicle_type": vehicle_type,
            "slot": slot,
            "entry_hour": entry_hour,
            "ticket": ticket_id,
            "vip": vip
        }

        print("Vehicle Number :", vehicle_number)
        print("Vehicle Type   :", vehicle_type)
        print("Parking Slot   :", slot)
        print("Ticket ID      :", ticket_id)

        if vip:
            print("Parking Type   : VIP")

        print("Entry Successful")
        print("===================================")

        return ticket_id

    # ------------------------------------------------
    # Calculate parking fee
    # ------------------------------------------------
    def calculate_fee(
        self,
        vehicle_type,
        entry_hour,
        exit_hour,
        vip=False
    ):

        # Calculate parking hours
        if exit_hour < entry_hour:
            # Overnight parking
            duration = (24 - entry_hour) + exit_hour
        else:
            duration = exit_hour - entry_hour

        # Minimum 1 hour
        if duration <= 0:
            duration = 1

        # Base hourly rates
        rates = {
            "Bike": 20,
            "Car": 50,
            "SUV": 70,
            "Truck": 100,
            "Electric Vehicle": 50
        }

        base_rate = rates[vehicle_type]

        fee = duration * base_rate

        # Peak hour pricing: 8-10 AM and 5-8 PM
        peak_hours = [8, 9, 17, 18, 19]

        if entry_hour in peak_hours or exit_hour in peak_hours:
            fee *= 1.5

        # VIP discount
        if vip:
            fee *= 0.80

        return round(fee, 2)

    # ------------------------------------------------
    # EV charging fee
    # ------------------------------------------------
    def calculate_ev_charging_fee(self, charging_units):

        # Rs. 15 per charging unit
        return charging_units * 15

    # ------------------------------------------------
    # Vehicle Exit
    # ------------------------------------------------
    def vehicle_exit(
        self,
        vehicle_number,
        exit_hour,
        lost_ticket=False,
        charging_units=0
    ):

        print("\n========== VEHICLE EXIT ==========")

        # Check vehicle
        if vehicle_number not in self.occupied:
            print("Exit Failed: Vehicle not found")
            return None

        vehicle = self.occupied[vehicle_number]

        vehicle_type = vehicle["vehicle_type"]
        entry_hour = vehicle["entry_hour"]
        vip = vehicle["vip"]
        slot = vehicle["slot"]

        # Lost ticket
        if lost_ticket:

            # Fixed lost ticket penalty
            parking_fee = 500

            print("Lost Ticket Handling")
            print("Lost Ticket Charge : Rs.", parking_fee)

        else:

            parking_fee = self.calculate_fee(
                vehicle_type,
                entry_hour,
                exit_hour,
                vip
            )

        # EV charging
        charging_fee = 0

        if vehicle_type == "Electric Vehicle":

            charging_fee = self.calculate_ev_charging_fee(
                charging_units
            )

        total_fee = parking_fee + charging_fee

        print("Vehicle Number     :", vehicle_number)
        print("Vehicle Type       :", vehicle_type)
        print("Parking Slot       :", slot)
        print("Parking Fee        : Rs.", parking_fee)
        print("EV Charging Fee    : Rs.", charging_fee)
        print("Total Fee          : Rs.", total_fee)

        # Free slot after exit
        del self.occupied[vehicle_number]

        print("Slot Released      :", slot)
        print("Exit Successful")
        print("===================================")

        return total_fee

    # ------------------------------------------------
    # Display parking status
    # ------------------------------------------------
    def display_status(self):

        print("\n========== PARKING STATUS ==========")

        total_slots = sum(
            len(slots) for slots in self.slots.values()
        )

        occupied_slots = len(self.occupied)

        print("Total Slots    :", total_slots)
        print("Occupied Slots :", occupied_slots)
        print("Available Slots:", total_slots - occupied_slots)

        print("====================================")


# ------------------------------------------------
# DEVELOPMENT PROGRAM
# ------------------------------------------------

if __name__ == "__main__":

    parking = ParkingManagement()

    print("====================================")
    print(" SMART PARKING MANAGEMENT SYSTEM")
    print("====================================")

    parking.display_status()

    # Vehicle entry
    parking.vehicle_entry(
        "TN01AB1234",
        "Car",
        10
    )

    parking.display_status()

    # Vehicle exit
    parking.vehicle_exit(
        "TN01AB1234",
        15
    )

    parking.display_status()