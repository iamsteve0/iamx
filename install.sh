#!/bin/bash

echo "🚀 Installing iamx - IAM Policy Explainer..."
echo ""

# Install with quiet output
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
    echo "❌ Installation failed. Try: pip install iamx --verbose"
    exit 1
fi
