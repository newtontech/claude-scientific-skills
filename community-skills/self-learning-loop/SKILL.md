---
name: self-learning-loop
version: 2.0.0
description: |
  长期自我学习迭代系统 (Self-Learning Loop) v2.0。
  每日/每周/每月循环，视频学习内容自动转换为技能，
  持续改进和扩展能力。

author: Assistant
category: meta
created: 2026-02-28
updated: 2026-02-28
---

# 自我学习迭代系统 v2.0

## 核心理念

通过持续迭代，实现：
1. 🎯 **技能积累** - 自动学习并创建新技能
2. 📺 **视频学习** - 分析视频内容，提取知识
3. 🔄 **自我改进** - 基于反馈优化自身行为
4. 📈 **能力扩展** - 不断扩大可处理的任务范围

## 学习循环架构

```
┌─────────────────────────────────────────────────────────┐
│                    自我学习循环                           │
├─────────────────────────────────────────────────────────┤
│  1. 发现 (Discover)                                      │
│     └─> 扫描新领域、视频、问题                           │
│                                                         │
│  2. 学习 (Learn)                                         │
│     └─> 分析内容、提取知识、理解模式                     │
│                                                         │
│  3. 创建 (Create)                                        │
│     └─> 生成技能、文档、解决方案                         │
│                                                         │
│  4. 验证 (Validate)                                      │
│     └─> 测试、获取反馈、评估效果                         │
│                                                         │
│  5. 迭代 (Iterate)                                       │
│     └─> 改进、优化、扩展                                 │
└─────────────────────────────────────────────────────────┘
```

## 时间分层循环

### 每日循环 (Daily Loop) - 每 4 小时

```yaml
schedule: "0 */4 * * *"

tasks:
  # 1. 视频学习
  - name: "daily-video-learning"
    description: "分析新的学习机会，处理待学习的视频"
    max_videos: 5
    sources:
      - youtube_subscriptions
      - bilibili_feed
      - curated_playlists
    
  # 2. 技能创建
  - name: "skill-extraction"
    description: "从学习内容中提取并创建新技能"
    min_quality_score: 0.7
    
  # 3. 日志记录
  - name: "learning-log"
    description: "记录学习进度和成果"
    output: "memory/YYYY-MM-DD.md"
```

**每日执行脚本：**

```python
#!/usr/bin/env python3
# daily-loop.py

import asyncio
from datetime import datetime
from skills.video_learning import VideoLearner
from skills.skill_creator import SkillCreator

async def daily_loop():
    """每日学习循环"""
    print(f"🔄 启动每日学习循环 - {datetime.now()}")
    
    # 1. 发现视频
    learner = VideoLearner()
    candidates = await discover_learning_candidates()
    
    # 2. 批量分析
    for video in candidates[:5]:
        result = await learner.analyze(video['url'])
        
        # 3. 评估并提取技能
        if should_extract_skill(result):
            skill = await SkillCreator.from_video(result)
            print(f"✅ 创建技能: {skill.name}")
        
        # 4. 记录学习
        log_learning(video, result)
    
    # 5. 生成日报
    report = generate_daily_report()
    save_to_memory(report)

if __name__ == "__main__":
    asyncio.run(daily_loop())
```

### 每周循环 (Weekly Loop) - 每周日 9:00

```yaml
schedule: "0 9 * * 0"

tasks:
  # 1. 学习成果分析
  - name: "weekly-review"
    description: "分析本周学习成果"
    analysis:
      - videos_learned
      - skills_created
      - knowledge_areas_expanded
      
  # 2. 技能审计
  - name: "skill-audit"
    description: "审计技能有效性和质量"
    actions:
      - test_skill_examples
      - check_skill_coverage
      - identify_gaps
      
  # 3. 知识图谱更新
  - name: "knowledge-graph-update"
    description: "更新知识图谱"
    
  # 4. 下周计划
  - name: "next-week-planning"
    description: "制定下周学习计划"
```

