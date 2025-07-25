#!/data/data/com.termux/files/usr/bin/bash

# ✅ GitHub Configuration
GITHUB_USERNAME="sunnamsriram1"
GIT_EMAIL="jj1585105@gmail.com"
REPO_NAME="S"
SRC_FOLDER="$HOME/S"
DEST_FOLDER="$HOME/GIT_PUSH_S"
TOKEN=$(cat "$SRC_FOLDER/githubtoken.txt")
CLONE_URL="https://${GITHUB_USERNAME}:${TOKEN}@github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

# ✅ Step 1: Prepare destination folder
echo "🔁 Cloning repository from GitHub..."
rm -rf "$DEST_FOLDER"
git clone "$CLONE_URL" "$DEST_FOLDER"
cd "$DEST_FOLDER" || exit 1

# ✅ Step 2: Set Git user config (local only)
git config user.name "$GITHUB_USERNAME"
git config user.email "$GIT_EMAIL"

# ✅ Step 3: Copy from source folder
echo "📂 Copying files from $SRC_FOLDER ..."
cp -r "$SRC_FOLDER"/* .

# ✅ Step 4: Clean up unnecessary or harmful files
rm -f githubtoken.txt
find . -type d -name ".git" -exec rm -rf {} +
rm -rf ENCRYPTED_FILES/.git
rm -rf S/.git

# ✅ Step 5: Commit and push
echo "➕ Adding all files..."
git init
git add .

echo "📝 Committing changes..."
git commit -m "🚀 Auto-upload from Termux ~/S folder"

echo "🌱 Creating branch main..."
git branch -M main

echo "☁️ Pushing to GitHub..."
git remote add origin "$CLONE_URL"
git push -u origin main

# ✅ Success message
if [ $? -eq 0 ]; then
  echo "✅ Successfully uploaded to: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
else
  echo "❌ Push failed. Please check your GitHub token or repo name."
fi
