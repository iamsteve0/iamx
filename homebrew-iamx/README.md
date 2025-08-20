# Homebrew Tap for iamx

This repository contains the Homebrew formula for [iamx](https://github.com/iamsteve0/iamx) - IAM Policy Explainer.

## Installation

```bash
# Install iamx via Homebrew
brew install iamsteve0/iamx/iamx
```

## What is iamx?

iamx is a local-first IAM policy analyzer that scans AWS IAM JSON policies, detects risky patterns deterministically, explains them in plain English, assigns severity levels, and suggests least-privilege fixes.

## Usage

```bash
# Analyze a policy
iamx analyze policy.json

# Start web interface
iamx web

# Get help
iamx --help
```

## More Information

- [GitHub Repository](https://github.com/iamsteve0/iamx)
- [PyPI Package](https://pypi.org/project/iamx/)
- [Documentation](https://github.com/iamsteve0/iamx#readme)
