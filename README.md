# CLI Password Manager

A secure command-line password manager built in Python that allows you to store and retrieve passwords with encryption.

## Features

- 🔐 Secure password storage using Fernet encryption
- 🎲 Strong password generation
- 👤 Master password protection
- 📝 Store usernames/emails along with passwords
- 💾 Local storage in JSON format
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

2. Set your master password when prompted. This password will be required to access your stored passwords.

3. Choose from the following options:
   - **Option 1**: Add new password
   - **Option 2**: Retrieve password
   - **Option 3**: Exit

### Adding a New Password

1. Select Option 1
2. Enter the site name (e.g., "github", "gmail")
3. Enter your username or email
4. Either:
   - Enter your own password, or
   - Press Enter to generate a strong password

### Retrieving a Password

1. Select Option 2
2. Enter the site name
3. The program will display the stored username and password

## Security Features

- **Encryption**: Uses Fernet (symmetric encryption) from the cryptography package
- **Master Password**: All operations require master password authentication
- **Local Storage**: Passwords are stored locally in an encrypted format
- **Strong Password Generation**: Includes uppercase, lowercase, numbers, and special characters

## File Structure

- `cli_password.py`: Main program file
- `database.json`: Encrypted password storage (created on first use)

## Technical Details

- **Encryption Method**: Fernet symmetric encryption
- **Key Generation**: Master password is used to generate a secure encryption key
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
3. Regularly backup your `database.json` file
4. Don't share your master password with anyone
5. Consider using generated passwords for maximum security

## Limitations

- No built-in backup functionality
- Master password cannot be changed without recreating the database
- No password strength checker for user-provided passwords

## Future Improvements

Potential features that could be added:
- Password strength checking
- List all stored sites
- Delete passwords
- Update existing passwords
- Export/Import functionality
- Master password change option
- Password categories/tags

## Contributing

Feel free to fork this project and submit pull requests for any improvements.

## License

This project is open source and available under the MIT License.

## Security Notice

This password manager is a basic implementation and while it uses secure encryption, it's recommended to:
- Keep your master password secure
- Regularly update your passwords
- Use unique passwords for each site
- Consider using established password managers for critical accounts

## Support

For issues, questions, or contributions, please open an issue in the repository. 