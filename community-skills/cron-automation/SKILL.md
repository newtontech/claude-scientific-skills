---
name: cron-automation
version: 1.0.0
description: |
  Cron Jobs 自动化管理系统。
  管理 OpenClaw 的定时任务，包括 HEARTBEAT.md 格式、
  任务监控、日志管理和自动恢复机制。

author: Assistant
category: automation
dependencies:
  - cron (system package)
  - crontab
---

# Cron Jobs 自动化管理

## 概述

本技能提供完整的 Cron Jobs 管理体系，包括：

- 8 个定时任务的统一管理
- HEARTBEAT.md 任务配置格式
- 任务监控和日志收集
- 自动故障恢复机制

## 当前任务列表

| 任务名称 | 执行时间 | 功能描述 | 日志位置 |
|----------|----------|----------|----------|
| **Morning Brief** | 每天 8:17 | 生成晨间简报 | `~/.openclaw/logs/morning-brief.log` |
| **Dynamic Dashboard** | 每15分钟 (7,22,37,52) | 更新动态仪表板 | `~/.openclaw/logs/dashboard.log` |
| **Self-Healing Server** | 每15分钟 (8,23,38,53) | 服务器健康检查 | `~/.openclaw/logs/health-check.log` |
| **YouTube Digest** | 每天 9:13 | YouTube 视频摘要 | `~/.openclaw/logs/youtube-digest.log` |
| **Tech News Digest** | 每天 8:23, 20:23 | 科技新闻汇总 | `~/.openclaw/logs/tech-news.log` |
| **Second Brain Sync** | 每小时 47 分 | 第二大脑同步 | `~/.openclaw/logs/second-brain.log` |
| **AI Earnings Tracker** | 每周一 9:17 | AI 收益追踪 | `~/.openclaw/logs/earnings.log` |
| **GitHub Stars Explorer** | 每天 3:17 | GitHub Stars 增长探索 | `~/.openclaw/workspace/logs/github_stars_explorer.log` |

## HEARTBEAT.md 格式

HEARTBEAT.md 是 OpenClaw 的心跳任务配置文件，用于定义周期性检查任务。

### 文件位置
```
~/.openclaw/workspace/HEARTBEAT.md
```

### 基本结构

```markdown
# HEARTBEAT.md

# 保持文件为空或仅包含注释以跳过心跳 API 调用

## 任务名称
- **Schedule**: Cron 表达式 (如 "0 */4 * * *")
- **Command**: 执行的命令或脚本
- **Timeout**: 超时时间（秒）
- **Retry**: 失败重试次数
- **Notify**: 失败通知渠道
```

### 任务配置示例

```markdown
# HEARTBEAT.md

## Daily Health Check
- **Schedule**: "0 */4 * * *"  # 每4小时
- **Command**: ~/.openclaw/scripts/health-check.sh
- **Timeout**: 300
- **Retry**: 3
- **Notify**: telegram:@yhm_bot

## Weekly Report
- **Schedule**: "0 9 * * 0"  # 每周日9点
- **Command**: python3 ~/.openclaw/scripts/weekly_report.py
- **Timeout**: 600
- **Retry**: 2
- **Notify**: feishu:group_id
```

## Cron 配置管理

### 查看当前 Cron 任务

```bash
# 列出所有定时任务
crontab -l

# 查看特定任务的下次执行时间
crontab -l | grep "morning-brief"
```

### 添加新任务

```bash
# 方法1: 直接编辑 crontab
crontab -e

# 方法2: 使用脚本添加
echo "17 8 * * * /path/to/script.sh" | crontab -
```

### 任务时间设计原则

**避开整点规则：**
- 所有任务分钟不为 `00`
- 分散在 17, 23, 37, 47, 52, 53 等时间点
- 避免系统负载高峰

```bash
# ❌ 不推荐 - 整点执行
0 8 * * * /task.sh

# ✅ 推荐 - 错开时间
17 8 * * * /task.sh
23 8 * * * /another-task.sh
```

## 任务监控

### 实时监控

