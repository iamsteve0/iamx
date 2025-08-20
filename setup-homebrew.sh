#!/bin/bash

echo "🚀 Setting up Homebrew repository for iamx..."
echo ""

# Check if homebrew-iamx directory exists
if [ ! -d "homebrew-iamx" ]; then
    echo "❌ homebrew-iamx directory not found!"
    exit 1
fi

echo "📁 Creating Homebrew repository..."
echo ""

# Create a temporary directory for the Homebrew repo
mkdir -p /tmp/homebrew-iamx-setup
cd /tmp/homebrew-iamx-setup

# Copy the formula files
cp /Users/stevenson/iamx/homebrew-iamx/* .

echo "📝 Files ready for Homebrew repository:"
ls -la

echo ""
echo "🎯 Next steps:"
echo "1. Create a new GitHub repository named 'homebrew-iamx'"
echo "2. Run these commands:"
echo ""
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Add iamx Homebrew formula'"
echo "   git branch -M main"
echo "   git remote add origin https://github.com/iamsteve0/homebrew-iamx.git"
echo "   git push -u origin main"
echo ""
echo "3. Test installation:"
echo "   brew install iamsteve0/iamx/iamx"
echo ""

echo "✅ Setup complete! Follow the steps above to create your Homebrew repository."
