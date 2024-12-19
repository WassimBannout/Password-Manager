# Secure Password Vault

A simple python based password manager that encrypts and securely stores passwords for different services using the `cryptography` library. 

## Features
- Generate and store encryption keys securely.
- Create a password vault to store encrypted passwords.
- Add, retrieve, update, and list stored passwords.
- Supports loading existing encryption keys and password vaults.

## How It Works
The password vault encrypts all stored passwords using the `Fernet` encryption provided by the `cryptography` library. The encrypted passwords are saved to a file, and only the corresponding encryption key can decrypt them.

Install the `cryptography` library if not already installed:
```
pip install cryptography
```
1. Clone this repository:
   ```
   git clone https://github.com/WassimBannout/Password-Manager.git
   ```
2. Navigate into the project directory:
   ```
   cd Password-Manager
   ```
3. Run the game
   ```
   python3 main.py

   ```
