from HospitalManagement import HospitalManagement


print("====================================")
print(" HOSPITAL MANAGEMENT QA TESTING")
print("====================================")


# Test Case 1
print("\nTEST CASE 1: Normal Patient")

HospitalManagement.generate_bill(
    "Arun",
    35,
    "Dr. Kumar",
    "General Medicine",
    "Normal",
    20,
    ["Blood Test"],
    500,
    False
)


# Test Case 2
print("\nTEST CASE 2: Emergency Patient")

HospitalManagement.generate_bill(
    "Priya",
    28,
    "Dr. Ravi",
    "Emergency",
    "Emergency",
    45,
    ["Blood Test", "X-Ray"],
    1000,
    False
)


# Test Case 3
print("\nTEST CASE 3: Senior Citizen")

HospitalManagement.generate_bill(
    "Raman",
    65,
    "Dr. Kumar",
    "Cardiology",
    "Normal",
    30,
    ["Blood Test", "CT Scan"],
    1500,
    False
)


# Test Case 4
print("\nTEST CASE 4: Insurance Patient")

HospitalManagement.generate_bill(
    "Meena",
    40,
    "Dr. Priya",
    "Orthopedics",
    "Normal",
    30,
    ["X-Ray", "MRI"],
    2000,
    True
)


# Test Case 5
print("\nTEST CASE 5: Follow-up Patient")

HospitalManagement.generate_bill(
    "Karthik",
    45,
    "Dr. Kumar",
    "General Medicine",
    "Follow-up",
    20,
    ["Blood Test"],
    300,
    False
)


print("\n====================================")
print(" ALL TEST SCENARIOS EXECUTED")
print("====================================")