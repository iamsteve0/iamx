#!/bin/bash

echo "🚀 Installing iamx - IAM Policy Explainer..."
echo ""

# Detect OS and suggest best installation method
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 macOS detected"
    echo ""
    echo "💡 For macOS users, we recommend:"
    echo "   pipx install iamx    # Isolated installation (recommended)"
    echo "   brew install iamsteve0/tap/iamx  # Homebrew (if available)"
    echo ""
    echo "📦 Installing with pip..."
    echo ""
fi

# Try pip install first
pip install iamx --quiet

if [ $? -eq 0 ]; then
    echo "✅ iamx installed successfully!"
    echo ""
    echo "🎯 Quick start:"
    echo "  iamx --help          # See all commands"
    echo "  iamx analyze policy.json  # Analyze a policy"
    echo "  iamx web             # Start web interface"
    echo ""
    echo "📖 For more info: https://github.com/iamsteve0/iamx"
else
    echo "❌ pip installation failed."
    echo ""
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "💡 Try these alternatives:"
        echo "   pipx install iamx"
        echo "   python3 -m venv venv && source venv/bin/activate && pip install iamx"
    else
        echo "💡 Try: pip install iamx --verbose"
    fi
    exit 1
fi