**每周执行脚本：**

```python
#!/usr/bin/env python3
# weekly-loop.py

async def weekly_loop():
    """每周学习循环"""
    print(f"📊 启动每周复盘 - Week {datetime.now().isocalendar()[1]}")
    
    # 1. 统计本周数据
    stats = {
        'videos_analyzed': count_videos_this_week(),
        'skills_created': count_skills_this_week(),
        'learning_hours': calculate_learning_time(),
        'topics_covered': get_topics_covered()
    }
    
    # 2. 技能审计
    skills_audit = await audit_all_skills()
    
    # 3. 识别改进点
    gaps = identify_knowledge_gaps()
    
    # 4. 生成周报
    report = generate_weekly_report(stats, skills_audit, gaps)
    
    # 5. 制定下周计划
    next_week_plan = create_learning_plan(gaps)
    
    # 6. 保存报告
    save_weekly_report(report, next_week_plan)
```

### 每月循环 (Monthly Loop) - 每月 1 日 10:00

```yaml
schedule: "0 10 1 * *"

tasks:
  # 1. 深度技能审计
  - name: "monthly-skill-deep-audit"
    description: "深度审计所有技能"
    
  # 2. 架构优化
  - name: "architecture-optimization"
    description: "优化技能架构"
    
  # 3. 新领域探索
  - name: "new-domain-exploration"
    description: "探索新的知识领域"
    
  # 4. 长期目标调整
  - name: "long-term-goals"
    description: "评估和调整长期目标"
```

**每月执行脚本：**

```python
#!/usr/bin/env python3
# monthly-loop.py

async def monthly_loop():
    """每月学习循环"""
    print(f"🌙 启动月度进化 - {datetime.now().strftime('%Y-%m')}")
    
    # 1. 生成月度统计
    monthly_stats = generate_monthly_statistics()
    
    # 2. 技能体系评估
    skill_ecosystem = evaluate_skill_ecosystem()
    
    # 3. 识别新领域
    new_domains = await explore_new_domains()
    
    # 4. 更新长期目标
    update_long_term_goals(monthly_stats, new_domains)
    
    # 5. 生成月报
    save_monthly_report(monthly_stats, skill_ecosystem, new_domains)
```

## 视频 → 技能 转换流程

### 转换流程图

```
┌─────────────────────────────────────────────────────────────┐
│                    视频 → 技能 转换流程                       │
└─────────────────────────────────────────────────────────────┘

  输入: 视频 URL
       │
       ▼
  ┌─────────────┐
  │ 1. 内容提取  │  ← 字幕、元数据、章节
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │ 2. AI 分析   │  ← 知识点提取、结构分析
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │ 3. 质量评估  │  ← 是否值得创建技能
  └──────┬──────┘
         │
    ┌────┴────┐
    │ 质量≥0.7 │
    └────┬────┘
         │ Yes
         ▼
  ┌─────────────┐
  │ 4. 技能设计  │  ← 命令、示例、最佳实践
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │ 5. SKILL.md  │  ← 生成技能文档
  │   生成      │
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │ 6. 测试验证  │  ← 验证示例可运行
  └──────┬──────┘
         │
    ┌────┴────┐
    │ 测试通过 │
    └────┬────┘
         │ Yes
         ▼
  ┌─────────────┐
  │ 7. 技能部署  │  ← 保存到 skills/ 目录
  └──────┬──────┘
         │
         ▼
  输出: 可用的新技能
```

### 自动技能创建实现