```bash
# 查看最近的 cron 日志
tail -f /var/log/syslog | grep CRON

# 查看特定任务的日志
tail -f ~/.openclaw/logs/morning-brief.log
```

### 健康检查脚本

```bash
#!/bin/bash
# check-cron-health.sh - 检查 cron 任务健康状态

LOG_DIR="~/.openclaw/logs"
ALERT_THRESHOLD=3600  # 1小时无更新视为异常

check_task() {
    local task_name=$1
    local log_file=$2
    
    if [ ! -f "$log_file" ]; then
        echo "❌ $task_name: 日志文件不存在"
        return 1
    fi
    
    last_update=$(stat -c %Y "$log_file")
    current_time=$(date +%s)
    diff=$((current_time - last_update))
    
    if [ $diff -gt $ALERT_THRESHOLD ]; then
        echo "⚠️  $task_name: 超过1小时未更新"
        return 1
    else
        echo "✅ $task_name: 正常运行"
        return 0
    fi
}

# 检查所有任务
check_task "Morning Brief" "$LOG_DIR/morning-brief.log"
check_task "Dashboard" "$LOG_DIR/dashboard.log"
check_task "Health Check" "$LOG_DIR/health-check.log"
```

### 自动恢复机制

```bash
#!/bin/bash
# auto-restore.sh - 自动恢复失败的 cron 任务

restart_if_needed() {
    local service=$1
    local check_command=$2
    local restart_command=$3
    
    if ! eval "$check_command" > /dev/null 2>&1; then
        echo "$(date): $service 异常，执行恢复..."
        eval "$restart_command"
        echo "$(date): $service 已恢复"
    fi
}

# 检查并恢复关键服务
restart_if_needed "cron" "pgrep cron" "sudo service cron restart"
```

## 日志管理

### 日志轮转配置

```bash
# ~/.openclaw/config/logrotate.conf
~/.openclaw/logs/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
    create 644 yhm yhm
}
```

### 日志分析

```python
#!/usr/bin/env python3
# analyze-cron-logs.py

import os
import re
from datetime import datetime, timedelta
from collections import defaultdict

LOG_DIR = os.path.expanduser("~/.openclaw/logs")

def analyze_logs():
    """分析 cron 任务执行统计"""
    stats = defaultdict(lambda: {"success": 0, "error": 0, "total_time": 0})
    
    for filename in os.listdir(LOG_DIR):
        if filename.endswith('.log'):
            task_name = filename.replace('.log', '')
            filepath = os.path.join(LOG_DIR, filename)
            
            with open(filepath, 'r') as f:
                content = f.read()
                
            # 统计成功/失败
            stats[task_name]["success"] = len(re.findall(r'✅|success|completed', content))
            stats[task_name]["error"] = len(re.findall(r'❌|error|failed', content))
    
    # 输出报告
    print("📊 Cron 任务执行统计")
    print("-" * 50)
    for task, data in stats.items():
        total = data["success"] + data["error"]
        success_rate = (data["success"] / total * 100) if total > 0 else 0
        print(f"{task:20} | ✅ {data['success']:3} | ❌ {data['error']:3} | {success_rate:5.1f}%")

if __name__ == "__main__":
    analyze_logs()
```

## 最佳实践

### 1. 任务设计原则

```bash
# ✅ 好的做法
- 每个任务做一件事
- 设置合理的超时时间
- 记录详细的日志
- 失败时发送通知

# ❌ 避免的做法
- 一个任务做太多事
- 无限制的运行时间
- 忽略错误处理
- 静默失败
```

### 2. 脚本模板

