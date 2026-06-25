import argparse
import sys
from file_utils import ensure_directories
from LnK.crypto_utils import encryption
from LnK.crypto_utils import decryption


def main():
    parser = argparse.ArgumentParser(
        prog="lnk",
        description="LockNKey secure file encryption and decryption tool",
    )
    parser.add_argument("mode", choices=["encrypt", "decrypt"])
    parser.add_argument("file", nargs="?")
    args = parser.parse_args()
    ensure_directories()
    if args.file is None:
        print("Please provide a file path.")
        sys.exit(1)
    if args.mode == "encrypt":
        encryption(args.file)
    elif args.mode == "decrypt":
        decryption(args.file)


if __name__ == "__main__":
    main()
