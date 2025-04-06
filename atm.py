# Initial setup
correct_pin = "1234"
balance = 5000

# Functions
def insert_card():
    card = input("Please insert your card (Enter any key to simulate): ")
    if card:
        print("Card inserted successfully.")
        return True
    else:
        print("No card inserted. Please try again.")
        return False

def check_pin():
    pin = input("Enter your 4-digit PIN: ")
    return pin == correct_pin

def show_menu():
    print("\n--- ATM Menu ---")
    print("1. Check Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Exit")

def check_balance(balance):
    print(f"Your current balance is ₹{balance}")
    return balance

def deposit(balance):
    amount = float(input("Enter amount to deposit: ₹"))
    if amount > 0:
        balance += amount
        print(f"₹{amount} deposited successfully.")
    else:
        print("Enter a valid amount.")
    return balance

def withdraw(balance):
    amount = float(input("Enter amount to withdraw: ₹"))
    if 0 < amount <= balance:
        balance -= amount
        print(f"₹{amount} withdrawn successfully.")
    else:
        print("Invalid or insufficient amount.")
    return balance

# Main Program
print("Welcome to the ATM!")

# Simulate card insertion
if insert_card():
    if check_pin():
        print("PIN verified successfully.")

        while True:
            show_menu()
            choice = input("Choose an option (1-4): ")

            if choice == "1":
                balance = check_balance(balance)
            elif choice == "2":
                balance = deposit(balance)
            elif choice == "3":
                balance = withdraw(balance)
            elif choice == "4":
                print("Thank you for using the ATM. Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")
    else:
        print("Incorrect PIN. Access denied.")
else:
    print("ATM access denied. No card detected.")


