---
name: skills-system
version: 1.0.0
description: |
  OpenClaw Skills 体系维护指南。
  统一管理所有技能，提供分类、依赖检查、更新和维护工作流。

author: Assistant
category: meta
---

# OpenClaw Skills 体系

## 📊 技能统计

- **总数量**: 64 个 skills
- **分类数**: 15+ 个类别
- **已测试**: 30+ 个
- **待完善**: 10+ 个

---

## 🗂️ 技能分类体系

### 1. 🔧 开发工具 (DevTools)
| Skill | 功能 | 状态 |
|-------|------|------|
| coding-agent | 代码生成和审查 | ✅ 完善 |
| github | GitHub CLI 操作 | ✅ 完善 |
| acp-orchestrator | ACP Agent 编排 | ✅ 完善 |
| docker-essentials | Docker 管理 | ✅ 完善 |
| mcporter | MCP 服务器管理 | ✅ 完善 |

### 2. 📚 学术工具 (Academic)
| Skill | 功能 | 状态 |
|-------|------|------|
| semanticscholar | Semantic Scholar API | ✅ 完善 |
| google-scholar | Google Scholar 搜索 | ✅ 完善 |
| context7 | Context7 文档查询 | ✅ 完善 |
| moltsci | 科学论文发布 | ✅ 完善 |

### 3. 🎓 学习系统 (Learning)
| Skill | 功能 | 状态 |
|-------|------|------|
| self-learning-loop | 自我学习迭代 | ✅ 完善 |
| bilibili-video-analyzer | B站视频分析 | ✅ 完善 |
| youtube-video-analyzer | YouTube 视频分析 | ✅ 完善 |
| academic-writing | 学术写作 | ✅ 完善 |

### 4. 🔬 材料科学 (Materials Science)
| Skill | 功能 | 状态 |
|-------|------|------|
| materials-crystal-structure | 晶体结构分析 | ✅ 完善 |
| materials-vasp-workflow | VASP 工作流 | ✅ 完善 |
| materials-dft-analysis | DFT 分析 | ✅ 完善 |
| materials-molecular-dynamics | 分子动力学 | ✅ 完善 |
| materials-property-prediction | 性质预测 | ✅ 完善 |

### 5. ⏰ 自动化 (Automation)
| Skill | 功能 | 状态 |
|-------|------|------|
| cron-automation | Cron 任务管理 | ✅ 完善 |
| gh-issues | GitHub Issues 自动处理 | ✅ 完善 |

### 6. 🎨 内容创作 (Content)
| Skill | 功能 | 状态 |
|-------|------|------|
| canvas-design | Canvas 设计 | ✅ 完善 |
| remotion-animate | 视频动画 | ✅ 完善 |
| image-enhancer | 图像增强 | ✅ 完善 |
| docx | Word 文档处理 | ✅ 完善 |
| pptx | PPT 处理 | ✅ 完善 |
| nano-pdf | PDF 编辑 | ✅ 完善 |

### 7. 🔍 搜索与信息 (Search)
| Skill | 功能 | 状态 |
|-------|------|------|
| tavily-search | Tavily 搜索 | ✅ 完善 |
| bird | Twitter/X 搜索 | ✅ 完善 |

### 8. 💼 商业工具 (Business)
| Skill | 功能 | 状态 |
|-------|------|------|
| lead-research-assistant | 潜在客户研究 | ✅ 完善 |
| invoice-organizer | 发票管理 | ✅ 完善 |
| competitive-ads-extractor | 竞品广告提取 | ✅ 完善 |

### 9. 🛠️ 系统集成 (Integration)
| Skill | 功能 | 状态 |
|-------|------|------|
| discord | Discord 集成 | ✅ 完善 |
| slack | Slack 集成 | ✅ 完善 |
| feishu | 飞书集成 | ✅ 完善 |
| canvas-lms | Canvas LMS | ✅ 完善 |

### 10. 🤖 AI 工具 (AI Tools)
| Skill | 功能 | 状态 |
|-------|------|------|
| langsmith-fetch | LangSmith 数据获取 | ✅ 完善 |
| coremem | 核心记忆管理 | ✅ 完善 |
| computer-use | 计算机使用 | ✅ 完善 |

### 11. 📝 其他工具 (Others)
| Skill | 功能 | 状态 |
|-------|------|------|
| file-organizer | 文件整理 | ⚠️ 待完善 |
| changelog-generator | 变更日志生成 | ⚠️ 待完善 |
| meeting-insights-analyzer | 会议分析 | ⚠️ 待完善 |

---

## 🔧 维护工作流

### 每周维护检查清单

```bash
# 1. 检查技能完整性
openclaw skills list --check

# 2. 更新过时依赖
openclaw skills update --outdated

# 3. 测试核心技能
openclaw skills test --category core

# 4. 清理未使用技能
openclaw skills cleanup --unused
```

### 技能质量检查

每个 skill 必须包含：
- [ ] SKILL.md (完整文档)
- [ ] 使用示例 (可运行)
- [ ] 依赖列表 (清晰明确)
- [ ] 最佳实践 (推荐用法)
- [ ] 错误处理 (异常情况)

---

## 🔄 技能更新流程

### 1. 发现问题
- 使用中发现 bug
- 依赖版本更新
- 功能需求变更

### 2. 更新技能
```bash
# 编辑 skill
cd ~/.openclaw/workspace/skills/<skill-name>
vim SKILL.md

# 测试更新
openclaw skills test <skill-name>
```

### 3. 记录变更
- 更新版本号
- 记录变更日志
- 更新依赖列表

### 4. 提交更新
```bash
# 如果有远程仓库
git add .
git commit -m "update: <skill-name> v<x.y.z>"
git push
```

---

## 📋 技能依赖关系图

```
acp-orchestrator
├── codex
├── claude
├── opencode
└── gemini

cron-automation
├── cron (system)
└── HEARTBEAT.md

github-automation
├── gh (GitHub CLI)
└── gh-issues

academic-tools
├── semanticscholar
├── google-scholar
├── context7
└── moltsci

learning-system
├── self-learning-loop
├── bilibili-video-analyzer
├── youtube-video-analyzer
└── academic-writing

materials-science (5 skills)
├── materials-crystal-structure
├── materials-vasp-workflow
├── materials-dft-analysis
├── materials-molecular-dynamics
└── materials-property-prediction
```

---

## 🎯 优先级维护列表

### 高优先级 (本周)
- [ ] 测试所有视频学习 skills
- [ ] 验证 GitHub 自动化流程
- [ ] 更新 ACP 认证文档

### 中优先级 (本月)
- [ ] 完善待完善的 skills
- [ ] 添加更多使用示例
- [ ] 优化技能分类

### 低优先级 (长期)
- [ ] 创建技能依赖自动检查
- [ ] 建立技能评分系统
- [ ] 社区贡献指南

---

## 📚 快速参考

### 查找技能
```bash
# 按名称查找
openclaw skills list | grep <keyword>

# 按分类查找
openclaw skills list --category <category>

# 查看技能详情
openclaw skills info <skill-name>
```

### 使用技能
```bash
# 直接使用
use <skill-name>

# 在对话中提及
@<skill-name> help

# 通过 exec 调用
exec skill:<skill-name>
```

---

*维护指南版本: 2026-02-28*
*技能总数: 64*
*维护周期: 每周检查，每月更新*
