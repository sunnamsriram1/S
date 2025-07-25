#!/bin/bash

# === CONFIG ===
ENV_DIR="myenv"
SCRIPT="Ram2.py"

# === Colors ===
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}[*] Starting Python environment setup...${NC}"

# Check for python3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[!] Python3 is not installed. Install it first.${NC}"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$ENV_DIR" ]; then
    python3 -m venv "$ENV_DIR"
    echo -e "${GREEN}[+] Virtual environment created at: $ENV_DIR${NC}"
else
    echo -e "${GREEN}[=] Virtual environment already exists.${NC}"
fi

# Activate virtual environment
source "$ENV_DIR/bin/activate"

# Upgrade pip
echo -e "${GREEN}[*] Upgrading pip...${NC}"
pip install --upgrade pip

# Install requirements
echo -e "${GREEN}[*] Installing required Python packages...${NC}"
pip install requests PySocks pytz psutil speedtest-cli colorama

# Check if script exists
if [ ! -f "$SCRIPT" ]; then
    echo -e "${RED}[!] Python script '$SCRIPT' not found in current directory.${NC}"
    deactivate
    exit 1
fi

# Run the script
echo -e "${GREEN}[*] Running $SCRIPT...${NC}"
python "$SCRIPT"

# Done
deactivate
echo -e "${GREEN}[?] Script execution complete. Environment deactivated.${NC}"
