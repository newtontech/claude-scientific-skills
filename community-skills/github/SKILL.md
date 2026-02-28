---
name: github
version: 1.1.0
description: |
  全面的 GitHub 自动化工作流。
  包含 gh CLI 操作、PR 自动化、gh-issues skill 使用模式、
  Fork 管理和 upstream 同步。

author: Assistant
category: devops
dependencies:
  - gh (GitHub CLI)
  - git
  - curl
---

# GitHub 自动化技能

## 概述

本技能提供完整的 GitHub 工作流自动化，包括：

- `gh` CLI 基础操作
- PR 自动化工作流
- gh-issues skill 使用模式
- Fork 和 upstream 管理

## 基础操作

### PR 管理

```bash
# 查看 PR 列表
gh pr list --repo owner/repo

# 查看 PR 详情
gh pr view 55 --repo owner/repo

# 检查 PR 的 CI 状态
gh pr checks 55 --repo owner/repo

# 创建 PR
gh pr create --title "fix: bug fix" --body "Description"
```

### Workflow Runs

```bash
# 列出最近的工作流运行
gh run list --repo owner/repo --limit 10

# 查看运行详情
gh run view <run-id> --repo owner/repo

# 查看失败步骤的日志
gh run view <run-id> --repo owner/repo --log-failed
```

### 高级 API 查询

```bash
# 使用 gh api 访问高级功能
gh api repos/owner/repo/pulls/55 --jq '.title, .state, .user.login'

# JSON 输出配合 jq 过滤
gh issue list --repo owner/repo --json number,title --jq '.[] | "\(.number): \(.title)"'
```

## PR 自动化工作流

### 1. 批量 PR 审查

```python
async def batch_review_prs(repo: str, limit: int = 10):
    """批量审查 PR 并生成报告"""
    
    # 获取待审查的 PR 列表
    prs = exec(command=f"gh pr list --repo {repo} --limit {limit} --json number,title,author,createdAt")
    
    review_results = []
    for pr in prs:
        # 检查 CI 状态
        ci_status = exec(command=f"gh pr checks {pr['number']} --repo {repo}")
        
        # 获取 PR 详情
        details = exec(command=f"gh pr view {pr['number']} --repo {repo} --json files,additions,deletions")
        
        review_results.append({
            "number": pr['number'],
            "title": pr['title'],
            "ci_passed": "pass" in ci_status.lower(),
            "changes": details
        })
    
    return review_results
```

### 2. 自动化 PR 创建

```bash
#!/bin/bash
# create-feature-pr.sh

BRANCH_NAME="feature/$(date +%s)"
BASE_BRANCH="main"

# 创建分支
git checkout -b "$BRANCH_NAME" "$BASE_BRANCH"

# 执行修改
# ... 代码修改 ...

# 提交
git add .
git commit -m "feat: new feature"

# 推送
git push -u origin "$BRANCH_NAME"

# 创建 PR
gh pr create \
    --base "$BASE_BRANCH" \
    --title "feat: $(git log -1 --pretty=%B)" \
    --body "## Changes
- Feature implementation
- Tests added
- Documentation updated

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass" \
    --label "enhancement"
```

### 3. 自动化合并

```python
async def auto_merge_prs(repo: str, conditions: dict):
    """根据条件自动合并 PR"""
    
    # 获取可合并的 PR
    prs = exec(command=f"gh pr list --repo {repo} --json number,title,mergeStateStatus")
    
    for pr in prs:
        pr_number = pr['number']
        
        # 检查条件
        checks_pass = exec(command=f"gh pr checks {pr_number} --repo {repo}") == "pass"
        has_approval = int(exec(command=f"gh pr view {pr_number} --repo {repo} --json reviewDecision | jq '.reviews | length'")) > 0
        
        if checks_pass and has_approval:
            # 自动合并
            exec(command=f"gh pr merge {pr_number} --repo {repo} --squash --delete-branch")
            print(f"✅ 已合并 PR #{pr_number}")
```

## gh-issues Skill 使用模式

