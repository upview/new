# TofuPilot Python Client - PR #143

> **⚠️ Development Branch**: Preview of changes from PR #143
> For stable version, see [main branch](https://github.com/upview/new/tree/main)

**Original PR**: [Add Python client auto-generation with commit-based strategy](https://github.com/tofupilot/app/pull/143)
**Branch**: `julien/app-3688`

## Preview Installation
```bash
pip install git+https://github.com/upview/new.git@pr-143
```

## Changes
- Add generation workflow that waits for Vercel deployment and commits changes
- Add release workflow that publishes to PyPI only when generated files change
- Configure Python client generation with dotted notation API
- Update gitignore to track auto-generated files for diff detection


---
🔄 Auto-synced from PR: https://github.com/tofupilot/app/pull/143
