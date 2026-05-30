import os 
import json
import sys
from config import REGISTRY_FILE
def load_registry():
    if not os.path.exists(REGISTRY_FILE):
        return {}
    try:
        with open(REGISTRY_FILE, 'r', encoding='utf-8') as registry_file:
            return json.load(registry_file)
    except json.JSONDecodeError:
        print("Registry file is corrupted.")
        sys.exit(1)

def save_registry(registry):
    temp_registry_file = REGISTRY_FILE + ".tmp"
    try:
        with open(temp_registry_file, 'w', encoding='utf-8') as registry_file:
            json.dump(registry, registry_file)
        os.replace(temp_registry_file, REGISTRY_FILE)
    except OSError as e:
        print(f"Failed to save registry: {e}")
        if os.path.exists(temp_registry_file):
            os.remove(temp_registry_file)
        sys.exit(1)
