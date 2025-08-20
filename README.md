# iamx - IAM Policy Explainer

[![PyPI version](https://badge.fury.io/py/iamx.svg)](https://badge.fury.io/py/iamx)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A local-first IAM policy analyzer that scans AWS IAM JSON policies, detects risky patterns deterministically, explains them in plain English, assigns severity levels, and suggests least-privilege fixes.

## 🎯 Why iamx?

Copy-pasting IAM policies into ChatGPT is unsafe, inaccurate, and doesn't scale for bulk analysis. Manual policy review is time-consuming and error-prone.

**iamx solves these problems:**
- ✅ **Accuracy first** - Static parser + deterministic rules (no hallucinations)
- ✅ **Human-readable explanations** - Plain English descriptions of risks
- ✅ **Bulk scanning** - Process multiple policies efficiently
- ✅ **CI/CD integration** - GitHub Actions with configurable thresholds
- ✅ **Privacy-first** - Local by default, optional AI summaries
- ✅ **Multiple outputs** - Markdown, JSON, and interactive web reports

## 🚀 Features

### Core Analysis
- **Deterministic pattern detection** - No AI hallucinations, consistent results
- **Risk severity classification** - Critical/High/Medium/Low based on impact
- **Plain English explanations** - Understandable descriptions of each finding
- **Least-privilege suggestions** - Specific recommendations for policy improvements

### Supported Patterns
- Overly permissive actions (`*` permissions)
- Wildcard resources without restrictions
- Cross-account access patterns
- Administrative actions detection
- Data access actions analysis
- Missing resource restrictions
- Sensitive service permissions

### Output Formats
- **CLI** - Terminal output with color-coded results
- **Web UI** - Interactive local web interface
- **Markdown** - Detailed reports for documentation
- **JSON** - Machine-readable output for CI/CD
- **GitHub Actions** - Automated policy reviews in PRs

## 🛠️ Installation

```bash
# Option 1: One-liner (recommended)
pip install iamx

# Option 2: Homebrew (macOS users)
brew install iamsteve0/iamx/iamx

# Option 2b: pipx (isolated Python installation)
pipx install iamx

# Option 3: Clean installation script
curl -sSL https://raw.githubusercontent.com/iamsteve0/iamx/main/install.sh | bash

# Option 4: Quiet installation (less output)
pip install iamx --quiet

# What you'll see:
# ✅ Successfully installed iamx-0.1.0
# (All dependencies are installed automatically)

## 🍎 macOS Users

If you encounter "externally-managed-environment" errors:

```bash
# Option 1: Use pipx (recommended)
pipx install iamx

# Option 2: Use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install iamx

# Option 3: Use Homebrew (when available)
brew install iamsteve0/iamx/iamx
```

# Or install from source
git clone https://github.com/iamsteve0/iamx.git
cd iamx
pip install -e .
```

## 📖 Quick Start

**Install and use iamx in 30 seconds:**

```bash
# Install (one command!)
pip install iamx

# Analyze a policy (one command!)
iamx analyze policy.json

# Start web UI (one command!)
iamx web
```

### CLI Usage

```bash
# Analyze a single policy file
iamx analyze policy.json

# Analyze multiple policies
iamx analyze policies/*.json

# Generate detailed report
iamx analyze policy.json --output report.md --format markdown

# Set severity threshold for CI
iamx analyze policy.json --fail-on high
```

### Web UI

```bash
# Start the local web interface
iamx web

# The interface will automatically find an available port
# Usually starts at http://localhost:8081
# If port 8081 is busy, it will try 8082, 8083, etc.

# You can also specify a custom port:
iamx web --port 9000
```

### GitHub Actions Integration

```yaml
name: IAM Policy Review
on: [pull_request]
jobs:
  iamx:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install iamx
        run: pip install iamx
      - name: Run iamx analysis
        run: iamx analyze policies/ --output iamx-report.md --format markdown
      - name: Comment on PR
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('iamx-report.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## 🔍 IAM Policy Security Analysis\n\n${report}\n\n---\n*This analysis was performed by [iamx](https://github.com/iamsteve0/iamx) - IAM Policy Explainer*`
            });
```

## 📊 Example Output

```
🔍 Analyzing IAM Policy: admin-policy.json

❌ CRITICAL: Overly Permissive Actions
   The policy grants '*' permissions on all resources for ec2:* actions.
   This allows full EC2 control including instance termination and data access.
   
   Recommendation: Replace with specific actions like:
   - ec2:DescribeInstances
   - ec2:StartInstances
   - ec2:StopInstances

⚠️  HIGH: Missing Resource Restrictions
   The policy allows s3:GetObject on any S3 bucket without restrictions.
   This could expose sensitive data across all buckets.
   
   Recommendation: Add resource ARN restrictions:
   "Resource": "arn:aws:s3:::my-bucket/*"

✅ LOW: Consider Adding Conditions
   The policy doesn't require MFA for administrative actions.
   
   Recommendation: Add MFA condition for sensitive operations.
```

## 🏗️ Architecture

```
iamx/
├── core/           # Core analysis engine
├── cli/            # Command-line interface
├── web/            # Web UI components
├── rules/          # Policy analysis rules
├── reports/        # Report generators
├── github/         # GitHub Actions integration
└── tests/          # Test suite
```

## 🔧 Troubleshooting

### Web UI Issues

**Port already in use:**
```bash
# iamx automatically finds available ports, but you can specify one:
iamx web --port 9000
```

**Web interface won't start:**
```bash
# Check if dependencies are installed:
pip install iamx[web]

# Try a different host:
iamx web --host 0.0.0.0 --port 8081
```

### CLI Issues

**Permission denied:**
```bash
# On macOS/Linux, you might need:
sudo pip install iamx

# Or use a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install iamx
```

**Too much output during installation:**
```bash
# Use quiet mode for cleaner output:
pip install iamx --quiet

# Or suppress dependency details:
pip install iamx --no-deps
```

**macOS "externally-managed-environment" error:**
```bash
# Option 1: Use Homebrew (recommended)
brew install iamsteve0/tap/iamx

# Option 2: Use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install iamx

# Option 3: Use pipx (isolated installation)
pipx install iamx

# Option 4: Use conda
conda install -c conda-forge iamx
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/yourusername/iamx.git
cd iamx
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
black .
flake8 .
```

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Built with modern Python tooling and best practices
- Designed for the security and DevOps community
- Inspired by the need for better IAM policy analysis tools
