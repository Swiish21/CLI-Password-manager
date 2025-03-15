#Below we are importing dependencies required for the program to run, they cover various aspects that our program requires
import json
import os
import base64
import getpass
import hashlib
from cryptography.fernet import Fernet
import secrets
import string


#file to store passwords(encrypted)
DB_FILE = 'database.json'

#Generate a key from a master password
def generate_key(master_password):
    key = hashlib.sha256(master_password.encode()).digest()
    return base64.urlsafe_b64encode(key)

#Encrypt a password
def encrypt_password(password, key):
    cipher = Fernet(key)
    return cipher.encrypt(password.encode()).decode()


#Decrypt a password
def decrypt_password(encrypted_password, key):
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_password.encode()).decode()

#load password database
def load_passwords():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, 'r') as file:
            content = file.read()
            if not content:  # If file is empty
                return {}
            return json.loads(content)
    except json.JSONDecodeError:
        return {}
    
#save password database
def save_passwords(passwords):
    with open(DB_FILE, 'w') as file:
        json.dump(passwords, file, indent=4)

#generate a strong password
def generate_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))
    
#add a new password
def add_password(master_key):
    site = input('Enter the site name:')
    username = input("Enter username/email: ")
    password = input("Enter password(or press Enter to generate a strong one): ")
    
    if not password:
        password = generate_password()
        print(f"Generated password:{password}")
            
    encrypted_password = encrypt_password(password, master_key)
    passwords = load_passwords()
    passwords[site] = {"username": username, "password": encrypted_password}
    save_passwords(passwords)
    print("Password saved successfully!")
    
#Retrieve a password
def get_password(master_key):
    site = input("Enter site/app name: ")
    passwords = load_passwords()
    
    if site in passwords:
        encrypted_password = passwords[site]["password"]
        decrypted_password = decrypt_password(encrypted_password, master_key)
        print(f"Username: {passwords[site]['username']}")
        print(f"password: {decrypted_password}")
    else:
        print("No password found for this site")
        
#main funtion
def main():
    print("Welcome to Password Manager!")
    master_password = input("Set your master password: ")  # Changed from getpass to input for testing
    master_key = generate_key(master_password)
    
    while True:
        print("\nPassword Manager CLI")
        print("1. Add new password")
        print("2. Retrieve Password")
        print("3. Exit")
        
        choice = input("Choose an option: ")
        if choice == "1":
            add_password(master_key)
        elif choice == "2":
            get_password(master_key)
        elif choice == "3":
            print("Exiting.....")
            break
        else:
            print("Invalid option, try again!")
            
if __name__ == "__main__":
    main()         
