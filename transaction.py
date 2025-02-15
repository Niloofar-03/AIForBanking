# transaction.py

def simulate_transfer(amount, recipient):
    print(f"Transfer successful! ${amount} has been sent to {recipient}.")
    return True

def authenticate_user():
    correct_pin = "1234"  # Simple mock PIN
    pin = input("Please enter your PIN: ")

    if pin == correct_pin:
        print("PIN verified!")
        return True
    else:
        print("Incorrect PIN. Please try again.")
        return False

def secure_transfer():
    print("Voice command recognized. Please confirm your transaction.")
    
    if authenticate_user():
        amount = input("Enter the amount you wish to transfer: $")
        recipient = input("Enter the recipient's name: ")
        
        simulate_transfer(amount, recipient)
    else:
        print("Transfer aborted due to incorrect PIN.")
