import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64
import json
import getpass
import time
import re
import argparse
#just a simple CLI menu
#not simple anymore lol
#need to add error handling and edge cases
#need to add creating a folder for this and registry .json file
def encryption(file_path):
    # file_path = input("Enter the file path to encrypt: ")
    if not os.path.isfile(file_path):
        print("File does not exist. Please try again.")
        return
    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as file:
        data = file.read()
    print(f"file loaded successfully")
    print(f"File-name: {file_name}")
    print(f"File-size: {len(data)} bytes")
    def validate_password(password):
        if len(password) < 8:
            print("Password must be at least 8 characters long.")
            return False
        if not re.search(r"[A-Z]", password):
            print("Password must contain at least one uppercase letter.")
            return False
        if not re.search(r"[a-z]", password):
            print("Password must contain at least one lowercase letter.")
            return False
        if not re.search(r"\d", password):
            print("Password must contain at least one digit.")
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            print("Password must contain at least one special character.")
            return False
        return True
    while True:
        password = getpass.getpass("Enter a strong password for encryption: ")
        if validate_password(password):
            break
    time.sleep(1)
    password_bytes = password.encode()
    salt= os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=500000,
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
    if os.path.exists("registry.json"):
        with open("registry.json", 'r') as registry_file:
            registry = json.load(registry_file)
    else:
        registry = {}
    registry[os.path.basename(encrypted_file_path)] = {
        "original_name": file_name,
        "path": encrypted_file_path,
        "salt": salt.hex(),
    }
    with open("encrypted_files/registry.json", 'w') as registry_file:
        json.dump(registry, registry_file, indent=4)
    print(f"File encrypted successfully and saved to {encrypted_file_path}")
    delete_original = input("Do you want to delete the original file? (yes/no): ").lower()
    print("Encrypt Salt:", salt.hex())
    if delete_original == "yes":
        os.remove(file_path)
        print("Original file deleted.")
    # if not os.path.isfile("encrypted_files/registry.json"):
    #     with open("encrypted_files/registry.json", 'w') as registry_file:
    #         json.dump({}, registry_file)
    # with open("encrypted_files/registry.json", 'r') as registry_file:
    #     registry = json.load(registry_file)
    # registry[file_name] = {
    #     "path": encrypted_file_path,
    #     "salt": salt.hex(),
    #     "key": key.hex()
    # }
    # with open("encrypted_files/registry.json", 'w') as registry_file:
    #     json.dump(registry, registry_file)
def decryption(file_path=None):
    print("Decryption selected")
    # Here we would add our decryption code
    #now we will
    if not os.path.isfile("encrypted_files/registry.json"):
        print("No encrypted files found. Please encrypt a file first.")
        return
    with open("encrypted_files/registry.json", 'r') as registry_file:
        registry = json.load(registry_file)
    print("Available encrypted files:")
    for index, file_name in enumerate(registry.keys(), start=1):
        print(f"{index}. {file_name}")
    try:
        choice = int(input("Enter the number of the file you want to decrypt: "))
        keys = list(registry.keys())
        if choice < 1 or choice > len(keys):
            print("Invalid choice. Please try again.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return
    
    file_info = registry[selected_file]
    encrypted_file_path = file_info["path"]
    salt = bytes.fromhex(file_info["salt"])
    original_name = file_info["original_name"]
    password = getpass.getpass("Enter the password for decryption: ")
    password_bytes = password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=500000,
    )
    key = kdf.derive(password_bytes)
    fernet_key = base64.urlsafe_b64encode(key)
    fernet = Fernet(fernet_key)
    try:
        with open(encrypted_file_path, 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = fernet.decrypt(encrypted_data)
    except Exception as e:
        print("Decryption failed. Incorrect password or corrupted file.")
        return
    output_file_path = os.path.join("decrypted_files", original_name)
    if os.path.exists(output_file_path):
        overwrite = input(f"{output_file_path} already exists. Do you want to overwrite it? (yes/no): ").lower()
        if overwrite != "yes":
            print("Decryption cancelled.")
            return
    os.makedirs("decrypted_files", exist_ok=True)
    with open(output_file_path, 'wb') as output_file:
        output_file.write(decrypted_data)
    print(f"File decrypted successfully and saved to {output_file_path}")

def menu():
    while True:
        print("Welcome to the Encryption/Decryption Tool")
        print("1. Encrypt a file")
        print("2. Decrypt a file")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            encryption()
        elif choice == "2":
            decryption()
        elif choice == "3":
            print("Exiting...")
            time.sleep(2)
            os._exit(0)
        else:
            print("Invalid choice. Please try again.")
            time.sleep(1)
            os._exit(0)

def main():
    parser = argparse.ArgumentParser(description="A simple encryption/decryption tool")
    parser.add_argument("mode", choices=['encrypt', 'decrypt'], help='Mode of operation')
    parser.add_argument("file", help="Path to the file to encrypt/decrypt", nargs='?', default=None)
    args = parser.parse_args()
    if args.mode == 'encrypt':
        encryption(args.file)
    elif args.mode == 'decrypt':
        decryption(args.file)
    else:
        menu()
#nearly done close to deploying.