```python
class SkillFromVideo:
    """从视频自动创建技能"""
    
    async def create(self, video_url: str) -> dict:
        """完整的视频->技能转换流程"""
        
        # 步骤1: 分析视频
        learner = VideoLearner()
        analysis = await learner.analyze(video_url)
        
        # 步骤2: 质量评估
        quality = self._assess_quality(analysis)
        if quality['score'] < 0.7:
            return {'status': 'rejected', 'reason': quality['issues']}
        
        # 步骤3: 提取技能要素
        skill_elements = self._extract_skill_elements(analysis)
        
        # 步骤4: 设计技能结构
        skill_design = self._design_skill(skill_elements)
        
        # 步骤5: 生成 SKILL.md
        skill_md = self._generate_skill_md(skill_design)
        
        # 步骤6: 测试验证
        test_result = await self._test_skill(skill_design)
        if not test_result['passed']:
            return {'status': 'failed_test', 'errors': test_result['errors']}
        
        # 步骤7: 部署技能
        skill_path = self._deploy_skill(skill_md, skill_design['name'])
        
        return {
            'status': 'success',
            'skill_path': skill_path,
            'quality_score': quality['score'],
            'test_coverage': test_result['coverage']
        }
    
    def _assess_quality(self, analysis: dict) -> dict:
        """评估视频是否适合创建技能"""
        scores = {
            'content_density': len(analysis['transcript']) / analysis['duration'],
            'actionability': len(analysis.get('commands', [])) / 10,
            'structure_clarity': analysis.get('structure_score', 0.5),
            'practical_value': len(analysis.get('action_items', [])) / 5,
            'code_examples': len(analysis.get('code_snippets', [])) / 3
        }
        
        overall = sum(scores.values()) / len(scores)
        
        issues = []
        if scores['actionability'] < 0.3:
            issues.append("可操作性不足")
        if scores['content_density'] < 0.1:
            issues.append("内容密度过低")
            
        return {'score': overall, 'scores': scores, 'issues': issues}
    
    def _extract_skill_elements(self, analysis: dict) -> dict:
        """从分析结果中提取技能要素"""
        return {
            'name': self._generate_skill_name(analysis),
            'category': analysis['metadata'].get('category', 'general'),
            'description': analysis['summary'],
            'commands': analysis.get('commands', []),
            'examples': analysis.get('code_snippets', []),
            'best_practices': analysis.get('recommendations', []),
            'dependencies': analysis.get('tools', []),
            'related_skills': analysis.get('related_topics', [])
        }
    
    def _generate_skill_name(self, analysis: dict) -> str:
        """生成技能名称"""
        # 从标题、标签、内容中提取关键词
        keywords = self._extract_keywords(analysis)
        
        # 转换为大驼峰或 kebab-case
        name = '-'.join(keywords[:3]).lower()
        
        # 确保唯一性
        return self._ensure_unique_name(name)
    
    def _design_skill(self, elements: dict) -> dict:
        """设计技能结构"""
        return {
            'name': elements['name'],
            'metadata': {
                'name': elements['name'],
                'version': '1.0.0',
                'description': elements['description'],
                'author': 'Auto-generated from video',
                'category': elements['category'],
                'source_video': elements.get('video_url'),
                'created_at': datetime.now().isoformat()
            },
            'sections': [
                {'title': '快速开始', 'content': self._create_quickstart(elements)},
                {'title': '使用示例', 'content': self._create_examples(elements)},
                {'title': '最佳实践', 'content': self._create_best_practices(elements)}
            ]
        }
    
    def _generate_skill_md(self, design: dict) -> str:
        """生成 SKILL.md 内容"""
        template = """---
name: {name}
version: {version}
description: |
  {description}

author: {author}
category: {category}
created: {created_at}
dependencies:
{dependencies}
---

# {name}

## 概述

{description}

## 快速开始

{quickstart}

## 使用示例

{examples}

## 最佳实践

{best_practices}

---
*Auto-generated from video learning*
"""
        return template.format(**design['metadata'])
    
    async def _test_skill(self, design: dict) -> dict:
        """测试生成的技能"""
        errors = []
        
        # 测试所有代码示例
        for example in design.get('examples', []):
            try:
                result = await self._run_example(example)
                if not result['success']:
                    errors.append(f"示例失败: {example['title']}")
            except Exception as e:
                errors.append(f"示例异常: {str(e)}")
        
        return {
            'passed': len(errors) == 0,
            'errors': errors,
            'coverage': len(design.get('examples', []))
        }
    
    def _deploy_skill(self, content: str, name: str) -> str:
        """部署技能到 skills 目录"""
        import os
        
        skill_dir = f"skills/{name}"
        os.makedirs(skill_dir, exist_ok=True)
        
        skill_path = f"{skill_dir}/SKILL.md"
        with open(skill_path, 'w') as f:
            f.write(content)
        
        return skill_path
```

