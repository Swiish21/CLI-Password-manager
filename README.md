# CLI Password Manager

A secure command-line password manager built in Python that allows you to store, retrieve, update, and manage passwords with strong encryption and advanced security features.

## Features

- 🔐 Secure password storage using Fernet encryption
- 🎲 Strong password generation
- 👤 Master password protection with strength checking
- 📝 Store and manage usernames/emails along with passwords
- 💪 Password strength assessment and feedback
- 🔄 Update existing passwords and usernames
- 🗑️ Delete stored passwords
- 📋 List all stored sites and usernames
- 💾 Automated backup and restore functionality
- 🔍 Easy password retrieval

## Requirements

- Python 3.x
- Required packages:
  ```
  cryptography
  ```

## Installation

1. Clone the repository or download the source code:
   ```bash
   git clone <your-repository-url>
   cd cli-password-manager
   ```

2. Install the required package:
   ```bash
   python -m pip install cryptography
   ```

## Usage

1. Run the program:
   ```bash
   python cli_password.py
   ```

2. Set your master password when prompted
   - The program will check password strength and provide feedback
   - Warns if the master password is weak or moderate
   - Option to continue or choose a stronger password

3. Choose from the following options:
   - **Option 1**: Add new password
   - **Option 2**: Retrieve password
   - **Option 3**: List all sites
   - **Option 4**: Update password
   - **Option 5**: Delete password
   - **Option 6**: Backup database
   - **Option 7**: Restore database
   - **Option 8**: Exit

### Adding a New Password

1. Select Option 1
2. Enter the site name (e.g., "github", "gmail")
3. Enter your username or email
4. Either:
   - Enter your own password, or
   - Press Enter to generate a strong password
5. Review password strength assessment and feedback
6. Confirm if you want to proceed with a weak/moderate password

### Managing Passwords

#### Retrieving a Password
- Enter the site name to view stored username and password

#### Updating a Password
1. Enter the site name
2. Option to update username or keep current
3. Choose to:
   - Enter a new password manually
   - Generate a new strong password
   - Keep the current password
4. Review password strength if entering manually

#### Deleting a Password
- Enter site name and confirm deletion

#### Listing All Sites
- View a formatted table of all stored sites and usernames
- Alphabetically sorted for easy reference

### Backup and Restore

#### Creating a Backup
- Creates timestamped backup files
- Automatic error handling

#### Restoring from Backup
1. View list of available backups
2. Select backup to restore
3. Automatic backup of current database before restore
4. Confirmation of successful restore

## Security Features

- **Strong Encryption**: Uses Fernet (symmetric encryption) from the cryptography package
- **Password Strength Checking**:
  - Length requirements (minimum 8 characters)
  - Complexity requirements (uppercase, lowercase, numbers, special characters)
  - Detailed feedback and improvement suggestions
- **Master Password Protection**: All operations require master password authentication
- **Local Storage**: Passwords stored locally in encrypted format
- **Backup Protection**: All backups maintain encryption

## File Structure

- `cli_password.py`: Main program file
- `database.json`: Encrypted password storage (created on first use)
- `database_backup_[timestamp].json`: Backup files
- `database_current_[timestamp].json`: Auto-backup before restore

## Technical Details

- **Encryption Method**: Fernet symmetric encryption
- **Key Generation**: Master password is used to generate a secure encryption key
- **Password Strength Scoring**:
  - Score based on length and complexity
  - Additional points for longer passwords
  - Checks for character variety
- **Storage Format**: JSON with the following structure:
  ```json
  {
    "site_name": {
      "username": "user@example.com",
      "password": "encrypted_password_string"
    }
  }
  ```

## Best Practices

1. Choose a strong master password
2. Keep your master password secure - it cannot be recovered if lost
3. Regularly backup your password database
4. Use generated passwords for maximum security
5. Review password strength feedback
6. Create regular backups using the built-in backup feature

## Security Notice

This password manager is a basic implementation and while it uses secure encryption, it's recommended to:
- Keep your master password secure
- Regularly update your passwords
- Use unique passwords for each site
- Consider using established password managers for critical accounts
- Store backup files securely

## Support

For issues, questions, or contributions, please open an issue in the repository.

## License

This project is open source and available under the MIT License. 