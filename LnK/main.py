import argparse
from email import parser
import sys
from file_utils import ensure_directories
from crypto_utils import encryption
from crypto_utils import decryption
VERSION = "1.0.0"
def main():
    parser = argparse.ArgumentParser(
        prog="lnk",
        description="LockNKey secure file encryption and decryption tool",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"%LNK v{VERSION}"
    )
    parser.add_argument("mode", choices=["encrypt", "decrypt"])
    parser.add_argument("file", nargs="?")
    args = parser.parse_args()
    ensure_directories()
    if args.file is None:
        print("Please provide a file path.")
        sys.exit(1)
    try:
        if args.mode == "encrypt":
            encryption(args.file)
        elif args.mode == "decrypt":
            decryption(args.file)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
if __name__ == "__main__":
    main()
