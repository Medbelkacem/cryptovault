# CryptoVault - Usage Examples

## 📚 Table of Contents

1. [Basic Operations](#basic-operations)
2. [Advanced Usage](#advanced-usage)
3. [Real-World Scenarios](#real-world-scenarios)
4. [Security Best Practices](#security-best-practices)

---

## Basic Operations

### 1. Encrypt a Single File

```bash
# Basic encryption (will prompt for password)
cryptovault -e document.pdf -o document.pdf.encrypted

# With password in command (less secure, visible in history)
cryptovault -e document.pdf -o document.pdf.encrypted -p "MyPassword123"

# Encrypt and delete original
cryptovault -e document.pdf -o document.pdf.encrypted --delete-original
```

### 2. Decrypt a File

```bash
# Basic decryption
cryptovault -d document.pdf.encrypted -o document.pdf

# Decrypt and remove encrypted file
cryptovault -d document.pdf.encrypted -o document.pdf --delete-original
```

### 3. Generate Secure Passwords

```bash
# Generate 32-character password (default)
cryptovault --generate-password

# Generate 64-character password
cryptovault --generate-password --password-length 64

# Generate and save to file
cryptovault --generate-password > mypassword.txt
```

---

## Advanced Usage

### 4. Encrypt Entire Directories

```bash
# Encrypt all files in a directory
cryptovault -e ~/Documents/private -o ~/Documents/encrypted --directory

# Decrypt entire directory
cryptovault -d ~/Documents/encrypted -o ~/Documents/decrypted --directory

# Encrypt and remove originals (DANGEROUS!)
cryptovault -e ~/Documents/private -o ~/Documents/encrypted --directory --delete-original
```

### 5. View Encrypted File Information

```bash
# Show metadata of encrypted file
cryptovault --info myfile.encrypted

# Output example:
# Original Filename: secret_document.pdf
# Encrypted On: 2026-01-29T10:30:45.123456
# Original Size: 2.45 MB
# Checksum: a1b2c3d4e5f6...
```

### 6. Secure File Deletion (Shredding)

```bash
# Shred with 3 passes (default)
cryptovault --shred sensitive.txt

# Shred with 7 passes (more secure)
cryptovault --shred sensitive.txt --shred-passes 7

# Shred with 35 passes (DoD standard)
cryptovault --shred classified.pdf --shred-passes 35
```

---

## Real-World Scenarios

### Scenario 1: Secure Cloud Backup

```bash
#!/bin/bash
# Backup script with encryption

# Create backup
tar -czf backup-$(date +%Y%m%d).tar.gz ~/important_files/

# Generate password
PASSWORD=$(cryptovault --generate-password --no-banner)

# Encrypt backup
cryptovault -e backup-*.tar.gz -o backup-encrypted.tar.gz -p "$PASSWORD"

# Save password securely (using GPG)
echo "$PASSWORD" | gpg --encrypt -r your@email.com > backup-password.gpg

# Delete unencrypted backup
rm backup-*.tar.gz

# Upload to cloud
rclone copy backup-encrypted.tar.gz remote:backups/
```

### Scenario 2: Secure Document Sharing

```bash
# Sender side:
# 1. Generate shared password
cryptovault --generate-password > shared_password.txt

# 2. Encrypt document
cryptovault -e contract.pdf -o contract.pdf.encrypted -p "$(cat shared_password.txt)"

# 3. Send encrypted file via email/cloud
# 4. Share password via different channel (phone, Signal, etc.)

# Recipient side:
# 1. Receive password via secure channel
# 2. Decrypt file
cryptovault -d contract.pdf.encrypted -o contract.pdf -p "ReceivedPassword"
```

### Scenario 3: USB Drive Encryption

```bash
# Encrypt all files on USB drive
USB_PATH="/media/usb"
ENCRYPTED_PATH="/media/usb_encrypted"

# Create encrypted backup
cryptovault -e "$USB_PATH" -o "$ENCRYPTED_PATH" --directory

# Verify encryption
ls -lh "$ENCRYPTED_PATH"

# Delete originals after verification
rm -rf "$USB_PATH"/*
```

### Scenario 4: Password Manager Workflow

```bash
# Create password database
echo "Gmail: user@gmail.com" > passwords.txt
echo "Bank: account123" >> passwords.txt
echo "SSH: privatekey" >> passwords.txt

# Generate master password
MASTER_PASS=$(cryptovault --generate-password --password-length 48)
echo "$MASTER_PASS" | gpg --encrypt -r your@email.com > master.gpg

# Encrypt password database
cryptovault -e passwords.txt -o passwords.encrypted -p "$MASTER_PASS"

# Shred original
cryptovault --shred passwords.txt --shred-passes 7

# To access later:
# 1. Decrypt master password
gpg --decrypt master.gpg

# 2. Decrypt database
cryptovault -d passwords.encrypted -o passwords.txt -p "DecryptedMasterPass"
```

### Scenario 5: Automated Daily Encryption

```bash
#!/bin/bash
# Add to crontab: 0 2 * * * /home/user/encrypt_daily.sh

# Configuration
SOURCE_DIR="$HOME/Documents/work"
ENCRYPTED_DIR="$HOME/encrypted_backups"
PASSWORD_FILE="$HOME/.vault_password"

# Read password from secure file
PASSWORD=$(cat "$PASSWORD_FILE")

# Create dated backup
DATE=$(date +%Y%m%d)
BACKUP_NAME="backup_$DATE"

# Encrypt directory
cryptovault -e "$SOURCE_DIR" -o "$ENCRYPTED_DIR/$BACKUP_NAME" --directory -p "$PASSWORD"

# Keep only last 7 days
find "$ENCRYPTED_DIR" -name "backup_*" -mtime +7 -delete

# Send notification
echo "Daily backup encrypted successfully" | mail -s "Backup Status" your@email.com
```

### Scenario 6: Protecting API Keys

```bash
# Create config file with sensitive data
cat > config.json << EOF
{
  "api_key": "sk-abc123def456",
  "database_url": "postgresql://user:pass@host:5432/db",
  "secret_token": "very_secret_token_here"
}
EOF

# Encrypt config
cryptovault -e config.json -o config.json.encrypted --delete-original

# In your application, decrypt at runtime:
cryptovault -d config.json.encrypted -o /tmp/config.json
# Load config
# Delete after use
rm /tmp/config.json
```

### Scenario 7: Medical Records Protection

```bash
# HIPAA-compliant file encryption

# Scan medical documents
scanimage --format=pdf > medical_record.pdf

# Generate unique password for this patient
PATIENT_ID="12345"
PASSWORD=$(cryptovault --generate-password --password-length 32)

# Encrypt with patient ID in filename
cryptovault -e medical_record.pdf -o "patient_${PATIENT_ID}_encrypted.pdf" -p "$PASSWORD"

# Store password in secure database (example)
echo "$PATIENT_ID:$PASSWORD" | gpg --encrypt -r medical@clinic.com > passwords.gpg

# Shred original
cryptovault --shred medical_record.pdf --shred-passes 7
```

---

## Security Best Practices

### 1. Password Management

```bash
# ✅ GOOD: Generate strong password
cryptovault --generate-password --password-length 32

# ❌ BAD: Weak password
cryptovault -e file.txt -o file.encrypted -p "password123"

# ✅ GOOD: Password prompt (hidden input)
cryptovault -e file.txt -o file.encrypted

# ❌ BAD: Password in command (visible in history)
cryptovault -e file.txt -o file.encrypted -p "MyPassword"
```

### 2. Secure Password Storage

```bash
# ✅ GOOD: Encrypt password with GPG
cryptovault --generate-password | gpg --encrypt -r your@email.com > password.gpg

# ✅ GOOD: Use password manager
cryptovault --generate-password | pass insert encryption/myfile

# ❌ BAD: Plain text file
cryptovault --generate-password > password.txt
```

### 3. Verification Before Deletion

```bash
# ✅ GOOD: Verify then delete
cryptovault -e important.pdf -o important.pdf.encrypted
cryptovault --info important.pdf.encrypted  # Verify
cryptovault -d important.pdf.encrypted -o test.pdf  # Test decrypt
diff important.pdf test.pdf  # Compare
rm important.pdf test.pdf  # Delete if identical

# ❌ BAD: Delete immediately
cryptovault -e important.pdf -o important.pdf.encrypted --delete-original
```

### 4. Backup Encrypted Files

```bash
# ✅ GOOD: Multiple backups
cryptovault -e data.txt -o data.encrypted
cp data.encrypted ~/Dropbox/
cp data.encrypted /media/usb/
cp data.encrypted ~/local_backup/

# ✅ GOOD: Verify checksums
sha256sum data.encrypted > data.encrypted.sha256
```

### 5. Network Transfer

```bash
# ✅ GOOD: Encrypt before upload
cryptovault -e sensitive.pdf -o sensitive.encrypted
scp sensitive.encrypted user@server:/path/

# ❌ BAD: Upload unencrypted
scp sensitive.pdf user@server:/path/
```

---

## Tips and Tricks

### Batch Encryption with Loop

```bash
# Encrypt multiple files with same password
for file in *.pdf; do
  cryptovault -e "$file" -o "$file.encrypted" -p "MySharedPassword"
done
```

### Integrate with Git Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Encrypt secrets before commit
if [ -f config/secrets.json ]; then
  cryptovault -e config/secrets.json -o config/secrets.json.encrypted
  git add config/secrets.json.encrypted
fi
```

### Decrypt to Stdout (for piping)

```bash
# Decrypt and pipe to another command
cryptovault -d data.encrypted -o /dev/stdout | grep "search_term"
```

### Create Encrypted Zip Archive

```bash
# Compress then encrypt
zip -r archive.zip folder/
cryptovault -e archive.zip -o archive.zip.encrypted --delete-original
```

---

## Troubleshooting Examples

### Forgot Password?

```bash
# Unfortunately, there's NO way to recover if password is lost
# This is by design for security

# Prevention:
# 1. Always save passwords securely
# 2. Use multiple password storage methods
# 3. Test decryption immediately after encryption
```

### Check if File is Encrypted

```bash
# View file info (works only on encrypted files)
cryptovault --info myfile.dat

# If it shows metadata, it's encrypted with CryptoVault
# If it errors, it's either not encrypted or corrupted
```

### Recover from Corruption

```bash
# CryptoVault files have checksum verification
# If decrypt shows checksum mismatch, file is corrupted

# You can still attempt decryption:
cryptovault -d corrupted.encrypted -o output.txt
# It will warn you but may still extract partial data
```

---

**Remember**: Always test your encryption/decryption workflow before relying on it for critical data!
