import os
password = input("Enter the password: ")
password = password.encode()
salt = os.urandom(16)
print(salt)
print(password)