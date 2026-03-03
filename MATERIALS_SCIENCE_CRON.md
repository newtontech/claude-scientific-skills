# Materials Science Skills - Cron Job Configuration

This document describes the automated cron jobs for maintaining the materials science skills collection in the claude-scientific-skills repository.

## Overview

The cron jobs perform three main tasks:
1. Check upstream repository for updates
2. Process new materials science related issues
3. Maintain existing skills (documentation updates, bug fixes)

## Cron Schedule

All times are in UTC. The schedule is designed to avoid peak hours and distribute workload.

```
# Check upstream updates
17 1 * * * cd /tmp/claude-scientific-skills && /usr/local/bin/check_upstream.sh

# Process new issues
29 2 * * * cd /tmp/claude-scientific-skills && /usr/local/bin/process_issues.sh

# Maintain existing skills
41 3 * * * cd /tmp/claude-scientific-skills && /usr/local/bin/maintain_skills.sh
```

## Job Descriptions

### 1. Check Upstream Updates (01:17 UTC)

**Script:** `check_upstream.sh`

**Purpose:**
- Fetch latest changes from upstream (K-Dense-AI/claude-scientific-skills)
- Check for changes in materials science related skills
- Create a PR if upstream has new features relevant to our skills

**Implementation:**
```bash
#!/bin/bash
set -e

REPO_DIR="/tmp/claude-scientific-skills"
UPSTREAM="https://github.com/K-Dense-AI/claude-scientific-skills.git"

cd "$REPO_DIR"

# Add upstream remote if not exists
git remote add upstream "$UPSTREAM" 2>/dev/null || true

# Fetch upstream
git fetch upstream

# Check if main branch is behind
BEHIND=$(git rev-list HEAD..upstream/main --count)

if [ "$BEHIND" -gt 0 ]; then
    echo "Upstream is $BEHIND commits ahead"
    
    # Create a branch for sync
    git checkout -b sync/upstream-$(date +%Y%m%d)
    
    # Merge upstream changes
    git merge upstream/main --no-edit
    
    # Push to fork
    git push origin sync/upstream-$(date +%Y%m%d)
    
    # Create PR using gh CLI
    gh pr create \
        --repo newtontech/claude-scientific-skills \
        --title "Sync with upstream - $(date +%Y-%m-%d)" \
        --body "Automated sync with upstream repository. $BEHIND new commits." \
        --base main \
        --head sync/upstream-$(date +%Y%m%d) || true
    
    echo "Created sync PR"
else
    echo "Already up to date with upstream"
fi
```

### 2. Process New Issues (02:29 UTC)

**Script:** `process_issues.sh`

**Purpose:**
- Check upstream repository for new issues labeled "materials-science"
- Automatically generate new skills based on feature requests
- Create PRs with generated skills

**Implementation:**
```bash
#!/bin/bash
set -e

REPO_DIR="/tmp/claude-scientific-skills"
ISSUES_FILE="/tmp/materials_issues.json"

# Fetch issues with materials-science label
gh issue list \
    --repo K-Dense-AI/claude-scientific-skills \
    --label "materials-science" \
    --state open \
    --json number,title,body \
    > "$ISSUES_FILE"

# Process each issue
jq -c '.[]' "$ISSUES_FILE" | while read issue; do
    NUMBER=$(echo "$issue" | jq -r '.number')
    TITLE=$(echo "$issue" | jq -r '.title')
    BODY=$(echo "$issue" | jq -r '.body')
    
    echo "Processing issue #$NUMBER: $TITLE"
    
    # Check if already processed
    if [ -f "$REPO_DIR/.processed_issues/$NUMBER" ]; then
        echo "Issue #$NUMBER already processed, skipping"
        continue
    fi
    
    # Generate skill name from title
    SKILL_NAME=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | sed 's/[^a-z0-9-]//g')
    SKILL_DIR="$REPO_DIR/scientific-skills/materials-science/materials-$SKILL_NAME"
    
    # Create skill directory
    mkdir -p "$SKILL_DIR"
    
    # Generate skill content (this would use an AI agent in practice)
    # For now, create a template
    cat > "$SKILL_DIR/SKILL.md" << 'EOF'
---
name: materials-PLACEHOLDER
description: Auto-generated skill from issue #NUMBER - TITLE
homepage: https://materialsproject.org
metadata: {"clawdbot":{"emoji":"🔬","requires":{"bins":["python3"]}}}
---

# Materials SKILL_NAME

Auto-generated skill addressing issue #NUMBER.

## Description

BODY

## Implementation

[To be implemented based on issue requirements]

EOF
    
    # Replace placeholders
    sed -i "s/PLACEHOLDER/$SKILL_NAME/g" "$SKILL_DIR/SKILL.md"
    sed -i "s/NUMBER/$NUMBER/g" "$SKILL_DIR/SKILL.md"
    sed -i "s/TITLE/$TITLE/g" "$SKILL_DIR/SKILL.md"
    sed -i "s/BODY/$BODY/g" "$SKILL_DIR/SKILL.md"
    
    # Commit and push
    cd "$REPO_DIR"
    git checkout -b "feature/materials-$SKILL_NAME"
    git add "$SKILL_DIR"
    git commit -m "Add skill: materials-$SKILL_NAME - Auto-generated from issue #$NUMBER"
    git push origin "feature/materials-$SKILL_NAME"
    
    # Create PR
    gh pr create \
        --repo newtontech/claude-scientific-skills \
        --title "Add skill: materials-$SKILL_NAME" \
        --body "Resolves upstream issue #$NUMBER\n\nAuto-generated skill based on:\n$TITLE\n\n$BODY" \
        --base main \
        --head "feature/materials-$SKILL_NAME"
    
    # Mark as processed
    mkdir -p "$REPO_DIR/.processed_issues"
    echo "$(date -Iseconds)" > "$REPO_DIR/.processed_issues/$NUMBER"
    
    echo "Created PR for issue #$NUMBER"
done

rm -f "$ISSUES_FILE"
```

