import os

from config import ENCRYPTED_DIR, DECRYPTED_DIR, REGISTRY_FILE


def ensure_directories():
    os.makedirs(ENCRYPTED_DIR, exist_ok=True)
    os.makedirs(DECRYPTED_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(REGISTRY_FILE), exist_ok=True)
