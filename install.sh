#!/data/data/com.termux/files/usr/bin/bash

echo "📦 Installing Python & Pip..."
pkg update -y && pkg upgrade -y
pkg install python python-pip -y

echo "⚠️  Skipping pip upgrade to avoid Termux break."

if [ -f requirements.txt ]; then
    echo "📄 Found requirements.txt"
    pip install --no-cache-dir -r requirements.txt
    echo "✅ All modules installed successfully."
else
    echo "❌ requirements.txt not found!"
fi
pip install colorama 
pip install pytz
#pkg update -y
#pkg install python python-pip -y

#echo "📦 Installing Python packages..."
#pip install -r requirements.txt
