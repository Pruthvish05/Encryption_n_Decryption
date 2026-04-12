import base64
import json
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
passwordlist = ["password", "123456", "123456789", 
            "12345678", "12345", "qwerty", "abc123", 
            "football", "monkey", "letmein"]
salt_here = "salt_from_registry_json"
#this is just the file which can be created to decrypt a file without the owner 
#knowing the password but having the encrypted file and the salt
#and also the password
salt = bytes.fromhex(salt_here)  
for password in passwordlist:
    password_bytes = password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200000,
    )
    key = kdf.derive(password_bytes)
    fernet_key = base64.urlsafe_b64encode(key)
    fernet = Fernet(fernet_key)
    try:
        decrypted_data = fernet.decrypt(b"encrypted_data_here")
        print(f"Password found: {password}")
        break
    except Exception as e:
        continue