```bash
#!/bin/bash
# template-cron-task.sh

# 配置
TASK_NAME="my-task"
LOG_FILE="$HOME/.openclaw/logs/${TASK_NAME}.log"
LOCK_FILE="/tmp/${TASK_NAME}.lock"
TIMEOUT=300

# 防止重复执行
if [ -f "$LOCK_FILE" ]; then
    echo "$(date): 任务正在运行，跳过" >> "$LOG_FILE"
    exit 0
fi

touch "$LOCK_FILE"
trap "rm -f $LOCK_FILE" EXIT

# 记录开始
echo "$(date '+%Y-%m-%d %H:%M:%S'): 任务开始" >> "$LOG_FILE"

# 设置超时
timeout $TIMEOUT bash << 'EOF'
    # 任务逻辑在这里
    echo "执行具体任务..."
    
    # 检查结果
    if [ $? -eq 0 ]; then
        echo "✅ 任务成功完成"
    else
        echo "❌ 任务失败"
        exit 1
    fi
EOF >> "$LOG_FILE" 2>&1

# 记录结束
echo "$(date '+%Y-%m-%d %H:%M:%S'): 任务结束" >> "$LOG_FILE"
```

### 3. 错误通知

```bash
# notify-on-error.sh

notify_error() {
    local task=$1
    local error_msg=$2
    
    # Telegram 通知
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d "chat_id=${TELEGRAM_CHAT_ID}" \
        -d "text=❌ Cron 任务失败: ${task}%0A${error_msg}"
    
    # 飞书通知 (可选)
    # curl -s -X POST "${FEISHU_WEBHOOK}" \
    #     -H "Content-Type: application/json" \
    #     -d "{\"msg_type\":\"text\",\"content\":{\"text\":\"任务失败: ${task}\"}}"
}
```

## 常见问题

### Q: Cron 任务不执行
```bash
# 检查1: cron 服务是否运行
sudo service cron status

# 检查2: 环境变量
# cron 的环境变量与 shell 不同，需要显式设置
# 在 crontab 顶部添加：
PATH=/usr/local/bin:/usr/bin:/bin
HOME=/home/yhm

# 检查3: 权限
chmod +x /path/to/script.sh
```

### Q: 日志不写入
```bash
# 确保日志目录存在
mkdir -p ~/.openclaw/logs

# 使用绝对路径
# ❌ 错误
crontab: * * * * * ./script.sh > logs/out.log

# ✅ 正确
crontab: * * * * * /home/yhm/.openclaw/scripts/script.sh >> /home/yhm/.openclaw/logs/out.log 2>&1
```

### Q: 任务执行时间漂移
```bash
# 使用 anacron 处理每天/每周任务（系统启动后执行）
# 或者使用 systemd timer 替代 cron
```

## 高级功能

### 动态任务调度

```python
#!/usr/bin/env python3
# dynamic-scheduler.py

import json
from datetime import datetime, timedelta

class DynamicScheduler:
    def __init__(self):
        self.tasks_file = "~/.openclaw/config/dynamic-tasks.json"
    
    def add_task(self, name: str, command: str, schedule: str):
        """动态添加定时任务"""
        task = {
            "name": name,
            "command": command,
            "schedule": schedule,
            "created_at": datetime.now().isoformat(),
            "enabled": True
        }
        # 保存到 JSON 并更新 crontab
        pass
    
    def pause_task(self, name: str):
        """暂停任务（注释掉 crontab 中的条目）"""
        pass
    
    def resume_task(self, name: str):
        """恢复任务"""
        pass

if __name__ == "__main__":
    scheduler = DynamicScheduler()
    # scheduler.add_task("test", "echo hello", "*/5 * * * *")
```

### 任务依赖管理

```yaml
# task-dependencies.yaml
tasks:
  - name: "fetch-data"
    command: "fetch_data.sh"
    schedule: "0 */4 * * *"
    
  - name: "process-data"
    command: "process_data.sh"
    depends_on: ["fetch-data"]
    schedule: "10 */4 * * *"  # fetch 后 10 分钟执行
    
  - name: "generate-report"
    command: "generate_report.sh"
    depends_on: ["process-data"]
    schedule: "20 */4 * * *"  # process 后 10 分钟执行
```

## 相关技能

- [self-learning-loop](../self-learning-loop/SKILL.md) - 自我学习迭代系统
- [acp-orchestrator](../acp-orchestrator/SKILL.md) - ACP 工作流编排
- [github](../github/SKILL.md) - GitHub 自动化

---

*"Automate everything that can be automated."*