### 3. Maintain Existing Skills (03:41 UTC)

**Script:** `maintain_skills.sh`

**Purpose:**
- Check for outdated documentation
- Update skill files based on package version changes
- Fix reported issues in existing skills

**Implementation:**
```bash
#!/bin/bash
set -e

REPO_DIR="/tmp/claude-scientific-skills"
SKILLS_DIR="$REPO_DIR/scientific-skills/materials-science"

MAINTENANCE_BRANCH="maintenance/$(date +%Y%m%d)"

# Create maintenance branch
cd "$REPO_DIR"
git checkout main
git pull origin main
git checkout -b "$MAINTENANCE_BRANCH"

UPDATES_MADE=0

# Function to check if skill needs update
needs_update() {
    local skill_file=$1
    local last_modified=$(stat -c %Y "$skill_file")
    local days_since_update=$(( ($(date +%s) - last_modified) / 86400 ))
    
    if [ $days_since_update -gt 30 ]; then
        return 0  # Needs update
    fi
    return 1  # Up to date
}

# Check each skill
for skill_dir in "$SKILLS_DIR"/materials-*/; do
    if [ -d "$skill_dir" ]; then
        skill_name=$(basename "$skill_dir")
        skill_file="$skill_dir/SKILL.md"
        
        echo "Checking $skill_name..."
        
        if needs_update "$skill_file"; then
            echo "  -> Needs maintenance"
            
            # Add maintenance note
            echo "" >> "$skill_file"
            echo "## Last Updated" >> "$skill_file"
            echo "- Maintenance check: $(date -Iseconds)" >> "$skill_file"
            
            UPDATES_MADE=$((UPDATES_MADE + 1))
        fi
    fi
done

# If updates were made, commit and push
if [ $UPDATES_MADE -gt 0 ]; then
    git add "$SKILLS_DIR"
    git commit -m "Maintenance: Update $UPDATES_MADE materials science skills"
    git push origin "$MAINTENANCE_BRANCH"
    
    # Create PR
    gh pr create \
        --repo newtontech/claude-scientific-skills \
        --title "Maintenance: Routine skill updates - $(date +%Y-%m-%d)" \
        --body "Automated maintenance update:\n- Checked $(ls -d "$SKILLS_DIR"/materials-*/ | wc -l) skills\n- Updated $UPDATES_MADE skills\n- Routine documentation refresh" \
        --base main \
        --head "$MAINTENANCE_BRANCH"
    
    echo "Created maintenance PR with $UPDATES_MADE updates"
else
    echo "No maintenance needed"
    git checkout main
    git branch -D "$MAINTENANCE_BRANCH"
fi
```

## Environment Setup

Create the necessary directories and configuration:

```bash
# Create directories
mkdir -p /tmp/claude-scientific-skills
mkdir -p /tmp/materials_issues
mkdir -p ~/.processed_issues

# Set up git config for automation
git config --global user.name "Materials Science Bot"
git config --global user.email "bot@materials-science.local"

# Ensure gh CLI is authenticated
echo $GITHUB_TOKEN | gh auth login --with-token
```

## Monitoring and Logging

All scripts log to `/var/log/materials-skills/`:

```bash
# Log rotation configuration
/etc/logrotate.d/materials-skills:
/var/log/materials-skills/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

View logs:
```bash
tail -f /var/log/materials-skills/upstream-check.log
tail -f /var/log/materials-skills/issue-processing.log
tail -f /var/log/materials-skills/maintenance.log
```

## Manual Execution

To run any job manually:

```bash
# Check upstream
bash /usr/local/bin/check_upstream.sh

# Process issues
bash /usr/local/bin/process_issues.sh

# Maintain skills
bash /usr/local/bin/maintain_skills.sh
```

## Troubleshooting

### Common Issues

1. **Git authentication failed**
   - Check `gh auth status`
   - Re-authenticate: `gh auth login`

2. **Rate limiting**
   - Add delay between API calls
   - Use authenticated requests for higher limits

3. **Merge conflicts**
   - Manually resolve conflicts
   - Re-run sync script

### Health Check

```bash
# Verify all components
which gh && gh --version
which git && git --version
which jq && jq --version
test -d /tmp/claude-scientific-skills && echo "Repo exists"
```

## Security Considerations

- Store `GITHUB_TOKEN` securely (use environment variables, not hardcoded)
- Limit token permissions to required scopes only
- Use branch protection rules on main branch
- Review auto-generated PRs before merging

## Future Enhancements

1. **AI-Powered Skill Generation**
   - Use Claude/Codex to generate skill content from issues
   - Auto-update documentation based on package releases

2. **Testing Pipeline**
   - Add automated tests for generated skills
   - Validate skill format compliance

3. **Metrics Dashboard**
   - Track skill usage statistics
   - Monitor PR merge rates

## Contact

For issues with the cron jobs, contact the repository maintainer.
