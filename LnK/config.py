import os
import sys
if getattr(sys, "frozen", False):
    # Running as a PyInstaller executable
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running as a normal Python script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENCRYPTED_DIR = os.path.join(BASE_DIR, "encrypted_files")
DECRYPTED_DIR = os.path.join(BASE_DIR, "decrypted_files")
REGISTRY_FILE = os.path.join(ENCRYPTED_DIR, "registry.json")
