---
name: acp-orchestrator
version: 1.0.0
description: |
  ACP (Agent Control Protocol) 工作流编排器。
  统一管理 codex、claude、opencode、gemini 等 AI 编程工具的使用模式、
  会话管理和自动批准策略。

author: Assistant
category: orchestration
dependencies:
  - acpx (npm install -g acpx)
  - codex (npm install -g codex)
  - claude (pip install claude-code)
  - opencode (optional)
  - gemini (optional)
---

# ACP 工作流编排器

## 概述

ACP (Agent Control Protocol) 是 OpenClaw 用于连接远程 AI Agent 的协议。
本技能提供统一的 ACP 工作流管理，包括：

- 多 Agent 选择 (codex / claude / opencode / gemini)
- 执行模式 vs 会话模式
- 自动批准策略配置
- 会话生命周期管理

## 快速开始

### 1. 基础使用

```bash
# 使用默认 Agent (codex) 执行单次任务
acpx codex exec "分析当前目录的代码结构"

# 使用 Claude
acpx claude exec "优化数据库查询"

# 使用 OpenCode
acpx opencode exec "重构 auth 模块"
```

### 2. OpenClaw 集成

```python
# 使用 exec 运行 ACP 任务
exec command:"acpx codex exec 'fix the bug'" workdir:~/project

# 使用会话模式保持上下文
exec command:"acpx codex -s myproject 'refactor utils'" workdir:~/project
```

## 执行模式详解

### Exec 模式 (单次执行)

适合一次性任务，执行完后立即退出。

```bash
# 基础用法
acpx codex exec "summarize this repo"

# 指定工作目录
acpx codex exec --cwd /path/to/project "analyze code"

# 结合 OpenClaw exec
exec command:"acpx codex exec 'list files'" workdir:~/project
```

**优点：**
- 快速启动，执行完立即退出
- 无会话残留
- 适合 CI/CD 场景

**缺点：**
- 每次执行都是新上下文
- 无法保持历史记录

### Session 模式 (持久会话)

适合需要多轮交互的复杂任务。

```bash
# 创建命名会话
acpx codex -s backend "设计 API 接口"

# 继续使用同一会话
acpx codex -s backend "实现用户认证"
acpx codex -s backend "添加单元测试"

# 查看所有会话
acpx codex sessions

# 删除会话
acpx codex sessions delete backend
```

**优点：**
- 保持上下文和历史记录
- 适合长时间迭代开发
- 可查看会话历史

**缺点：**
- 需要手动管理会话生命周期
- 占用资源直到会话超时

## 自动批准策略

### 策略级别

| 策略 | 命令 | 说明 |
|------|------|------|
| **deny-all** | `--deny-all` | 预览模式，只显示会做什么但不执行 |
| **default** | (无参数) | 每次操作都询问确认 |
| **approve-reads** | `--approve-reads` | 自动批准读取操作，写入仍询问 |
| **approve-all** | `--approve-all` | 自动批准所有操作（谨慎使用） |

### 使用建议

```bash
# 1. 首次探索代码库 - 使用 deny-all 预览
acpx codex --deny-all "重构 auth 模块"

# 2. 日常开发 - 使用 approve-reads 提高效率
acpx codex --approve-reads "添加新功能"

# 3. 可信任务 - 使用 approve-all 完全自动化
acpx codex --approve-all "格式化代码"

# 4. 重要变更 - 使用默认模式仔细确认
acpx codex "修改生产配置"
```

### OpenClaw 中的最佳实践

```python
# 安全级别：只读分析
exec command:"acpx codex --approve-reads 'analyze codebase'" workdir:~/project

# 标准级别：自动读取，写入确认
exec command:"acpx codex --approve-reads 'implement feature'" workdir:~/project

# 快速级别：完全自动（仅用于可信任务）
exec command:"acpx codex --approve-all 'run tests'" workdir:~/project
```

## 多 Agent 支持

### Agent 对比

| Agent | 安装命令 | 特点 | 适用场景 |
|-------|----------|------|----------|
| **codex** | `npm install -g codex` | OpenAI 出品，响应快 | 快速原型、代码生成 |
| **claude** | `pip install claude-code` | Anthropic 出品，推理强 | 复杂分析、架构设计 |
| **opencode** | `npm install -g opencode` | 开源替代 | 本地优先、隐私敏感 |
| **gemini** | (内置) | Google 出品 | 长上下文、多语言 |

### Agent 切换

```bash
# 设置默认 Agent
acpx config init
# 按提示选择默认 Agent

# 临时切换 Agent
acpx claude exec "task"    # 使用 Claude
acpx codex exec "task"     # 使用 Codex
acpx gemini exec "task"    # 使用 Gemini
```

### 配置检查

```bash
# 查看当前配置
acpx config show

# 典型输出：
# {
#   "defaultAgent": "codex",
#   "defaultPermissions": "approve-reads",
#   "ttl": 300,
#   "timeout": null,
#   "format": "text"
# }
```

