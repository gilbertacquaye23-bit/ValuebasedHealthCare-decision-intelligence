# Publish to GitHub

Suggested repository: vbhc-decision-intelligence. Start private until the initial review is complete.

From the project directory with authenticated GitHub CLI:

```bash
git init -b main
git add .
git commit -m "Release healthcare decision intelligence workflow"
gh repo create vbhc-decision-intelligence --private --source=. --remote=origin --push
```

If already initialized, inspect `git status` and remotes first rather than repeating initialization. For an existing destination, add its verified URL as the origin and push the main branch. Never commit credentials, raw private data, local environments, or generated model files.

Verify the Actions workflow passes, review the README and methodology, choose a license, and create a v0.1.0 release after completing a full reproducibility run. Publishing this repository hosts code; it does not deploy a running web application.