### 模式1: 单次 Issue 修复

```bash
# 处理单个 issue
/gh-issues owner/repo --limit 1 --label bug

# 自动修复，无需确认
/gh-issues owner/repo --limit 5 --yes --label bug
```

### 模式2: 持续监控模式 (--watch)

```bash
# 持续监控新 issue，每5分钟检查一次
/gh-issues owner/repo --watch --interval 5 --label bug

# 仅监控已有 PR 的 review 评论
/gh-issues owner/repo --reviews-only --watch --interval 10
```

### 模式3: Cron 定时任务

```bash
# 添加到 crontab，每小时处理一次
0 * * * * cd ~/.openclaw/workspace && openclaw /gh-issues owner/repo --cron --limit 3 --label bug

# 仅处理 review 评论
*/15 * * * * cd ~/.openclaw/workspace && openclaw /gh-issues owner/repo --cron --reviews-only
```

### 模式4: Fork 模式工作流

```bash
# 从 fork 修复上游 issue
/gh-issues upstream-owner/repo \
    --fork your-username/repo \
    --label good-first-issue \
    --limit 5

# 流程说明：
# 1. 从 upstream 获取 issues
# 2. 在 fork 上创建 fix/issue-{N} 分支
# 3. 推送分支到 fork
# 4. 向 upstream 发起 PR
```

### gh-issues 完整参数参考

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--label` | - | 按标签过滤 |
| `--limit` | 10 | 最大处理数量 |
| `--milestone` | - | 按里程碑过滤 |
| `--assignee` | - | 按负责人过滤 (@me 为自己) |
| `--fork` | - | 指定 fork 仓库 |
| `--watch` | false | 持续监控模式 |
| `--interval` | 5 | 监控间隔（分钟）|
| `--yes` | false | 自动确认，不询问 |
| `--dry-run` | false | 仅预览，不执行 |
| `--cron` | false | Cron 安全模式 |
| `--reviews-only` | false | 仅处理 review 评论 |
| `--model` | - | 指定 AI 模型 |
| `--notify-channel` | - | Telegram 通知频道 |

## Fork 和 Upstream 管理

### Fork 工作流设置

```bash
# 1. Fork 仓库（在 GitHub Web 界面完成）
# 2. 克隆 fork 到本地
git clone git@github.com:your-username/repo.git
cd repo

# 3. 添加 upstream 远程
git remote add upstream git@github.com:original-owner/repo.git

# 4. 验证远程
git remote -v
# origin    git@github.com:your-username/repo.git (fetch)
# origin    git@github.com:your-username/repo.git (push)
# upstream  git@github.com:original-owner/repo.git (fetch)
# upstream  git@github.com:original-owner/repo.git (push)
```

### Upstream 同步

```bash
#!/bin/bash
# sync-upstream.sh - 同步 upstream 变更

set -e

echo "🔄 同步 upstream 变更..."

# 保存当前分支
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# 获取 upstream 更新
git fetch upstream

# 切换到 main 分支
git checkout main

# 合并 upstream 变更
git merge upstream/main --no-edit

# 推送到自己的 fork
git push origin main

# 返回原分支
git checkout "$CURRENT_BRANCH"

echo "✅ 同步完成"
```

### 功能分支工作流

```bash
#!/bin/bash
# feature-workflow.sh

FEATURE_NAME=$1

# 1. 确保 main 分支是最新的
git checkout main
git pull upstream main
git push origin main

# 2. 创建功能分支
git checkout -b "feature/${FEATURE_NAME}"

# 3. 开发...
# ... 代码修改 ...

# 4. 提交更改
git add .
git commit -m "feat: ${FEATURE_NAME}"

# 5. 推送到 fork
git push -u origin "feature/${FEATURE_NAME}"

# 6. 创建 PR（使用 gh CLI）
gh pr create \
    --repo original-owner/repo \
    --base main \
    --head "your-username:feature/${FEATURE_NAME}" \
    --title "feat: ${FEATURE_NAME}" \
    --body "## Description
Description of changes

