import os

REGISTRY_FILE = "encrypted_files/registry.json"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENCRYPTED_DIR = os.path.join(BASE_DIR, "encrypted_files")
DECRYPTED_DIR = os.path.join(BASE_DIR, "decrypted_files")
REGISTRY_FILE = os.path.join(ENCRYPTED_DIR, "registry.json")
