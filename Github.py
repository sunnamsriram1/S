#!/data/data/com.termux/files/usr/bin/bash

# ✅ Configuration
GITHUB_USERNAME="sunnamsriram1"
REPO_NAME="S"
SRC_FOLDER="$HOME/S"
DEST_FOLDER="$HOME/GIT_PUSH_S"
TOKEN=$(cat $SRC_FOLDER/githubtoken.txt)
CLONE_URL="https://${GITHUB_USERNAME}:${TOKEN}@github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

echo "🔁 Cloning repository from GitHub..."
rm -rf "$DEST_FOLDER"
git clone "$CLONE_URL" "$DEST_FOLDER"

if [ $? -ne 0 ]; then
  echo "❌ Clone failed. Please check your token or repo access."
  exit 1
fi

cd "$DEST_FOLDER"

echo "📂 Copying files from $SRC_FOLDER ..."
cp -r $SRC_FOLDER/* .

# Exclude token file itself
rm -f githubtoken.txt

echo "➕ Adding files..."
git add .

echo "📝 Committing changes..."
git commit -m "🚀 Auto-upload from Termux ~/S folder"

echo "☁️ Pushing to GitHub..."
git push

if [ $? -eq 0 ]; then
  echo "✅ All files pushed to: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
else
  echo "❌ Push failed. Check your network or token again."
fi