## Related Issues
Fixes #123"
```

### 多 Fork 管理

```bash
# 管理多个 fork
git remote add fork1 git@github.com:user1/repo.git
git remote add fork2 git@github.com:user2/repo.git

# 从特定 fork 获取
git fetch fork1

# 推送到特定 fork
git push fork1 feature-branch
```

## 完整工作流示例

### 示例1: 开源贡献工作流

```python
async def open_source_contribution(upstream: str, fork: str):
    """完整的开源贡献工作流"""
    
    # 1. 同步 upstream
    exec(command="git fetch upstream")
    exec(command="git checkout main")
    exec(command="git merge upstream/main")
    
    # 2. 查找 good-first-issue
    issues = exec(command=f"gh issue list --repo {upstream} --label good-first-issue --limit 5 --json number,title")
    
    # 3. 使用 gh-issues 自动修复
    for issue in issues[:2]:  # 选择前2个
        exec(command=f"/gh-issues {upstream} --fork {fork} --limit 1 --yes")
    
    # 4. 监控 PR 状态
    prs = exec(command=f"gh pr list --repo {upstream} --author @me --json number,state")
    return prs
```

### 示例2: 团队协作工作流

```python
async def team_collaboration(repo: str):
    """团队协作自动化"""
    
    # 1. 每日 PR 审查报告
    pending_prs = exec(command=f"gh pr list --repo {repo} --state open --json number,title,author,createdAt")
    
    report = []
    for pr in pending_prs:
        age_days = (datetime.now() - datetime.fromisoformat(pr['createdAt'])).days
        if age_days > 3:
            report.append(f"⚠️ PR #{pr['number']} 已等待 {age_days} 天")
    
    # 2. 自动提醒
    if report:
        message = "📋 PR 审查提醒\n\n" + "\n".join(report)
        send_notification(message)
    
    # 3. 合并符合条件的 PR
    await auto_merge_prs(repo, conditions={"required_approvals": 1, "ci_required": True})
```

### 示例3: 发布管理工作流

```bash
#!/bin/bash
# release-workflow.sh

VERSION=$1
REPO="owner/repo"

echo "🚀 开始发布 $VERSION"

# 1. 创建发布分支
git checkout -b "release/${VERSION}" main

# 2. 更新版本号
# ... 版本号更新逻辑 ...

# 3. 提交更改
git add .
git commit -m "chore(release): prepare ${VERSION}"

# 4. 推送分支
git push -u origin "release/${VERSION}"

# 5. 创建 Release PR
gh pr create \
    --repo "$REPO" \
    --base main \
    --head "release/${VERSION}" \
    --title "Release ${VERSION}" \
    --body "## Release Notes
- Version bump
- Changelog update" \
    --label "release"

# 6. 等待合并后创建 tag
gh release create "${VERSION}" \
    --repo "$REPO" \
    --title "Release ${VERSION}" \
    --notes "Release notes here" \
    --target main

echo "✅ 发布完成"
```

## 故障排除

### Q: 权限不足
```bash
# 检查 GH_TOKEN 或 gh auth 状态
gh auth status

# 重新认证
gh auth login

# 或者设置 GH_TOKEN
export GH_TOKEN="your-token"
```

### Q: Fork 模式下 PR 创建失败
```bash
# 确保 fork 已正确添加为远程
git remote add fork https://github.com/your-username/repo.git

# 验证令牌有权限访问 fork
gh api repos/your-username/repo --jq '.name'
```

### Q: Upstream 同步冲突
```bash
# 使用 rebase 保持历史整洁
git fetch upstream
git rebase upstream/main

# 如果有冲突，解决后
git add .
git rebase --continue
```

## 相关技能

- [gh-issues](../../openclaw-repo/skills/gh-issues/SKILL.md) - 自动化 Issue 修复和 PR 管理
- [acp-orchestrator](../acp-orchestrator/SKILL.md) - ACP 工作流编排
- [coding-agent](../coding-agent/SKILL.md) - 代码代理任务委托

---

*"Automate the boring, focus on the interesting."*
