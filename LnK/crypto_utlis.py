import base64
import getpass
import uuid
import os
import sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from password_utils import validate_password
from registry_utils import load_registry
from registry_utils import save_registry
from config import ENCRYPTED_DIR, DECRYPTED_DIR, REGISTRY_FILE
from file_utils import ensure_directories

def derive_key(password, salt):
    password_bytes = password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=500000,
    )
    key = kdf.derive(password_bytes)
    return base64.urlsafe_b64encode(key)

ensure_directories()

def encryption(file_path):
    # file_path = input("Enter the file path to encrypt: ")
    if not os.path.isfile(file_path):
        print("File does not exist. Please try again.")
        sys.exit(1)
    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as file:
        data = file.read()
    print(f"file loaded successfully")
    print(f"File-name: {file_name}")
    print(f"File-size: {len(data)} bytes")
    while True:
        password = getpass.getpass("Enter a strong password for encryption: ")
        confirm = getpass.getpass("Confirm password: ")
        if not validate_password(password):
            continue
        if confirm != password:
            print("Passwords do not match. Please try again.")
            continue
        break
    # time.sleep(1)
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
    fernet_key = derive_key(password, salt)
    fernet = Fernet(fernet_key)
    encrypted_data = fernet.encrypt(data)
    encrypted_name = f"{file_name}_{uuid.uuid4().hex[:8]}.enc"
    encrypted_file_path = os.path.join(ENCRYPTED_DIR, encrypted_name)
    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)
    registry = load_registry()
    registry[os.path.basename(encrypted_file_path)] = {
        "original_name": file_name,
        "path": os.path.basename(encrypted_file_path),
        "salt": salt.hex(),
    }
    save_registry(registry)
    print(f"Encrypted -> {encrypted_file_path}")
    delete_original = input("Do you want to delete the original file? (yes/no): ").lower()
    if delete_original == "yes":
        os.remove(file_path)
        print("Original file deleted.")

def decryption(file_path=None):
    print("Decryption selected")
    # Here we would add our decryption code
    #now we will
    if file_path is None:
        print("Please provide a file path for decryption.")
        return
    if not os.path.isfile(REGISTRY_FILE):
        print("No encrypted files found. Please encrypt a file first.")
        return
    registry = load_registry()
    # print("Available encrypted files:")
    selected_file = os.path.basename(file_path)
    if selected_file not in registry:
        print("File not found in registry. Please try again.")
        return
    # try:
    #     choice = int(input("Enter the number of the file you want to decrypt: "))
    #     keys = list(registry.keys())
    #     if choice < 1 or choice > len(keys):
    #         print("Invalid choice. Please try again.")
    #         return
    # except ValueError:
    #     print("Invalid input. Please enter a number.")
    #     return
    #selected_file = keys[choice - 1]
    file_info = registry[selected_file]
    encrypted_file_path = file_info["path"]
    salt = bytes.fromhex(file_info["salt"])
    original_name = file_info["original_name"]
    password = getpass.getpass("Enter the password for decryption: ")
    if not password:
        print("Password cannot be empty. Decryption cancelled.")
        return
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=500000,
    )
    key = kdf.derive(password.encode())
    fernet_key = derive_key(password, salt)
    fernet = Fernet(fernet_key)
    try:
        with open(encrypted_file_path, 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = fernet.decrypt(encrypted_data)
    except InvalidToken:
        print("Invalid password. Decryption failed.")
        return
    except OSError as e:
        print(f"Error reading encrypted file: {e}")
        return
    output_file_path = os.path.join(DECRYPTED_DIR, original_name)
    if os.path.exists(output_file_path):
        overwrite = input(f"{output_file_path} already exists. Do you want to overwrite it? (yes/no): ").lower()
        if overwrite != "yes":
            print("Decryption cancelled.")
            return
    os.makedirs(DECRYPTED_DIR, exist_ok=True)
    with open(output_file_path, 'wb') as output_file:
        output_file.write(decrypted_data)
    print(f"Decrypted -> {output_file_path}")