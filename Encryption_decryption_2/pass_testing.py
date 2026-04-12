import base64
import json
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
passwordlist = ["password", "123456", "123456789", 
            "12345678", "12345", "qwerty", "abc123", 
            "football", "monkey", "letmein"]
salt_here = "salt_from_registry_json"
salt = bytes.fromhex(salt_here)  




