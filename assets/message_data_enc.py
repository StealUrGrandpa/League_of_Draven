import json
import os
from cryptography.fernet import Fernet

# Generate and save a key (Run this once and store the key safely)
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Load the encryption key
def load_key():
    secret = os.getenv('secret_key')  # Ensure the variable name matches
    if secret is None:
        raise ValueError("Environment variable SECRET_KEY is not set.")
    return secret.encode()  # Convert to bytes

def decrypt_json(secret_key):

    fernet = Fernet(secret_key)
    base_dir = os.path.dirname(__file__)  # Get the directory of this script
    filename = os.path.join(base_dir, "data.json.enc")
    with open(filename, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = fernet.decrypt(encrypted_data)
    return json.loads(decrypted_data.decode())

# Example Dictionary
def encrypt_json(data, secret_key):
    fernet = Fernet(secret_key)
    filename = os.path.join(os.path.dirname(__file__), "data.json.enc")

    # Decrypt existing data if the file exists
    if os.path.exists(filename):
        with open(filename, "rb") as file:
            decrypted_data = json.loads(fernet.decrypt(file.read()).decode())
    else:
        decrypted_data = {}

    # Merge new data
    for key, value in data.items():
        decrypted_data.setdefault(key, {}).update(value)

    # Encrypt and save
    with open(filename, "wb") as file:
        file.write(fernet.encrypt(json.dumps(decrypted_data).encode()))

def delete_value(user_id, message_id, secret_key):
    fernet = Fernet(secret_key)
    filename = os.path.join(os.path.dirname(__file__), "data.json.enc")

    if os.path.exists(filename):
        with open(filename, "rb") as file:
            encrypted_data = file.read()

        decrypted_data = json.loads(fernet.decrypt(encrypted_data).decode())

        # Check if user_id exists
        if user_id in decrypted_data:
            # Check if message_id exists inside user_id
            if message_id in decrypted_data[user_id]:
                del decrypted_data[user_id][message_id]
                print(f"Message ID '{message_id}' deleted successfully from user '{user_id}'.")

                # Remove user_id if it's empty after deletion
                if not decrypted_data[user_id]:
                    del decrypted_data[user_id]
                    print(f"User '{user_id}' removed due to no remaining messages.")
            else:
                print(f"Message ID '{message_id}' not found for user '{user_id}'.")
        else:
            print(f"User ID '{user_id}' not found.")

        # Re-encrypt and save the updated data
        with open(filename, "wb") as file:
            file.write(fernet.encrypt(json.dumps(decrypted_data).encode()))
    else:
        print(f"File '{filename}' does not exist.")

