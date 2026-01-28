# 🔐 CryptoVault - Professional File Encryption Tool

A powerful, secure, and user-friendly command-line file encryption/decryption tool for Debian/Ubuntu Linux systems. Built with AES-256 encryption and designed for cybersecurity professionals, privacy enthusiasts, and anyone who needs to protect sensitive data.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6+-green.svg)
![Platform](https://img.shields.io/badge/platform-linux-lightgrey.svg)

## ✨ Features

- 🔒 **Military-Grade Encryption**: AES-256 encryption with PBKDF2 key derivation
- 📁 **Batch Processing**: Encrypt/decrypt entire directories
- 🔑 **Secure Password Generation**: Built-in cryptographically secure password generator
- 🗑️ **Secure File Deletion**: Shred files with multiple overwrite passes
- 📊 **File Metadata**: Stores original filename, timestamp, and checksum
- ✅ **Integrity Verification**: SHA-256 checksum validation
- 🎨 **Beautiful CLI**: Color-coded output for better user experience
- ⚡ **Fast Performance**: Optimized for large files
- 🛡️ **Error Handling**: Robust error detection and recovery

## 🚀 Quick Installation

### One-Line Install

```bash
curl -sSL https://raw.githubusercontent.com/Medbelkacem/cryptovault/main/install.sh | sudo bash
```

### Manual Installation

```bash
# Install dependencies
pip3 install cryptography

# Make executable
chmod +x cryptovault.py

# Install system-wide
sudo cp cryptovault.py /usr/local/bin/cryptovault
```

## 📖 Usage Examples

```bash
# Encrypt a file
cryptovault -e secret.txt -o secret.txt.encrypted

# Decrypt a file
cryptovault -d secret.txt.encrypted -o secret.txt

# Encrypt entire directory
cryptovault -e /path/to/docs -o /path/to/encrypted --directory

# Generate secure password
cryptovault --generate-password

# Shred (securely delete) a file
cryptovault --shred sensitive.txt

# View encrypted file info
cryptovault --info file.encrypted
```

## 🔒 Security

- **Algorithm**: AES-256 (Fernet)
- **Key Derivation**: PBKDF2 with 100,000 iterations
- **Integrity**: SHA-256 checksum verification
- **Secure Deletion**: DoD 5220.22-M compatible shredding

## 📝 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

**Medbelkacem** - [@Medbelkacem](https://github.com/Medbelkacem)

---

**Made with ❤️ for privacy and security** 🔐
