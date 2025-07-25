#!/data/data/com.termux/files/usr/bin/bash

# ✅ GitHub Configuration
GITHUB_USERNAME="sunnamsriram1"
GIT_EMAIL="jj1585105@gmail.com"
REPO_NAME="S"
SRC_FOLDER="$HOME/S"
DEST_FOLDER="$HOME/GIT_PUSH_S"
TOKEN=$(cat "$SRC_FOLDER/githubtoken.txt")
CLONE_URL="https://${GITHUB_USERNAME}:${TOKEN}@github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

echo "🔁 Cloning repository from GitHub..."
rm -rf "$DEST_FOLDER"
git clone "$CLONE_URL" "$DEST_FOLDER"
cd "$DEST_FOLDER" || exit 1

# 🛠️ Configure Git user details
git config user.name "$GITHUB_USERNAME"
git config user.email "$GIT_EMAIL"

echo "📂 Copying files from $SRC_FOLDER ..."
cp -r "$SRC_FOLDER"/* .

# 🧹 Remove .git folders from any embedded repositories (e.g., ENCRYPTED_FILES or S)
find . -type d -name ".git" -exec rm -rf {} +

# ❌ Don't upload your token file
rm -f githubtoken.txt

echo "➕ Adding all files..."
git add .

echo "📝 Committing changes..."
git commit -m "🚀 Auto-upload from Termux ~/S folder"

# 🌱 Create or switch to main branch
git branch -M main

echo "☁️ Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
  echo "✅ Successfully uploaded to: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
else
  echo "❌ Push failed. Please check your internet or GitHub token."
fi
