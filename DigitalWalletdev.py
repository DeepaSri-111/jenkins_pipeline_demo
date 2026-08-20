from datetime import datetime, timedelta
import threading


class DigitalWallet:

    DAILY_LIMIT = 50000
    LARGE_TRANSACTION_LIMIT = 20000
    MAX_TRANSACTIONS_10_MINUTES = 5
    MAX_FAILED_PIN_ATTEMPTS = 3

    def __init__(self):

        self.accounts = {}
        self.transactions = {}
        self.transaction_times = {}
        self.failed_pin_attempts = {}

        # Used for concurrent transaction safety
        self.lock = threading.Lock()

        self.transaction_counter = 1000

    # ==================================================
    # ACCOUNT CREATION
    # ==================================================

    def create_account(self, account_id, name, pin, initial_balance=0):

        if account_id in self.accounts:
            print("Account creation failed: Account already exists")
            return False

        if initial_balance < 0:
            print("Account creation failed: Negative balance")
            return False

        self.accounts[account_id] = {
            "name": name,
            "pin": str(pin),
            "balance": float(initial_balance),
            "daily_transaction": 0
        }

        self.transactions[account_id] = []
        self.transaction_times[account_id] = []
        self.failed_pin_attempts[account_id] = 0

        print("Account created successfully:", account_id)

        return True

    # ==================================================
    # PIN VERIFICATION
    # ==================================================

    def verify_pin(self, account_id, pin):

        if account_id not in self.accounts:
            return False

        account = self.accounts[account_id]

        if account["pin"] == str(pin):

            self.failed_pin_attempts[account_id] = 0
            return True

        self.failed_pin_attempts[account_id] += 1

        print(
            "Incorrect PIN. Failed attempts:",
            self.failed_pin_attempts[account_id]
        )

        return False

    # ==================================================
    # FRAUD DETECTION
    # ==================================================

    def fraud_detection(
        self,
        account_id,
        amount,
        current_time=None
    ):

        suspicious_reasons = []

        if current_time is None:
            current_time = datetime.now()

        # ----------------------------------------------
        # Large transaction
        # ----------------------------------------------

        if amount > self.LARGE_TRANSACTION_LIMIT:
            suspicious_reasons.append(
                "Large transaction"
            )

        # ----------------------------------------------
        # More than 5 transactions in 10 minutes
        # ----------------------------------------------

        ten_minutes_ago = current_time - timedelta(minutes=10)

        recent_transactions = []

        for transaction_time in self.transaction_times[account_id]:

            if transaction_time >= ten_minutes_ago:
                recent_transactions.append(transaction_time)

        if len(recent_transactions) >= self.MAX_TRANSACTIONS_10_MINUTES:
            suspicious_reasons.append(
                "More than 5 transactions in 10 minutes"
            )

        # ----------------------------------------------
        # Multiple failed PIN attempts
        # ----------------------------------------------

        if (
            self.failed_pin_attempts[account_id]
            >= self.MAX_FAILED_PIN_ATTEMPTS
        ):
            suspicious_reasons.append(
                "Multiple failed PIN attempts"
            )

        # ----------------------------------------------
        # Unusual transaction amount
        # ----------------------------------------------

        account_balance = self.accounts[account_id]["balance"]

        if amount > account_balance * 0.80 and account_balance > 0:
            suspicious_reasons.append(
                "Unusual transaction amount"
            )

        return suspicious_reasons

    # ==================================================
    # DEPOSIT
    # ==================================================

    def deposit(
        self,
        account_id,
        amount,
        pin,
        current_time=None
    ):

        if amount <= 0:
            print("Deposit failed: Amount must be positive")
            return False

        if account_id not in self.accounts:
            print("Deposit failed: Account not found")
            return False

        if not self.verify_pin(account_id, pin):
            print("Deposit failed: Invalid PIN")
            return False

        if current_time is None:
            current_time = datetime.now()

        with self.lock:

            account = self.accounts[account_id]

            # Daily limit
            if (
                account["daily_transaction"] + amount
                > self.DAILY_LIMIT
            ):
                print("Deposit failed: Daily transaction limit exceeded")
                return False

            fraud_flags = self.fraud_detection(
                account_id,
                amount,
                current_time
            )

            account["balance"] += amount
            account["daily_transaction"] += amount

            self.transaction_counter += 1

            transaction_id = "TX" + str(
                self.transaction_counter
            )

            self.transactions[account_id].append({
                "id": transaction_id,
                "type": "Deposit",
                "amount": amount
            })

            self.transaction_times[account_id].append(
                current_time
            )

            print(
                "Deposit successful. Transaction:",
                transaction_id
            )

            if fraud_flags:
                print("FRAUD ALERT:", fraud_flags)

            return True

    # ==================================================
    # WITHDRAWAL
    # ==================================================

    def withdraw(
        self,
        account_id,
        amount,
        pin,
        current_time=None
    ):

        if amount <= 0:
            print("Withdrawal failed: Amount must be positive")
            return False

        if account_id not in self.accounts:
            print("Withdrawal failed: Account not found")
            return False

        if not self.verify_pin(account_id, pin):
            print("Withdrawal failed: Invalid PIN")
            return False

        if current_time is None:
            current_time = datetime.now()

        with self.lock:

            account = self.accounts[account_id]

            # Balance verification
            if amount > account["balance"]:
                print("Withdrawal failed: Insufficient balance")
                return False

            # Daily limit
            if (
                account["daily_transaction"] + amount
                > self.DAILY_LIMIT
            ):
                print("Withdrawal failed: Daily limit exceeded")
                return False

            fraud_flags = self.fraud_detection(
                account_id,
                amount,
                current_time
            )

            account["balance"] -= amount
            account["daily_transaction"] += amount

            self.transaction_counter += 1

            transaction_id = "TX" + str(
                self.transaction_counter
            )

            self.transactions[account_id].append({
                "id": transaction_id,
                "type": "Withdrawal",
                "amount": amount
            })

            self.transaction_times[account_id].append(
                current_time
            )

            print(
                "Withdrawal successful. Transaction:",
                transaction_id
            )

            if fraud_flags:
                print("FRAUD ALERT:", fraud_flags)

            return True

    # ==================================================
    # MONEY TRANSFER
    # ==================================================

    def transfer(
        self,
        sender_id,
        receiver_id,
        amount,
        pin,
        current_time=None
    ):

        if amount <= 0:
            print("Transfer failed: Amount must be positive")
            return False

        if sender_id not in self.accounts:
            print("Transfer failed: Sender not found")
            return False

        if receiver_id not in self.accounts:
            print("Transfer failed: Receiver not found")
            return False

        if sender_id == receiver_id:
            print("Transfer failed: Sender and receiver cannot be same")
            return False

        if not self.verify_pin(sender_id, pin):
            print("Transfer failed: Invalid PIN")
            return False

        if current_time is None:
            current_time = datetime.now()

        with self.lock:

            sender = self.accounts[sender_id]
            receiver = self.accounts[receiver_id]

            # Balance verification
            if amount > sender["balance"]:
                print("Transfer failed: Insufficient balance")
                return False

            # Daily limit
            if (
                sender["daily_transaction"] + amount
                > self.DAILY_LIMIT
            ):
                print("Transfer failed: Daily limit exceeded")
                return False

            fraud_flags = self.fraud_detection(
                sender_id,
                amount,
                current_time
            )

            # Transfer money
            sender["balance"] -= amount
            receiver["balance"] += amount

            sender["daily_transaction"] += amount

            self.transaction_counter += 1

            transaction_id = "TX" + str(
                self.transaction_counter
            )

            self.transactions[sender_id].append({
                "id": transaction_id,
                "type": "Transfer Sent",
                "amount": amount,
                "to": receiver_id
            })

            self.transactions[receiver_id].append({
                "id": transaction_id,
                "type": "Transfer Received",
                "amount": amount,
                "from": sender_id
            })

            self.transaction_times[sender_id].append(
                current_time
            )

            print(
                "Transfer successful. Transaction:",
                transaction_id
            )

            if fraud_flags:
                print("FRAUD ALERT:", fraud_flags)

            return True

    # ==================================================
    # TRANSACTION HISTORY
    # ==================================================

    def show_transaction_history(self, account_id):

        if account_id not in self.accounts:
            print("Account not found")
            return

        print("\n========== TRANSACTION HISTORY ==========")

        history = self.transactions[account_id]

        if not history:
            print("No transactions found")

        for transaction in history:
            print(transaction)

        print("=========================================")

    # ==================================================
    # BALANCE
    # ==================================================

    def get_balance(self, account_id):

        if account_id not in self.accounts:
            return None

        return self.accounts[account_id]["balance"]


# ======================================================
# DEVELOPMENT PROGRAM
# ======================================================

if __name__ == "__main__":

    wallet = DigitalWallet()

    print("========================================")
    print(" DIGITAL WALLET AND FRAUD DETECTION")
    print("========================================")

    wallet.create_account(
        "A001",
        "Deepa",
        "1234",
        30000
    )

    wallet.create_account(
        "A002",
        "Arun",
        "5678",
        10000
    )

    wallet.deposit(
        "A001",
        5000,
        "1234"
    )

    wallet.withdraw(
        "A001",
        2000,
        "1234"
    )

    wallet.transfer(
        "A001",
        "A002",
        3000,
        "1234"
    )

    print(
        "\nFinal Balance:",
        wallet.get_balance("A001")
    )

    wallet.show_transaction_history("A001")
