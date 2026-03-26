from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
def file():
    file = input("Enter the address of the file is: ")
    with open(file, 'rb') as f:
        data = f.read()
    print(len(data))
    password = input("Enter the password: ")
    