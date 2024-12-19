from cryptography.fernet import Fernet

class SecurePasswordVault:
    def __init__(self):
        self.encryption_key = None
        self.password_file_path = None
        self.passwords = {}

    def generate_key(self, file_path):
        if input("This will overwrite any existing key at the path. Continue? (yes/no): ").lower() != "yes":
            print("Key generation canceled.")
            return
        self.encryption_key = Fernet.generate_key()
        with open(file_path, 'wb') as file:
            file.write(self.encryption_key)
        print(f"New encryption key saved to {file_path}")

    def load_key(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                self.encryption_key = file.read()
            print(f"Encryption key loaded from {file_path}")
        except FileNotFoundError:
            print("Error: Key file not found. Please check the path and try again.")

    def create_password_vault(self, file_path, initial_values=None):
        if input("This will overwrite any existing password vault. Continue? (yes/no): ").lower() != "yes":
            print("Password vault creation canceled.")
            return
        self.password_file_path = file_path
        self.passwords = {}
        if initial_values:
            for service_name, password in initial_values.items():
                self.add_password(service_name, password)
        print(f"Password vault created at {file_path}")

    def load_password_vault(self, file_path):
        try:
            self.password_file_path = file_path
            with open(file_path, 'r') as file:
                for line in file:
                    service_name, encrypted_password = line.strip().split(":")
                    self.passwords[service_name] = Fernet(self.encryption_key).decrypt(encrypted_password.encode()).decode()
            print(f"Passwords loaded from {file_path}")
        except FileNotFoundError:
            print("Error: Password vault not found. Please check the path and try again.")
        except Exception as e:
            print(f"Error loading password vault: {e}")

    def add_password(self, service_name, password):
        if not self.encryption_key:
            print("Error: Encryption key not loaded. Please load the key first.")
            return
        if service_name in self.passwords:
            print(f"Error: A password for {service_name} already exists. Use 'update_password' to modify it.")
            return
        self.passwords[service_name] = password
        if self.password_file_path:
            encrypted_password = Fernet(self.encryption_key).encrypt(password.encode())
            with open(self.password_file_path, 'a') as file:
                file.write(f"{service_name}:{encrypted_password.decode()}\n")
        print(f"Password for {service_name} added successfully.")

    def update_password(self, service_name, new_password):
        if service_name not in self.passwords:
            print(f"Error: No password found for {service_name}. Use 'add_password' to create a new entry.")
            return
        self.passwords[service_name] = new_password
        if self.password_file_path:
            with open(self.password_file_path, 'w') as file:
                for svc_name, password in self.passwords.items():
                    encrypted_password = Fernet(self.encryption_key).encrypt(password.encode())
                    file.write(f"{svc_name}:{encrypted_password.decode()}\n")
        print(f"Password for {service_name} updated successfully.")

    def get_password(self, service_name):
        if not self.passwords:
            print("Error: Password vault is empty or not loaded. Please load a vault first.")
            return
        return self.passwords.get(service_name, "Error: Password not found for the specified service.")

    def list_services(self):
        if not self.passwords:
            print("No passwords stored in the vault.")
            return
        print("Stored services:")
        for service_name in self.passwords:
            print(f"- {service_name}")


def main():
    default_passwords = {
        "email": "123456",
        "facebook": "password",
        "youtube": "qwerty"
    }
    vault = SecurePasswordVault()

    menu = """
What would you like to do?
1. Generate a new encryption key
2. Load an existing encryption key
3. Create a new password vault
4. Load an existing password vault
5. Add a new password
6. Update an existing password
7. Get a password
8. List stored services
q. Quit
"""
    while True:
        print(menu)
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            file_path = input("Enter the file path to save the key: ").strip()
            vault.generate_key(file_path)
        elif choice == "2":
            file_path = input("Enter the file path to load the key: ").strip()
            vault.load_key(file_path)
        elif choice == "3":
            file_path = input("Enter the file path to create the vault: ").strip()
            vault.create_password_vault(file_path, default_passwords)
        elif choice == "4":
            file_path = input("Enter the file path to load the vault: ").strip()
            vault.load_password_vault(file_path)
        elif choice == "5":
            service_name = input("Enter the service name: ").strip()
            password = input("Enter the password: ").strip()
            vault.add_password(service_name, password)
        elif choice == "6":
            service_name = input("Enter the service name: ").strip()
            new_password = input("Enter the new password: ").strip()
            vault.update_password(service_name, new_password)
        elif choice == "7":
            vault.list_services()
            service_name = input("Enter the service name to retrieve the password: ").strip()
            print(f"Password for {service_name}: {vault.get_password(service_name)}")
        elif choice == "8":
            vault.list_services()
        elif choice.lower() == "q":
            print("Exiting Secure Password Vault. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
