#just a simple CLI menu
def encryption():
    print("Encryption selected")
    # Here we would add our encryption code
def decryption():
    print("Decryption selected")
    # Here we would add our decryption code
def menu():
    print("Welcome to the Encryption/Decryption Tool")
    print("1. Encrypt a message")
    print("2. Decrypt a message")
    print("3. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        encryption()
    elif choice == "2":
        decryption()
    elif choice == "3":
        print("Exiting...")
    else:
        print("Invalid choice. Please try again.")
menu()