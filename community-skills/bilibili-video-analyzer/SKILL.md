---
name: bilibili-video-analyzer
version: 1.0.0
description: |
  自动化 Bilibili 视频内容分析和知识提取。
  提取字幕、弹幕、元数据，使用 AI 分析内容并生成学习笔记。

author: Assistant
category: video-learning
dependencies:
  - bilibili-api-python
  - whisper
  - ffmpeg-python
  - beautifulsoup4
  - requests
---

# Bilibili 视频分析器

## 快速开始

```python
from skills.bilibili_video_analyzer import VideoLearner

# 初始化学习者
learner = VideoLearner()

# 分析视频
result = await learner.analyze("BV1xx411c7mD")

# 获取学习产出
print(result.summary)
print(result.key_points)
print(result.skill_suggestions)
```

## 核心功能

### 1. 视频信息提取

```python
async def extract_video_info(bvid: str) -> VideoInfo:
    """
    提取视频元数据
    """
    return {
        'title': '视频标题',
        'description': '视频简介',
        'uploader': 'UP主',
        'duration': 600,  # 秒
        'tags': ['标签1', '标签2'],
        'view_count': 100000,
        'like_count': 5000,
        'coin_count': 1000,
        'danmaku_count': 2000
    }
```

### 2. 字幕提取 (多层级)

```python
async def extract_subtitles(bvid: str) -> SubtitleResult:
    """
    多级字幕提取策略
    """
    strategies = [
        # Level 1: 官方 CC 字幕
        lambda: get_official_subtitle(bvid),
        
        # Level 2: AI 自动生成字幕
        lambda: get_ai_subtitle(bvid),
        
        # Level 3: 音频转录
        lambda: transcribe_audio(bvid),
        
        # Level 4: 弹幕时间轴分析
        lambda: analyze_danmaku_as_subtitle(bvid)
    ]
    
    for strategy in strategies:
        result = await strategy()
        if result and len(result.text) > 100:
            return result
    
    return None
```

### 3. 弹幕分析

```python
async def analyze_danmaku(bvid: str) -> DanmakuAnalysis:
    """
    弹幕内容分析，识别：
    - 高潮时间点
    - 观众反应
    - 关键信息标记
    """
    danmaku_data = await fetch_danmaku(bvid)
    
    return {
        'highlights': find_peaks(danmaku_data),  # 弹幕高峰 = 重点内容
        'sentiment': analyze_sentiment(danmaku_data),
        'keywords': extract_keywords(danmaku_data),
        'questions': extract_questions(danmaku_data),  # 观众疑问
        'key_moments': identify_key_moments(danmaku_data)
    }
```

### 4. 内容 AI 分析

```python
async def analyze_content(text: str, metadata: dict) -> ContentAnalysis:
    """
    深度内容分析
    """
    prompt = f"""
    分析以下视频内容，提取结构化知识：
    
    标题: {metadata['title']}
    UP主: {metadata['uploader']}
    标签: {', '.join(metadata['tags'])}
    
    内容文本:
    {text[:10000]}  # 前10000字符
    
    请提供：
    1. 一句话总结
    2. 核心知识点 (3-5个)
    3. 讲解逻辑结构
    4. 可提取的技能/工具
    5. 学习难度评估
    6. 相关领域标签
    7. 推荐学习路径
    """
    
    return await ai.analyze(prompt)
```

### 5. 学习笔记生成

```python
def generate_learning_notes(analysis: ContentAnalysis) -> LearningNotes:
    """
    生成多格式学习笔记
    """
    return {
        'markdown_summary': generate_markdown(analysis),
        'mind_map': generate_mind_map(analysis),
        'flashcards': generate_flashcards(analysis),
        'quiz_questions': generate_quiz(analysis),
        'code_snippets': extract_code_examples(analysis),
        'further_reading': suggest_related_resources(analysis)
    }
```

## 完整使用示例

### 示例1: 技术教程视频学习

```python
async def learn_tech_tutorial(bvid: str):
    """
    学习技术教程类视频
    """
    learner = VideoLearner()
    
    # 1. 分析视频
    result = await learner.analyze(bvid)
    
    # 2. 提取代码示例
    code_blocks = result.extract_code_blocks()
    
    # 3. 生成可执行脚本
    for i, code in enumerate(code_blocks):
        save_script(f"example_{i}.py", code)
    
    # 4. 创建技能草案
    skill_draft = await generate_skill_draft(result)
    
    # 5. 输出学习报告
    return {
        'summary': result.summary,
        'key_commands': result.extract_commands(),
        'skill_suggestion': skill_draft,
        'practice_exercises': result.generate_exercises()
    }

# 使用
report = await learn_tech_tutorial("BV1Jdf8BYE7W")
```

### 示例2: 知识科普视频分析

