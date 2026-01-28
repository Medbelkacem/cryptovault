#!/usr/bin/env python3
"""
CryptoVault - Professional File Encryption/Decryption Tool
Author: Medbelkacem
GitHub: https://github.com/Medbelkacem
License: MIT
"""

import os
import sys
import argparse
import getpass
import hashlib
import secrets
import base64
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError:
    print("Error: Required cryptography library not found.")
    print("Install it with: pip3 install cryptography")
    sys.exit(1)

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class CryptoVault:
    """Main encryption/decryption class"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.chunk_size = 64 * 1024  # 64KB chunks for large files
        
    def print_banner(self):
        """Display tool banner"""
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║   ██████╗██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗  ║
║  ██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗ ║
║  ██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║ ║
║  ██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║   ██║ ║
║  ╚██████╗██║  ██║   ██║   ██║        ██║   ╚██████╔╝ ║
║   ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝  ║
║                                                       ║
║              VAULT - File Encryption Tool            ║
║                    Version {self.version}                    ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
{Colors.END}
        """
        print(banner)
    
    def derive_key(self, password: str, salt: bytes) -> bytes:
        """Derive a key from password using PBKDF2"""
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    def encrypt_file(self, input_file: str, output_file: str, password: str, 
                    delete_original: bool = False) -> bool:
        """
        Encrypt a file using AES-256
        
        Args:
            input_file: Path to file to encrypt
            output_file: Path for encrypted output
            password: Encryption password
            delete_original: Whether to delete original file
            
        Returns:
            bool: Success status
        """
        try:
            # Check if input file exists
            if not os.path.exists(input_file):
                print(f"{Colors.RED}[✗] Error: File '{input_file}' not found{Colors.END}")
                return False
            
            # Generate random salt
            salt = secrets.token_bytes(16)
            
            # Derive key from password
            key = self.derive_key(password, salt)
            
            # Create Fernet instance
            fernet = Fernet(key)
            
            # Get file size for progress
            file_size = os.path.getsize(input_file)
            
            print(f"{Colors.BLUE}[*] Encrypting: {input_file}{Colors.END}")
            print(f"{Colors.BLUE}[*] File size: {self.format_size(file_size)}{Colors.END}")
            
            # Read and encrypt file
            with open(input_file, 'rb') as f:
                file_data = f.read()
            
            encrypted_data = fernet.encrypt(file_data)
            
            # Create metadata
            metadata = {
                'version': self.version,
                'filename': os.path.basename(input_file),
                'timestamp': datetime.now().isoformat(),
                'size': file_size,
                'checksum': hashlib.sha256(file_data).hexdigest()
            }
            
            # Write encrypted file with salt and metadata
            with open(output_file, 'wb') as f:
                # Write salt
                f.write(salt)
                # Write metadata length (4 bytes)
                metadata_json = json.dumps(metadata).encode()
                f.write(len(metadata_json).to_bytes(4, byteorder='big'))
                # Write metadata
                f.write(metadata_json)
                # Write encrypted data
                f.write(encrypted_data)
            
            print(f"{Colors.GREEN}[✓] File encrypted successfully!{Colors.END}")
            print(f"{Colors.GREEN}[✓] Output: {output_file}{Colors.END}")
            
            # Delete original if requested
            if delete_original:
                os.remove(input_file)
                print(f"{Colors.YELLOW}[!] Original file deleted{Colors.END}")
            
            return True
            
        except Exception as e:
            print(f"{Colors.RED}[✗] Encryption failed: {str(e)}{Colors.END}")
            return False
    
    def decrypt_file(self, input_file: str, output_file: str, password: str,
                    delete_encrypted: bool = False) -> bool:
        """
        Decrypt a file
        
        Args:
            input_file: Path to encrypted file
            output_file: Path for decrypted output
            password: Decryption password
            delete_encrypted: Whether to delete encrypted file
            
        Returns:
            bool: Success status
        """
        try:
            # Check if input file exists
            if not os.path.exists(input_file):
                print(f"{Colors.RED}[✗] Error: File '{input_file}' not found{Colors.END}")
                return False
            
            print(f"{Colors.BLUE}[*] Decrypting: {input_file}{Colors.END}")
            
            with open(input_file, 'rb') as f:
                # Read salt
                salt = f.read(16)
                
                # Read metadata length
                metadata_length = int.from_bytes(f.read(4), byteorder='big')
                
                # Read metadata
                metadata_json = f.read(metadata_length)
                metadata = json.loads(metadata_json.decode())
                
                # Read encrypted data
                encrypted_data = f.read()
            
            # Derive key from password
            key = self.derive_key(password, salt)
            
            # Create Fernet instance
            fernet = Fernet(key)
            
            # Decrypt data
            try:
                decrypted_data = fernet.decrypt(encrypted_data)
            except Exception:
                print(f"{Colors.RED}[✗] Decryption failed: Invalid password or corrupted file{Colors.END}")
                return False
            
            # Verify checksum
            calculated_checksum = hashlib.sha256(decrypted_data).hexdigest()
            if calculated_checksum != metadata['checksum']:
                print(f"{Colors.RED}[✗] Warning: Checksum mismatch! File may be corrupted{Colors.END}")
                response = input(f"{Colors.YELLOW}Continue anyway? (y/N): {Colors.END}")
                if response.lower() != 'y':
                    return False
            
            # Write decrypted file
            with open(output_file, 'wb') as f:
                f.write(decrypted_data)
            
            print(f"{Colors.GREEN}[✓] File decrypted successfully!{Colors.END}")
            print(f"{Colors.GREEN}[✓] Output: {output_file}{Colors.END}")
            print(f"{Colors.CYAN}[i] Original filename: {metadata['filename']}{Colors.END}")
            print(f"{Colors.CYAN}[i] Encrypted on: {metadata['timestamp']}{Colors.END}")
            
            # Delete encrypted if requested
            if delete_encrypted:
                os.remove(input_file)
                print(f"{Colors.YELLOW}[!] Encrypted file deleted{Colors.END}")
            
            return True
            
        except Exception as e:
            print(f"{Colors.RED}[✗] Decryption failed: {str(e)}{Colors.END}")
            return False
    
    def encrypt_directory(self, directory: str, output_dir: str, password: str,
                         delete_original: bool = False) -> Tuple[int, int]:
        """
        Encrypt all files in a directory
        
        Returns:
            Tuple of (successful, failed) counts
        """
        success_count = 0
        fail_count = 0
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Get all files in directory
        files = []
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                files.append(os.path.join(root, filename))
        
        print(f"{Colors.BLUE}[*] Found {len(files)} files to encrypt{Colors.END}\n")
        
        for i, file_path in enumerate(files, 1):
            print(f"{Colors.CYAN}[{i}/{len(files)}]{Colors.END}", end=" ")
            
            # Create relative path for output
            rel_path = os.path.relpath(file_path, directory)
            output_path = os.path.join(output_dir, rel_path + '.encrypted')
            
            # Create subdirectories if needed
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            if self.encrypt_file(file_path, output_path, password, delete_original):
                success_count += 1
            else:
                fail_count += 1
            print()
        
        return success_count, fail_count
    
    def generate_password(self, length: int = 32, include_special: bool = True) -> str:
        """Generate a secure random password"""
        import string
        
        chars = string.ascii_letters + string.digits
        if include_special:
            chars += string.punctuation
        
        password = ''.join(secrets.choice(chars) for _ in range(length))
        return password
    
    def shred_file(self, filepath: str, passes: int = 3) -> bool:
        """
        Securely delete a file by overwriting it multiple times
        
        Args:
            filepath: Path to file to shred
            passes: Number of overwrite passes
            
        Returns:
            bool: Success status
        """
        try:
            if not os.path.exists(filepath):
                print(f"{Colors.RED}[✗] Error: File '{filepath}' not found{Colors.END}")
                return False
            
            file_size = os.path.getsize(filepath)
            
            print(f"{Colors.YELLOW}[*] Shredding: {filepath}{Colors.END}")
            print(f"{Colors.YELLOW}[*] Passes: {passes}{Colors.END}")
            
            with open(filepath, 'ba+') as f:
                for i in range(passes):
                    f.seek(0)
                    f.write(os.urandom(file_size))
                    f.flush()
                    os.fsync(f.fileno())
                    print(f"{Colors.YELLOW}[*] Pass {i+1}/{passes} completed{Colors.END}")
            
            # Delete the file
            os.remove(filepath)
            
            print(f"{Colors.GREEN}[✓] File securely shredded and deleted{Colors.END}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}[✗] Shredding failed: {str(e)}{Colors.END}")
            return False
    
    def file_info(self, filepath: str) -> bool:
        """Display information about an encrypted file"""
        try:
            if not os.path.exists(filepath):
                print(f"{Colors.RED}[✗] Error: File '{filepath}' not found{Colors.END}")
                return False
            
            with open(filepath, 'rb') as f:
                # Skip salt
                f.seek(16)
                
                # Read metadata
                metadata_length = int.from_bytes(f.read(4), byteorder='big')
                metadata_json = f.read(metadata_length)
                metadata = json.loads(metadata_json.decode())
            
            print(f"\n{Colors.CYAN}{Colors.BOLD}Encrypted File Information:{Colors.END}")
            print(f"{Colors.BLUE}{'─' * 50}{Colors.END}")
            print(f"{Colors.GREEN}Original Filename:{Colors.END} {metadata['filename']}")
            print(f"{Colors.GREEN}Encrypted On:{Colors.END} {metadata['timestamp']}")
            print(f"{Colors.GREEN}Original Size:{Colors.END} {self.format_size(metadata['size'])}")
            print(f"{Colors.GREEN}Checksum (SHA256):{Colors.END} {metadata['checksum']}")
            print(f"{Colors.GREEN}Tool Version:{Colors.END} {metadata['version']}")
            print(f"{Colors.BLUE}{'─' * 50}{Colors.END}\n")
            
            return True
            
        except Exception as e:
            print(f"{Colors.RED}[✗] Error reading file info: {str(e)}{Colors.END}")
            return False
    
    @staticmethod
    def format_size(bytes_size: int) -> str:
        """Format bytes to human readable size"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} PB"

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='CryptoVault - Professional File Encryption/Decryption Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Encrypt a file
  cryptovault -e secret.txt -o secret.txt.encrypted
  
  # Decrypt a file
  cryptovault -d secret.txt.encrypted -o secret.txt
  
  # Encrypt entire directory
  cryptovault -e /path/to/dir -o /path/to/encrypted_dir --directory
  
  # Generate secure password
  cryptovault --generate-password
  
  # Shred (securely delete) a file
  cryptovault --shred sensitive.txt
  
  # Show encrypted file info
  cryptovault --info file.encrypted
        """
    )
    
    parser.add_argument('-e', '--encrypt', metavar='FILE', help='File or directory to encrypt')
    parser.add_argument('-d', '--decrypt', metavar='FILE', help='File to decrypt')
    parser.add_argument('-o', '--output', metavar='FILE', help='Output file or directory')
    parser.add_argument('-p', '--password', metavar='PASS', help='Encryption password (prompt if not provided)')
    parser.add_argument('--directory', action='store_true', help='Encrypt/decrypt entire directory')
    parser.add_argument('--delete-original', action='store_true', help='Delete original file after encryption/decryption')
    parser.add_argument('--generate-password', action='store_true', help='Generate a secure random password')
    parser.add_argument('--password-length', type=int, default=32, help='Length of generated password (default: 32)')
    parser.add_argument('--shred', metavar='FILE', help='Securely delete a file')
    parser.add_argument('--shred-passes', type=int, default=3, help='Number of shred passes (default: 3)')
    parser.add_argument('--info', metavar='FILE', help='Show information about encrypted file')
    parser.add_argument('--version', action='version', version='CryptoVault 1.0.0')
    parser.add_argument('--no-banner', action='store_true', help='Hide banner')
    
    args = parser.parse_args()
    
    # Create CryptoVault instance
    vault = CryptoVault()
    
    # Show banner
    if not args.no_banner:
        vault.print_banner()
    
    # Generate password
    if args.generate_password:
        password = vault.generate_password(args.password_length)
        print(f"{Colors.GREEN}[✓] Generated Password:{Colors.END}")
        print(f"{Colors.BOLD}{password}{Colors.END}")
        print(f"\n{Colors.YELLOW}[!] Save this password in a secure location!{Colors.END}")
        return
    
    # Shred file
    if args.shred:
        vault.shred_file(args.shred, args.shred_passes)
        return
    
    # Show file info
    if args.info:
        vault.file_info(args.info)
        return
    
    # Encrypt or decrypt
    if args.encrypt or args.decrypt:
        # Get password
        if args.password:
            password = args.password
        else:
            password = getpass.getpass(f"{Colors.CYAN}Enter password: {Colors.END}")
            
            if args.encrypt:
                confirm = getpass.getpass(f"{Colors.CYAN}Confirm password: {Colors.END}")
                if password != confirm:
                    print(f"{Colors.RED}[✗] Passwords do not match!{Colors.END}")
                    return
        
        # Encrypt
        if args.encrypt:
            if not args.output:
                print(f"{Colors.RED}[✗] Error: Output file/directory required (-o){Colors.END}")
                return
            
            if args.directory:
                success, failed = vault.encrypt_directory(
                    args.encrypt, args.output, password, args.delete_original
                )
                print(f"\n{Colors.GREEN}[✓] Encryption complete!{Colors.END}")
                print(f"{Colors.GREEN}[✓] Successful: {success}{Colors.END}")
                if failed > 0:
                    print(f"{Colors.RED}[✗] Failed: {failed}{Colors.END}")
            else:
                vault.encrypt_file(args.encrypt, args.output, password, args.delete_original)
        
        # Decrypt
        elif args.decrypt:
            if not args.output:
                print(f"{Colors.RED}[✗] Error: Output file required (-o){Colors.END}")
                return
            
            vault.decrypt_file(args.decrypt, args.output, password, args.delete_original)
    
    else:
        parser.print_help()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Operation cancelled by user{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}[✗] Fatal error: {str(e)}{Colors.END}")
        sys.exit(1)