## 技能质量监控

### 性能指标

```python
class SkillPerformanceMonitor:
    """技能性能监控器"""
    
    def __init__(self):
        self.metrics = {
            'task_success_rate': [],
            'response_quality_scores': [],
            'skill_usage_frequency': {},
            'learning_efficiency': [],
            'user_satisfaction': []
        }
    
    def record_interaction(self, task: str, result: dict, feedback: dict):
        """记录每次交互用于分析"""
        self.metrics['task_success_rate'].append(result.get('success', False))
        self.metrics['response_quality_scores'].append(feedback.get('quality', 0))
        
        # 技能使用频率
        skill = task.get('skill_used')
        if skill:
            self.metrics['skill_usage_frequency'][skill] = \
                self.metrics['skill_usage_frequency'].get(skill, 0) + 1
        
        # 识别改进点
        if not result.get('success') or feedback.get('quality', 0) < 0.7:
            improvement_area = self._identify_weakness(task, result)
            self._queue_improvement(improvement_area)
    
    def generate_improvement_plan(self) -> dict:
        """基于数据生成改进计划"""
        weaknesses = self._analyze_weaknesses(self.metrics)
        return self._create_learning_plan(weaknesses)
```

### 成功指标

| 指标 | 目标 | 监控频率 |
|------|------|----------|
| **技能增长率** | 每周新增 2-3 个 | 每周 |
| **视频学习量** | 每天分析 5-10 个 | 每日 |
| **任务成功率** | 95%+ | 实时 |
| **技能使用率** | 每个技能每周至少使用1次 | 每周 |
| **用户满意度** | 4.5+/5 | 每次交互 |

## 预期成果

### 短期 (1个月)
- 掌握视频内容自动分析
- 创建 5-10 个新技能
- 建立稳定的学习循环

### 中期 (3个月)
- 覆盖主要学习场景
- 技能库达到 50+
- 实现自我诊断和改进

### 长期 (6个月+)
- 具备自主学习能力
- 技能库达到 100+
- 能够处理全新领域

## Cron 配置

```bash
# 添加到 crontab

# 每日循环 - 每4小时
0 */4 * * * cd ~/.openclaw/workspace && python3 skills/self-learning-loop/daily-loop.py >> ~/.openclaw/logs/learning-daily.log 2>&1

# 每周循环 - 每周日9点
0 9 * * 0 cd ~/.openclaw/workspace && python3 skills/self-learning-loop/weekly-loop.py >> ~/.openclaw/logs/learning-weekly.log 2>&1

# 每月循环 - 每月1日10点
0 10 1 * * cd ~/.openclaw/workspace && python3 skills/self-learning-loop/monthly-loop.py >> ~/.openclaw/logs/learning-monthly.log 2>&1
```

## 相关技能

- [video-learning](../video-learning/SKILL.md) - 视频学习系统
- [bilibili-video-analyzer](../bilibili-video-analyzer/SKILL.md) - Bilibili 视频分析
- [youtube-video-analyzer](../youtube-video-analyzer/SKILL.md) - YouTube 视频分析
- [skill-creator](../skill-creator/SKILL.md) - 技能创建指南
- [cron-automation](../cron-automation/SKILL.md) - Cron 任务自动化

---

*"The capacity to learn is a gift; the ability to learn is a skill; 
the willingness to learn is a choice."* — Brian Herbert
