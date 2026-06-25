# 🔐 LNK (LockNKey)

LNK is a standalone command-line file encryption utility built in Python. It securely encrypts and decrypts files using password-based encryption without ever storing encryption keys.

The project is designed as a lightweight, production-oriented encryption tool that can be packaged into a standalone executable and used without requiring Python to be installed.

---

# Features

- Password-based file encryption
- Password-based file decryption
- PBKDF2-HMAC-SHA256 key derivation
- 500,000 PBKDF2 iterations
- Fernet symmetric encryption
- Random 16-byte salt for every encrypted file
- Secure password input using `getpass`
- Password strength validation
- Original file restoration
- Duplicate filename handling
- Registry-based encrypted file management
- Standalone executable using PyInstaller
- Cross-file support (Text, PDF, Images, etc.)

---

# Security

LNK follows several security best practices.

- Encryption keys are never stored.
- A new random salt is generated for every encrypted file.
- Passwords are never written to disk.
- Fernet provides authenticated encryption and integrity verification.
- Incorrect passwords automatically fail decryption.

---

# Installation

Clone the repository

```bash
git clone <repository-url>
cd LNK
```

Install dependencies

```bash
pip install -r requirements.txt
```

Build the executable

```bash
pyinstaller --onefile --name lnk main.py
```

(Optional)

Add the generated `lnk.exe` directory to your system PATH to use it globally.

---

# Usage

Encrypt a file

```bash
lnk encrypt example.txt
```

Decrypt a file

```bash
lnk decrypt example.txt
```

Display version

```bash
lnk --version
```

---

# Project Structure

```text
LNK/
│
├── main.py
├── config.py
├── crypto_utils.py
├── registry_utils.py
├── password_utils.py
├── file_utils.py
├── encrypted_files/
├── decrypted_files/
└── README.md
```

---

# Technologies Used

- Python
- cryptography
- PBKDF2-HMAC
- SHA-256
- Fernet
- argparse
- PyInstaller

---

# Current Limitations

- Uses a registry file for encrypted file metadata.
- Registry must remain available for successful decryption.
- Compression is not yet implemented.
- Chunked encryption is not yet supported.

---

# Roadmap

## Version 2

- Self-contained encrypted file format
- Embedded metadata
- Magic header (`LNK1`)
- Registry-free architecture
- Compression support
- Chunked encryption
- Secure file deletion
- AES-GCM evaluation
- Logging system

---

# License

This project is licensed under the MIT License.

---

# Author

Developed by Pruthvish.
