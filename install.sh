#!/bin/bash

################################################################################
# CryptoVault Installer for Debian/Ubuntu
# Quick install: curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/cryptovault/main/install.sh | sudo bash
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Banner
echo -e "${CYAN}"
cat << "EOF"
  ____                  _        __     __          _ _   
 / ___|_ __ _   _ _ __ | |_ ___  \ \   / /_ _ _   _| | |_ 
| |   | '__| | | | '_ \| __/ _ \  \ \ / / _` | | | | | __|
| |___| |  | |_| | |_) | || (_) |  \ V / (_| | |_| | | |_ 
 \____|_|   \__, | .__/ \__\___/    \_/ \__,_|\__,_|_|\__|
            |___/|_|                                       
                  Installation Script
EOF
echo -e "${NC}"

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    SUDO=""
else
    SUDO="sudo"
fi

echo -e "${GREEN}[+] Starting CryptoVault installation...${NC}\n"

# Update package list
echo -e "${YELLOW}[*] Updating package list...${NC}"
$SUDO apt update -qq

# Install Python3 and pip if not installed
echo -e "${YELLOW}[*] Installing Python3 and pip...${NC}"
$SUDO apt install -y python3 python3-pip python3-venv 2>/dev/null

# Install cryptography library
echo -e "${YELLOW}[*] Installing cryptography library...${NC}"
pip3 install --user cryptography 2>/dev/null || $SUDO pip3 install cryptography

# Download the main script
echo -e "${YELLOW}[*] Downloading CryptoVault...${NC}"
if [ -f "cryptovault.py" ]; then
    echo -e "${BLUE}[i] Using local cryptovault.py${NC}"
else
    curl -sSL https://raw.githubusercontent.com/Medbelkacem/cryptovault/main/cryptovault.py -o cryptovault.py 2>/dev/null || {
        echo -e "${RED}[✗] Failed to download. Using local installation.${NC}"
    }
fi

# Make it executable
chmod +x cryptovault.py

# Copy to /usr/local/bin
echo -e "${YELLOW}[*] Installing to /usr/local/bin...${NC}"
$SUDO cp cryptovault.py /usr/local/bin/cryptovault
$SUDO chmod +x /usr/local/bin/cryptovault

# Verify installation
if command -v cryptovault &> /dev/null; then
    echo -e "\n${GREEN}╔═══════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                           ║${NC}"
    echo -e "${GREEN}║  ✓ CryptoVault installed successfully!   ║${NC}"
    echo -e "${GREEN}║                                           ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════╝${NC}\n"
    
    echo -e "${CYAN}Usage Examples:${NC}"
    echo -e "${BLUE}  Encrypt a file:${NC}"
    echo -e "    cryptovault -e secret.txt -o secret.txt.encrypted"
    echo -e ""
    echo -e "${BLUE}  Decrypt a file:${NC}"
    echo -e "    cryptovault -d secret.txt.encrypted -o secret.txt"
    echo -e ""
    echo -e "${BLUE}  Generate password:${NC}"
    echo -e "    cryptovault --generate-password"
    echo -e ""
    echo -e "${BLUE}  Get help:${NC}"
    echo -e "    cryptovault --help"
    echo -e ""
else
    echo -e "${RED}[✗] Installation failed. Please check errors above.${NC}"
    exit 1
fi

echo -e "${GREEN}Happy encrypting! 🔐${NC}\n"
