import os


#just a simple CLI menu
def encryption():
    print("Encryption selected")
    file_path = input("Enter the file path to encrypt: ")
    if not os.path.isfile(file_path):
        print("File does not exist. Please try again.")
        return
    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as file:
        data = file.read()
    print(f"file loaded successfully")
    print(f"File-name: {file_name}")
    print(f"File-size: {len(data)} bytes")
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