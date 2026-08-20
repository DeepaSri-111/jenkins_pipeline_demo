from DigitalWalletdev import DigitalWallet
from datetime import datetime, timedelta
import threading


print("==========================================")
print(" DIGITAL WALLET - SECURITY QA TESTING")
print("==========================================")


# ==================================================
# TEST 1: NORMAL TRANSACTION
# ==================================================

print("\nTEST 1: NORMAL TRANSACTION")

wallet = DigitalWallet()

wallet.create_account(
    "A001",
    "Arun",
    "1234",
    10000
)

result = wallet.deposit(
    "A001",
    1000,
    "1234"
)

print("Expected: True")
print("Actual  :", result)


# ==================================================
# TEST 2: INSUFFICIENT BALANCE
# ==================================================

print("\nTEST 2: INSUFFICIENT BALANCE")

result = wallet.withdraw(
    "A001",
    50000,
    "1234"
)

print("Expected: False")
print("Actual  :", result)


# ==================================================
# TEST 3: DAILY TRANSACTION LIMIT
# ==================================================

print("\nTEST 3: DAILY TRANSACTION LIMIT")

wallet = DigitalWallet()

wallet.create_account(
    "A002",
    "Priya",
    "2222",
    60000
)

result = wallet.deposit(
    "A002",
    50000,
    "2222"
)

result2 = wallet.deposit(
    "A002",
    1000,
    "2222"
)

print("First transaction:", result)
print("Second transaction:", result2)

print("Expected: Second transaction should fail")


# ==================================================
# TEST 4: MULTIPLE FAILED PINS
# ==================================================

print("\nTEST 4: MULTIPLE FAILED PINS")

wallet = DigitalWallet()

wallet.create_account(
    "A003",
    "Kumar",
    "3333",
    10000
)

wallet.withdraw(
    "A003",
    1000,
    "1111"
)

wallet.withdraw(
    "A003",
    1000,
    "1111"
)

wallet.withdraw(
    "A003",
    1000,
    "1111"
)

print("Expected: Multiple failed PIN attempts detected")

flags = wallet.fraud_detection(
    "A003",
    1000
)

print("Fraud Flags:", flags)


# ==================================================
# TEST 5: SUSPICIOUS TRANSACTION
# ==================================================

print("\nTEST 5: SUSPICIOUS TRANSACTION")

wallet = DigitalWallet()

wallet.create_account(
    "A004",
    "Meena",
    "4444",
    30000
)

result = wallet.withdraw(
    "A004",
    25000,
    "4444"
)

print("Expected: Transaction completed with fraud alert")
print("Actual  :", result)


# ==================================================
# TEST 6: DUPLICATE TRANSACTION
# ==================================================

print("\nTEST 6: DUPLICATE TRANSACTION")

wallet = DigitalWallet()

wallet.create_account(
    "A005",
    "Ravi",
    "5555",
    10000
)

# First transaction
result1 = wallet.withdraw(
    "A005",
    1000,
    "5555"
)

# Same transaction attempted again
result2 = wallet.withdraw(
    "A005",
    1000,
    "5555"
)

print("First Transaction :", result1)
print("Duplicate Attempt :", result2)

print(
    "Note: The system uses transaction IDs "
    "to distinguish transactions."
)


# ==================================================
# TEST 7: NEGATIVE AMOUNT
# ==================================================

print("\nTEST 7: NEGATIVE AMOUNT")

wallet = DigitalWallet()

wallet.create_account(
    "A006",
    "Suresh",
    "6666",
    10000
)

result = wallet.deposit(
    "A006",
    -500,
    "6666"
)

print("Expected: False")
print("Actual  :", result)


# ==================================================
# TEST 8: CONCURRENT TRANSACTIONS
# ==================================================

print("\nTEST 8: CONCURRENT TRANSACTIONS")

wallet = DigitalWallet()

wallet.create_account(
    "A007",
    "Concurrent User",
    "7777",
    10000
)


def make_transaction():

    wallet.withdraw(
        "A007",
        1000,
        "7777"
    )


threads = []

for i in range(5):

    thread = threading.Thread(
        target=make_transaction
    )

    threads.append(thread)
    thread.start()


for thread in threads:
    thread.join()


print(
    "Final Balance:",
    wallet.get_balance("A007")
)

print(
    "Expected Balance: 5000"
)


# ==================================================
# ADDITIONAL FRAUD TEST
# More than 5 transactions in 10 minutes
# ==================================================

print("\nADDITIONAL TEST: RAPID TRANSACTIONS")

wallet = DigitalWallet()

wallet.create_account(
    "A008",
    "Fraud Test",
    "8888",
    20000
)

base_time = datetime.now()

for i in range(6):

    wallet.deposit(
        "A008",
        100,
        "8888",
        base_time + timedelta(minutes=i)
    )

flags = wallet.fraud_detection(
    "A008",
    100,
    base_time + timedelta(minutes=6)
)

print("Fraud Flags:", flags)

print("\n==========================================")
print(" ALL WALLET QA TESTS COMPLETED")
print("==========================================")