## 会话管理

### 会话操作

```bash
# 创建新会话
acpx codex sessions new myproject

# 列出所有会话
acpx codex sessions

# 使用指定会话
acpx codex -s myproject "continue working"

# 删除会话
acpx codex sessions delete myproject

# 清理所有过期会话
acpx codex sessions cleanup
```

### 会话生命周期

```
创建会话 -> 执行任务 -> 保持活跃 -> 超时回收
    ↑                                    |
    └──────── 再次使用继续任务 ────────────┘
```

默认 TTL: 300 秒 (5分钟)
可使用 `--ttl 0` 保持永久在线

## 高级用法

### 批量任务处理

```python
# 批量处理多个项目的相同任务
projects = ["~/project-a", "~/project-b", "~/project-c"]

for project in projects:
    exec(
        command="acpx codex --approve-reads 'run linting'",
        workdir=project
    )
```

### 错误处理模式

```bash
# 设置超时防止无限等待
acpx codex --timeout 300 "complex task"

# 非交互模式（JSON 输出）
acpx codex --format json --json-strict "analyze and report"

# 取消正在运行的任务
acpx codex cancel
```

### 与 Sub-agents 结合

```python
# 在 sub-agent 中使用 ACP
sessions_spawn(
    task="""
    Use acpx to analyze this codebase:
    1. Run: acpx codex --approve-reads exec 'list all Python files'
    2. Run: acpx codex --approve-reads exec 'find security issues'
    3. Generate report
    """,
    runtime="subagent"
)
```

## 常见问题

### Q: Claude Code 需要认证
```bash
# 首次使用 Claude 需要先登录
claude login
# 按提示在浏览器完成认证

# 然后才能使用
acpx claude exec "analyze code"
```

### Q: 参数传递问题
```bash
# ❌ acpx claude exec 不支持 --cwd 参数
acpx claude exec --cwd ~/project "task"  # 会报错

# ✅ 使用 cd 切换目录
acpx claude exec "cd ~/project && task"

# ✅ 在 OpenClaw 中使用 workdir
exec command:"acpx claude exec 'task'" workdir:~/project
```

### Q: 会话模式超时
```bash
# 延长会话存活时间
acpx codex --ttl 3600 -s longtask "complex analysis"

# 或使用 --no-wait 模式
acpx codex --no-wait "background task"
```

## 完整工作流示例

### 示例1: 代码审查工作流

```python
async def code_review_workflow(repo_path: str):
    """使用 ACP 进行自动化代码审查"""
    
    # 步骤1: 静态分析
    exec(
        command="acpx codex --approve-reads exec 'find code smells'",
        workdir=repo_path
    )
    
    # 步骤2: 安全扫描
    exec(
        command="acpx codex --approve-reads exec 'check for security issues'",
        workdir=repo_path
    )
    
    # 步骤3: 生成审查报告
    exec(
        command="acpx codex --approve-reads exec 'generate review report'",
        workdir=repo_path
    )
```

### 示例2: 多 Agent 协作

```python
async def multi_agent_collaboration(project: str):
    """多个 Agent 协作完成复杂任务"""
    
    # Claude 负责架构设计
    exec(command="acpx claude --approve-reads exec 'design system architecture'", workdir=project)
    
    # Codex 负责快速实现
    exec(command="acpx codex --approve-all exec 'implement the API layer'", workdir=project)
    
    # Gemini 负责文档生成
    exec(command="acpx gemini --approve-reads exec 'write API documentation'", workdir=project)
```

### 示例3: 自动化修复工作流

```python
async def auto_fix_workflow(repo_path: str, issue_description: str):
    """自动化修复 GitHub Issue"""
    
    # 使用会话模式保持上下文
    session_name = f"fix-{int(time.time())}"
    
    # 分析问题
    exec(command=f"acpx codex -s {session_name} --approve-reads 'analyze issue: {issue_description}'", workdir=repo_path)
    
    # 实现修复
    exec(command=f"acpx codex -s {session_name} --approve-reads 'implement fix'", workdir=repo_path)
    
    # 运行测试
    exec(command=f"acpx codex -s {session_name} --approve-all 'run tests'", workdir=repo_path)
    
    # 清理会话
    exec(command=f"acpx codex sessions delete {session_name}")
```

## 配置参考

### 配置文件位置
```
~/.acpx/config.json
```

### 完整配置示例
```json
{
  "defaultAgent": "codex",
  "defaultPermissions": "approve-reads",
  "nonInteractivePermissions": "deny",
  "authPolicy": "skip",
  "ttl": 300,
  "timeout": null,
  "format": "text"
}
```

## 相关技能

- [coding-agent](../coding-agent/SKILL.md) - 代码代理任务委托
- [github](../github/SKILL.md) - GitHub CLI 操作
- [gh-issues](../gh-issues/SKILL.md) - 自动化 Issue 修复

---

*"The best agent is the one that knows when to ask for help."*
