#Below we are importing modules required for the program to run, they cover various aspects that our program requires
import json
import os
import base64
import getpass
import hashlib
from cryptography.fernet import Fernet
import secrets
import string
import re  # Add this to imports at the top
from datetime import datetime
import shutil


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
    
def check_password_strength(password):
    """Check the strength of a password and return feedback."""
    score = 0
    feedback = []
    
    # Length check
    if len(password) < 8:
        feedback.append("Password is too short (minimum 8 characters)")
    elif len(password) >= 12:
        score += 2
    else:
        score += 1
    
    # Complexity checks
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add numbers")
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters")
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters")
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Add special characters")
    
    # Return strength assessment
    if score < 2:
        return "Weak", feedback
    elif score < 3:
        return "Moderate", feedback
    elif score < 4:
        return "Strong", feedback
    else:
        return "Very Strong", feedback

def list_all_sites():
    """List all stored sites and their usernames."""
    passwords = load_passwords()
    if not passwords:
        print("No passwords stored yet.")
        return
    
    print("\nStored Sites:")
    print("-" * 40)
    print(f"{'Site':<20} {'Username':<20}")
    print("-" * 40)
    for site, data in sorted(passwords.items()):
        print(f"{site:<20} {data['username']:<20}")
    print("-" * 40)

#add a new password
def add_password(master_key):
    site = input('Enter the site name: ')
    username = input("Enter username/email: ")
    password = input("Enter password (or press Enter to generate a strong one): ")
    
    if not password:
        password = generate_password()
        print(f"\nGenerated password: {password}")
    
    # Check password strength
    strength, feedback = check_password_strength(password)
    print(f"\nPassword Strength: {strength}")
    if feedback:
        print("Suggestions to improve:")
        for suggestion in feedback:
            print(f"- {suggestion}")
        
        if strength in ["Weak", "Moderate"]:
            confirm = input("\nDo you want to continue with this password anyway? (y/n): ")
            if confirm.lower() != 'y':
                return
    
    encrypted_password = encrypt_password(password, master_key)
    passwords = load_passwords()
    passwords[site] = {"username": username, "password": encrypted_password}
    save_passwords(passwords)
    print("\nPassword saved successfully!")
    
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
        
def delete_password(master_key):
    """Delete a stored password."""
    site = input("Enter site name to delete: ")
    passwords = load_passwords()
    
    if site in passwords:
        confirm = input(f"Are you sure you want to delete password for {site}? (y/n): ")
        if confirm.lower() == 'y':
            del passwords[site]
            save_passwords(passwords)
            print(f"\nPassword for {site} deleted successfully!")
        else:
            print("\nDeletion cancelled.")
    else:
        print("\nNo password found for this site.")

def update_password(master_key):
    """Update an existing password."""
    site = input("Enter site name to update: ")
    passwords = load_passwords()
    
    if site in passwords:
        print(f"\nCurrent username: {passwords[site]['username']}")
        update_username = input("Enter new username/email (or press Enter to keep current): ")
        if update_username:
            passwords[site]['username'] = update_username
        
        update_choice = input("\nDo you want to:\n1. Enter a new password\n2. Generate a new password\n3. Keep current password\nChoice: ")
        
        if update_choice == '1':
            new_password = input("Enter new password: ")
            strength, feedback = check_password_strength(new_password)
            print(f"\nPassword Strength: {strength}")
            if feedback:
                print("Suggestions to improve:")
                for suggestion in feedback:
                    print(f"- {suggestion}")
                if strength in ["Weak", "Moderate"]:
                    confirm = input("\nDo you want to continue with this password anyway? (y/n): ")
                    if confirm.lower() != 'y':
                        return
            passwords[site]['password'] = encrypt_password(new_password, master_key)
            
        elif update_choice == '2':
            new_password = generate_password()
            print(f"\nGenerated password: {new_password}")
            passwords[site]['password'] = encrypt_password(new_password, master_key)
        
        save_passwords(passwords)
        print("\nPassword updated successfully!")
    else:
        print("\nNo password found for this site.")

def backup_database():
    """Create a backup of the password database."""
    if not os.path.exists(DB_FILE):
        print("\nNo database file exists yet.")
        return
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"database_backup_{timestamp}.json"
    
    try:
        shutil.copy2(DB_FILE, backup_file)
        print(f"\nBackup created successfully: {backup_file}")
    except Exception as e:
        print(f"\nError creating backup: {str(e)}")

def restore_database():
    """Restore the password database from a backup."""
    # List all backup files
    backup_files = [f for f in os.listdir('.') if f.startswith('database_backup_') and f.endswith('.json')]
    
    if not backup_files:
        print("\nNo backup files found.")
        return
        
    print("\nAvailable backups:")
    for i, file in enumerate(sorted(backup_files, reverse=True), 1):
        print(f"{i}. {file}")
    
    try:
        choice = int(input("\nEnter the number of the backup to restore (0 to cancel): "))
        if choice == 0:
            return
        if 1 <= choice <= len(backup_files):
            backup_file = sorted(backup_files, reverse=True)[choice-1]
            
            # Create a backup of current database if it exists
            if os.path.exists(DB_FILE):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                current_backup = f"database_current_{timestamp}.json"
                shutil.copy2(DB_FILE, current_backup)
                print(f"\nCurrent database backed up as: {current_backup}")
            
            # Restore the selected backup
            shutil.copy2(backup_file, DB_FILE)
            print(f"\nDatabase restored from: {backup_file}")
        else:
            print("\nInvalid choice.")
    except ValueError:
        print("\nInvalid input. Please enter a number.")
    except Exception as e:
        print(f"\nError restoring backup: {str(e)}")

#main funtion
def main():
    print("Welcome to Password Manager!")
    print("=" * 50)
    master_password = input("Set your master password: ")
    
    # Check master password strength
    strength, feedback = check_password_strength(master_password)
    if strength in ["Weak", "Moderate"]:
        print(f"\nWarning: Your master password is {strength}")
        print("Suggestions to improve:")
        for suggestion in feedback:
            print(f"- {suggestion}")
        confirm = input("\nDo you want to continue with this master password? (y/n): ")
        if confirm.lower() != 'y':
            return
    
    master_key = generate_key(master_password)
    
    while True:
        print("\nPassword Manager CLI")
        print("=" * 50)
        print("1. Add new password")
        print("2. Retrieve Password")
        print("3. List all sites")
        print("4. Update password")
        print("5. Delete password")
        print("6. Backup database")
        print("7. Restore database")
        print("8. Exit")
        print("=" * 50)
        
        choice = input("Choose an option: ")
        if choice == "1":
            add_password(master_key)
        elif choice == "2":
            get_password(master_key)
        elif choice == "3":
            list_all_sites()
        elif choice == "4":
            update_password(master_key)
        elif choice == "5":
            delete_password(master_key)
        elif choice == "6":
            backup_database()
        elif choice == "7":
            restore_database()
        elif choice == "8":
            print("Exiting.....")
            break
        else:
            print("Invalid option, try again!")
            
if __name__ == "__main__":
    main()         
