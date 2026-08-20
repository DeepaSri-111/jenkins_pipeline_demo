class HospitalManagement:

    # Calculate consultation fee
    @staticmethod
    def get_consultation_fee(appointment_type, duration):

        if appointment_type.lower() == "emergency":
            fee = 1000

        elif appointment_type.lower() == "follow-up":
            fee = 300

        else:
            fee = 500

        # Extra charge for consultation longer than 30 minutes
        if duration > 30:
            fee += 200

        return fee

    # Calculate lab charges
    @staticmethod
    def get_lab_charges(lab_tests):

        total = 0

        for test in lab_tests:

            if test.lower() == "blood test":
                total += 300

            elif test.lower() == "x-ray":
                total += 500

            elif test.lower() == "ct scan":
                total += 2000

            elif test.lower() == "mri":
                total += 3000

        return total

    # Calculate medicine charges
    @staticmethod
    def get_medicine_charges(medicine_cost):
        return medicine_cost

    # Calculate senior citizen discount
    @staticmethod
    def get_senior_discount(consultation_fee, age):

        if age >= 60:
            return consultation_fee * 0.10

        return 0

    # Calculate insurance coverage
    @staticmethod
    def get_insurance_coverage(total_amount, insurance):

        if insurance:
            return total_amount * 0.80

        return 0

    # Generate complete bill
    @staticmethod
    def generate_bill(
        patient_name,
        age,
        doctor,
        department,
        appointment_type,
        duration,
        lab_tests,
        medicine_cost,
        insurance
    ):

        consultation_fee = HospitalManagement.get_consultation_fee(
            appointment_type, duration
        )

        # Senior citizen discount
        senior_discount = HospitalManagement.get_senior_discount(
            consultation_fee, age
        )

        consultation_fee -= senior_discount

        # Lab charges
        lab_charges = HospitalManagement.get_lab_charges(lab_tests)

        # Medicine charges
        medicine_charges = HospitalManagement.get_medicine_charges(
            medicine_cost
        )

        # Total bill
        total_amount = (
            consultation_fee +
            lab_charges +
            medicine_charges
        )

        # Insurance
        insurance_coverage = HospitalManagement.get_insurance_coverage(
            total_amount, insurance
        )

        # Final payable amount
        patient_payable = total_amount - insurance_coverage

        # Display bill
        print("\n====================================")
        print("       HOSPITAL BILL")
        print("====================================")

        print(f"Patient Name       : {patient_name}")
        print(f"Age                : {age}")
        print(f"Doctor             : {doctor}")
        print(f"Department         : {department}")
        print(f"Appointment Type   : {appointment_type}")
        print(f"Consultation Time  : {duration} minutes")

        print("------------------------------------")

        print(f"Consultation Fee   : ₹{consultation_fee:.2f}")
        print(f"Lab Charges        : ₹{lab_charges:.2f}")
        print(f"Medicine Charges   : ₹{medicine_charges:.2f}")

        if age >= 60:
            print(f"Senior Discount    : ₹{senior_discount:.2f}")

        print(f"Total Bill         : ₹{total_amount:.2f}")
        print(f"Insurance Coverage : ₹{insurance_coverage:.2f}")

        print("------------------------------------")

        print(f"Patient Payable    : ₹{patient_payable:.2f}")

        print("====================================")

        return patient_payable


# Main program
if __name__ == "__main__":

    print("====================================")
    print(" HOSPITAL APPOINTMENT & BILLING")
    print("====================================")

    patient_name = input("Enter patient name: ")

    age = int(input("Enter age: "))

    doctor = input("Enter doctor name: ")

    department = input("Enter department: ")

    appointment_type = input(
        "Enter appointment type (Normal/Emergency/Follow-up): "
    )

    duration = int(
        input("Enter consultation duration in minutes: ")
    )

    number_of_tests = int(
        input("Enter number of lab tests: ")
    )

    lab_tests = []

    for i in range(number_of_tests):

        test = input(
            f"Enter lab test {i + 1} "
            "(Blood Test/X-Ray/MRI/CT Scan): "
        )

        lab_tests.append(test)

    medicine_cost = float(
        input("Enter medicine cost: ₹")
    )

    insurance_input = input(
        "Does patient have insurance? (yes/no): "
    )

    insurance = insurance_input.lower() == "yes"

    HospitalManagement.generate_bill(
        patient_name,
        age,
        doctor,
        department,
        appointment_type,
        duration,
        lab_tests,
        medicine_cost,
        insurance
    )