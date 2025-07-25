#!/data/data/com.termux/files/usr/bin/bash

# 📁 Source: Your Termux Home directory
SOURCE_DIR="/data/data/com.termux/files/home"

# 🎯 Destination: Internal Storage Documents folder
DEST_DIR="$SOURCE_DIR/storage/documents/R/Termux_Coding"

# ✅ Create destination folder if it doesn't exist
mkdir -p "$DEST_DIR"

echo -e "\n📂 Copying files to: $DEST_DIR"

# 📄 Copy all .py, .sh, .txt files
cp -v "$SOURCE_DIR"/*.py "$SOURCE_DIR"/*.sh "$SOURCE_DIR"/*.txt "$DEST_DIR" 2>/dev/null

# 📁 Copy important folders: S, sqlmap, APP, logs, etc.
FOLDERS=("S" "sqlmap" "APP" "logs" "ENCRYPTED_FILES" "GIT_PUSH_S")

for folder in "${FOLDERS[@]}"; do
    if [ -d "$SOURCE_DIR/$folder" ]; then
        echo "📁 Copying folder: $folder ..."
        cp -rv "$SOURCE_DIR/$folder" "$DEST_DIR/"
    else
        echo "⚠️ Folder not found: $folder"
    fi
done

echo -e "\n✅ Copy complete. Backup available at:\n📁 $DEST_DIR"
