import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64
import json
#just a simple CLI menu
#not simple anymore lol
#need to add error handling and edge cases
#need to add creating a folder for this and registry .json file
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
    password = input("Enter a password for encryption: ")
    password_bytes = password.encode()
    salt= os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(password_bytes)
    print(f"Encryption key derived successfully")
    # Here we would add our encryption code
    print("salt", salt.hex())
    print("key", key.hex())
    fernet_key = base64.urlsafe_b64encode(key)
    fernet = Fernet(fernet_key)
    encrypted_data = fernet.encrypt(data)
    os.makedirs("encrypted_files", exist_ok=True)
    encrypted_file_path = os.path.join("encrypted_files", file_name + ".enc")
    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)
    print(f"File encrypted successfully and saved to {encrypted_file_path}")
    # if not os.path.isfile("registry.json"):
    #     with open("registry.json", 'w') as registry_file:
    #         json.dump({}, registry_file)
    # with open("registry.json", 'r') as registry_file:
    #     registry = json.load(registry_file)
    # registry[file_name] = {
    #     "path": encrypted_file_path,
    #     "salt": salt.hex(),
    #     "key": key.hex()
    # }
    # with open("registry.json", 'w') as registry_file:
    #     json.dump(registry, registry_file)
    if os.path.exists("registry.json"):
        with open("registry.json", 'r') as registry_file:
            registry = json.load(registry_file)
    else:
        registry = {}
    registry[file_name + '.enc'] = {
        "path": encrypted_file_path,
        "salt": salt.hex(),
        "key": key.hex()
    }
    with open("registry.json", 'w') as registry_file:
        json.dump(registry, registry_file)

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