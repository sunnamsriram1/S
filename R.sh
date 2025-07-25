#!/data/data/com.termux/files/usr/bin/bash

# 🔐 SimRansom Safe File Locker (.sh Version)
# Author: S Gamer001

EXT=".locked"
ALLOWED="txt pdf jpg png mp3 py sh apk json"

read -p "🔄 Mode (lock/unlock): " MODE
read -p "📁 Target folder: " FOLDER
read -sp "🔑 Password: " PASSWORD
echo

if [[ ! -d "$FOLDER" ]]; then
    echo "[X] Invalid folder: $FOLDER"
    exit 1
fi

# Loop through files
find "$FOLDER" -type f | while read FILE; do
    BASENAME=$(basename "$FILE")
    EXTENSION="${BASENAME##*.}"

    if [[ "$MODE" == "lock" ]]; then
        if [[ "$ALLOWED" =~ "$EXTENSION" ]] && [[ "$FILE" != *"$EXT" ]]; then
            openssl enc -aes-256-cbc -salt -in "$FILE" -out "$FILE$EXT" -k "$PASSWORD" 2>/dev/null
            if [[ $? -eq 0 ]]; then
                echo "[✓] Locked: $FILE"
                rm -f "$FILE"
            else
                echo "[!] Error encrypting: $FILE"
            fi
        fi
    elif [[ "$MODE" == "unlock" ]]; then
        if [[ "$FILE" == *"$EXT" ]]; then
            OUTFILE="${FILE%$EXT}"
            openssl enc -aes-256-cbc -d -in "$FILE" -out "$OUTFILE" -k "$PASSWORD" 2>/dev/null
            if [[ $? -eq 0 ]]; then
                echo "[✓] Unlocked: $OUTFILE"
                rm -f "$FILE"
            else
                echo "[!] Wrong password or failed: $FILE"
            fi
        fi
    fi
done
