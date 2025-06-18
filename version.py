#!/usr/bin/env python3
"""
Automatic version determination based on conventional commits.

This script analyzes git commit history to determine the next version number
following semantic versioning (MAJOR.MINOR.PATCH) with optional dev builds.

Version bumping rules:
- BREAKING CHANGE or feat!: Bump MAJOR
- feat: Bump MINOR  
- fix: Bump PATCH
- Other commits: No version bump

Dev builds:
- Non-main branches: x.x.x.devN (where N is commits since last release)
- Main branch: x.x.x (production release)
"""

import re
import subprocess
import sys
from typing import Tuple, Optional, List


def run_git_command(cmd: List[str]) -> str:
    """Run a git command and return the output."""
    try:
        result = subprocess.run(
            ["git"] + cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}", file=sys.stderr)
        return ""


def parse_version(version_str: str) -> Tuple[int, int, int]:
    """Parse version string into (major, minor, patch) tuple."""
    # Remove 'v' prefix if present
    version_str = version_str.lstrip('v')
    
    # Handle dev versions by removing .devN suffix
    version_str = re.sub(r'\.dev\d+$', '', version_str)
    
    # Parse major.minor.patch
    parts = version_str.split('.')
    if len(parts) >= 3:
        try:
            return int(parts[0]), int(parts[1]), int(parts[2])
        except ValueError:
            pass
    
    # Default to 0.0.0 if parsing fails
    return 0, 0, 0


def get_latest_tag() -> Optional[str]:
    """Get the latest version tag from git."""
    tags = run_git_command(["tag", "--list", "--sort=-v:refname"])
    if not tags:
        return None
    
    # Find first tag that looks like a version
    for tag in tags.split('\n'):
        if re.match(r'^v?\d+\.\d+\.\d+', tag):
            return tag
    
    return None


def get_commits_since_tag(tag: str) -> List[str]:
    """Get commit messages since the given tag."""
    if not tag:
        # Get all commits if no tag
        commits = run_git_command(["log", "--pretty=format:%s", "--reverse"])
    else:
        # Get commits since tag
        commits = run_git_command(["log", f"{tag}..HEAD", "--pretty=format:%s", "--reverse"])
    
    return [commit.strip() for commit in commits.split('\n') if commit.strip()]


def analyze_commits(commits: List[str]) -> Tuple[bool, bool, bool]:
    """
    Analyze commits to determine version bump type.
    
    Returns:
        (has_breaking, has_feature, has_fix)
    """
    has_breaking = False
    has_feature = False
    has_fix = False
    
    for commit in commits:
        # Check for breaking changes
        if "BREAKING CHANGE" in commit or re.search(r'\w+!:', commit):
            has_breaking = True
        
        # Check for features
        elif commit.startswith('feat:') or commit.startswith('feat('):
            has_feature = True
        
        # Check for fixes
        elif commit.startswith('fix:') or commit.startswith('fix('):
            has_fix = True
    
    return has_breaking, has_feature, has_fix


def bump_version(current: Tuple[int, int, int], has_breaking: bool, has_feature: bool, has_fix: bool) -> Tuple[int, int, int]:
    """Bump version based on commit analysis."""
    major, minor, patch = current
    
    if has_breaking:
        return major + 1, 0, 0
    elif has_feature:
        return major, minor + 1, 0
    elif has_fix:
        return major, minor, patch + 1
    else:
        # No version bump needed
        return major, minor, patch


def get_current_branch() -> str:
    """Get the current git branch name."""
    return run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])


def count_commits_since_tag(tag: str) -> int:
    """Count commits since the given tag."""
    if not tag:
        # Count all commits if no tag
        commits = run_git_command(["rev-list", "--count", "HEAD"])
    else:
        commits = run_git_command(["rev-list", "--count", f"{tag}..HEAD"])
    
    try:
        return int(commits)
    except ValueError:
        return 0


def determine_version() -> str:
    """Determine the next version based on commit history."""
    # Get latest version tag
    latest_tag = get_latest_tag()
    
    # Parse current version
    if latest_tag:
        current_version = parse_version(latest_tag)
        print(f"📦 Latest tag: {latest_tag} -> {current_version}", file=sys.stderr)
    else:
        current_version = (0, 0, 0)
        print("📦 No version tags found, starting from 0.0.0", file=sys.stderr)
    
    # Get commits since last tag
    commits = get_commits_since_tag(latest_tag)
    commit_count = len(commits)
    
    print(f"🔍 Found {commit_count} commits since last release", file=sys.stderr)
    
    if commit_count == 0:
        # No new commits, return current version
        version_str = f"{current_version[0]}.{current_version[1]}.{current_version[2]}"
        print(f"✅ No new commits, using current version: {version_str}", file=sys.stderr)
        return version_str
    
    # Analyze commits for version bumping
    has_breaking, has_feature, has_fix = analyze_commits(commits)
    
    print(f"📊 Commit analysis:", file=sys.stderr)
    print(f"  Breaking changes: {has_breaking}", file=sys.stderr)
    print(f"  New features: {has_feature}", file=sys.stderr)
    print(f"  Bug fixes: {has_fix}", file=sys.stderr)
    
    # Determine new version
    new_version = bump_version(current_version, has_breaking, has_feature, has_fix)
    
    # Check if we're on main branch
    current_branch = get_current_branch()
    is_main_branch = current_branch in ['main', 'master']
    
    print(f"🌿 Current branch: {current_branch} (main: {is_main_branch})", file=sys.stderr)
    
    if is_main_branch:
        # Production release
        version_str = f"{new_version[0]}.{new_version[1]}.{new_version[2]}"
        print(f"🚀 Production version: {version_str}", file=sys.stderr)
    else:
        # Dev build - count commits since last tag
        dev_count = count_commits_since_tag(latest_tag)
        version_str = f"{new_version[0]}.{new_version[1]}.{new_version[2]}.dev{dev_count}"
        print(f"🔧 Dev version: {version_str}", file=sys.stderr)
    
    return version_str


if __name__ == "__main__":
    try:
        version = determine_version()
        print(version)
    except Exception as e:
        print(f"Error determining version: {e}", file=sys.stderr)
        sys.exit(1)