```python
async def learn_knowledge_video(bvid: str):
    """
    学习知识科普类视频
    """
    learner = VideoLearner()
    result = await learner.analyze(bvid)
    
    # 生成知识卡片
    flashcards = result.generate_flashcards()
    
    # 构建知识图谱
    knowledge_graph = result.build_knowledge_graph()
    
    # 生成思维导图
    mind_map = result.generate_mind_map()
    
    return {
        'flashcards': flashcards,
        'knowledge_graph': knowledge_graph,
        'mind_map': mind_map,
        'quiz': result.generate_quiz()
    }
```

### 示例3: 批量视频学习

```python
async def batch_learn(bvids: list[str]):
    """
    批量学习多个视频
    """
    learner = VideoLearner()
    
    results = []
    for bvid in bvids:
        try:
            result = await learner.analyze(bvid)
            results.append(result)
            
            # 识别跨视频的共同主题
            if len(results) > 1:
                common_themes = find_common_themes(results)
                print(f"发现共同主题: {common_themes}")
                
        except Exception as e:
            print(f"分析 {bvid} 失败: {e}")
            continue
    
    # 生成综合学习报告
    comprehensive_report = synthesize_learning(results)
    
    return comprehensive_report
```

## 高级功能

### 智能章节分割

```python
def auto_chapter_detection(subtitle: str, danmaku: list) -> List[Chapter]:
    """
    基于内容变化和弹幕密度自动分割章节
    """
    # 结合字幕主题变化和弹幕高峰
    chapters = []
    
    # 检测主题转换点
    topic_shifts = detect_topic_shifts(subtitle)
    
    # 检测弹幕高峰（观众反应强烈的点）
    danmaku_peaks = detect_danmaku_peaks(danmaku)
    
    # 合并两种信号
    segment_points = merge_signals(topic_shifts, danmaku_peaks)
    
    for i, point in enumerate(segment_points):
        chapters.append({
            'start': point.timestamp,
            'title': generate_chapter_title(point.context),
            'summary': summarize_section(point.content)
        })
    
    return chapters
```

### 学习难度评估

```python
def assess_difficulty(content: str, metadata: dict) -> DifficultyAssessment:
    """
    评估视频学习难度
    """
    factors = {
        'terminology_density': count_technical_terms(content),
        'concept_complexity': assess_concept_complexity(content),
        'prerequisites_needed': identify_prerequisites(content),
        'pace': metadata['duration'] / len(content.split()),
        'audience_level': infer_audience_level(metadata['tags'])
    }
    
    # 综合评分
    difficulty_score = calculate_difficulty(factors)
    
    return {
        'score': difficulty_score,  # 1-10
        'level': map_score_to_level(difficulty_score),  # 入门/中级/高级
        'estimated_learning_time': estimate_time(content),
        'prerequisites': factors['prerequisites_needed'],
        'target_audience': factors['audience_level']
    }
```

## 最佳实践

### 1. 优先使用字幕
官方字幕 > AI 字幕 > 音频转录 > 弹幕

### 2. 结合多源信息
视频内容 + 弹幕 + 评论 + 简介 = 完整理解

### 3. 分段处理长视频
- 每 10-15 分钟为一个学习单元
- 为每个单元生成小结
- 最后综合所有单元

### 4. 主动验证
- 提取的代码要测试运行
- 关键概念要交叉验证
- 不确定的内容要标注

## 集成到学习循环

```python
# 在 self-learning-loop 中调用
async def daily_video_learning():
    """
    每日视频学习任务
    """
    # 1. 发现待学习视频
    videos_to_learn = discover_videos_from_feed()
    
    # 2. 批量分析
    for video in videos_to_learn[:5]:  # 每天最多5个
        result = await bilibili_analyzer.analyze(video.bvid)
        
        # 3. 提取技能
        if result.has_tutorial_content:
            skill = await extract_skill(result)
            await create_skill(skill)
        
        # 4. 记录学习
        log_learning(video, result)
    
    # 5. 生成日报
    return generate_daily_learning_report()
```

## 错误处理

```python
class VideoAnalysisError(Exception):
    pass

async def robust_analyze(bvid: str, max_retries: int = 3):
    """
    健壮的视频分析，带重试机制
    """
    for attempt in range(max_retries):
        try:
            return await analyze_video(bvid)
        except SubtitleNotFoundError:
            # 尝试音频转录
            return await analyze_with_transcription(bvid)
        except RateLimitError:
            await asyncio.sleep(60 * (attempt + 1))
            continue
        except Exception as e:
            if attempt == max_retries - 1:
                # 最后尝试：仅使用元数据
                return await analyze_metadata_only(bvid)
            continue
    
    raise VideoAnalysisError(f"无法分析视频 {bvid}")
```

## 性能优化

- **缓存机制**: 已分析的视频结果缓存 7 天
- **并发处理**: 批量分析时使用 asyncio 并发
- **增量更新**: 只处理新增的视频片段
- **智能采样**: 长视频采用关键帧采样而非全量分析

---

*"Every video is a learning opportunity."*
