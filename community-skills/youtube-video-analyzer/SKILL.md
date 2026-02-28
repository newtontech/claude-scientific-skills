---
name: youtube-video-analyzer
version: 1.0.0
description: |
  Automated YouTube video content analysis and learning extraction.
  Fetches transcripts, analyzes content with AI, generates learning notes.
  Supports educational videos, tutorials, lectures, and knowledge content.

author: Assistant
category: video-learning
dependencies:
  - youtube-transcript-api
  - yt-dlp
  - openai-whisper
  - google-api-python-client
---

# YouTube 视频分析器

## 快速开始

```python
from skills.youtube_video_analyzer import YouTubeLearner

# 初始化
learner = YouTubeLearner()

# 分析视频
result = await learner.analyze("https://www.youtube.com/watch?v=VIDEO_ID")

# 获取学习产出
print(result.summary)
print(result.key_points)
print(result.skill_suggestions)
```

## 核心功能

### 1. 字幕提取 (多层级)

```python
async def extract_transcript(video_id: str) -> TranscriptResult:
    """
    多级字幕提取策略
    """
    from youtube_transcript_api import YouTubeTranscriptApi
    
    strategies = [
        # Level 1: 官方字幕 (多语言)
        lambda: YouTubeTranscriptApi.get_transcript(video_id, languages=['zh', 'en']),
        
        # Level 2: 自动生成的字幕
        lambda: YouTubeTranscriptApi.get_transcript(video_id, languages=['zh-CN', 'en-US']),
        
        # Level 3: 使用 yt-dlp 提取
        lambda: extract_with_ytdlp(video_id),
        
        # Level 4: 音频转录 (Whisper)
        lambda: transcribe_with_whisper(video_id)
    ]
    
    for strategy in strategies:
        try:
            result = await strategy()
            if result and len(result) > 0:
                return {
                    'text': ' '.join([item['text'] for item in result]),
                    'segments': result,
                    'source': strategy.__name__
                }
        except Exception:
            continue
    
    return None
```

### 2. 视频元数据获取

```python
async def get_video_metadata(video_id: str) -> VideoMetadata:
    """
    获取视频详细信息
    """
    import yt_dlp
    
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
        
        return {
            'title': info.get('title'),
            'description': info.get('description'),
            'channel': info.get('channel'),
            'duration': info.get('duration'),
            'view_count': info.get('view_count'),
            'like_count': info.get('like_count'),
            'upload_date': info.get('upload_date'),
            'tags': info.get('tags', []),
            'categories': info.get('categories', []),
            'language': info.get('language'),
            'chapters': info.get('chapters', [])  # 视频章节信息
        }
```

### 3. 内容 AI 分析

```python
async def analyze_content(transcript: str, metadata: dict) -> ContentAnalysis:
    """
    深度内容分析
    """
    analysis_prompt = f"""
    分析以下 YouTube 视频内容，提取结构化知识：
    
    标题: {metadata['title']}
    频道: {metadata['channel']}
    标签: {', '.join(metadata.get('tags', [])[:5])}
    时长: {metadata['duration']} 秒
    
    内容文本 (前10000字符):
    {transcript[:10000]}
    
    请提供：
    1. 一句话总结
    2. 核心知识点 (3-7个)
    3. 讲解逻辑结构
    4. 可提取的技能/工具
    5. 代码示例 (如有)
    6. 学习难度评估 (1-10)
    7. 相关领域标签
    8. 推荐学习路径
    9. 类似视频推荐关键词
    """
    
    return await ai.analyze(analysis_prompt)
```

### 4. 智能章节分割

```python
def auto_chapter_detection(transcript: list, chapters: list = None) -> List[Chapter]:
    """
    基于字幕内容或 YouTube 章节自动分割
    """
    if chapters:
        # 使用 YouTube 自带的章节
        return [{
            'start': ch['start_time'],
            'title': ch['title'],
            'summary': generate_chapter_summary(transcript, ch)
        } for ch in chapters]
    
    # 否则基于内容主题变化自动检测
    return detect_topic_shifts(transcript)
```

### 5. 学习笔记生成

```python
def generate_learning_notes(analysis: ContentAnalysis, metadata: dict) -> LearningNotes:
    """
    生成多格式学习笔记
    """
    return {
        'markdown_summary': generate_markdown_summary(analysis, metadata),
        'mind_map': generate_mind_map(analysis),
        'flashcards': generate_flashcards(analysis),
        'quiz': generate_quiz_questions(analysis),
        'code_snippets': extract_code_examples(analysis),
        'key_timestamps': extract_key_timestamps(analysis),
        'further_resources': suggest_related_resources(analysis),
        'action_items': extract_action_items(analysis)
    }
```

## 使用示例

### 示例1: 学习技术教程

```python
async def learn_tech_tutorial(video_url: str):
    """
    学习技术教程类 YouTube 视频
    """
    learner = YouTubeLearner()
    
    # 分析视频
    result = await learner.analyze(video_url)
    
    # 提取代码示例
    code_blocks = result.extract_code_blocks()
    for i, code in enumerate(code_blocks):
        save_script(f"example_{i}.py", code)
    
    # 生成技能草案
    skill_draft = await generate_skill_draft(result)
    
    return {
        'summary': result.summary,
        'commands': result.extract_commands(),
        'skill_suggestion': skill_draft,
        'exercises': result.generate_exercises(),
        'timestamp_links': result.generate_timestamp_links()
    }

# 使用
report = await learn_tech_tutorial("https://www.youtube.com/watch?v=example")
```

### 示例2: 批量频道学习

```python
async def learn_from_channel(channel_id: str, max_videos: int = 10):
    """
    批量学习某个 YouTube 频道的视频
    """
    learner = YouTubeLearner()
    
    # 获取频道视频列表
    videos = await get_channel_videos(channel_id, max_videos)
    
    results = []
    for video in videos:
        try:
            result = await learner.analyze(video['id'])
            results.append(result)
            
            # 识别系列课程结构
            if is_series_video(video['title']):
                series_structure = analyze_series_structure(results)
                print(f"检测到系列课程: {series_structure}")
                
        except Exception as e:
            print(f"分析 {video['id']} 失败: {e}")
            continue
    
    # 生成综合学习路径
    learning_path = synthesize_learning_path(results)
    
    return {
        'videos_analyzed': len(results),
        'learning_path': learning_path,
        'knowledge_graph': build_knowledge_graph(results),
        'skill_recommendations': extract_skills_from_series(results)
    }
```

### 示例3: 实时学习监控

```python
async def monitor_learning_progress(subscriptions: list):
    """
    监控订阅频道的更新并自动学习
    """
    learner = YouTubeLearner()
    
    for channel in subscriptions:
        # 检查新视频
        new_videos = await check_new_videos(channel)
        
        for video in new_videos:
            # 判断是否符合学习目标
            if is_relevant_to_learning_goals(video):
                print(f"发现相关视频: {video['title']}")
                
                # 自动分析
                result = await learner.analyze(video['id'])
                
                # 如果质量高，立即学习
                if result.quality_score > 0.8:
                    await process_high_quality_content(result)
                    
                    # 生成即时学习报告
                    await send_learning_summary(result)
```

## 批量处理工作流

```python
async def batch_process_playlist(playlist_id: str):
    """
    批量处理 YouTube 播放列表
    """
    from yt_dlp import YoutubeDL
    
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        playlist = ydl.extract_info(
            f"https://www.youtube.com/playlist?list={playlist_id}",
            download=False
        )
        
        videos = playlist['entries']
        
        # 并发分析 (限制并发数避免限流)
        semaphore = asyncio.Semaphore(3)
        
        async def analyze_with_limit(video):
            async with semaphore:
                return await analyze_video(video['id'])
        
        results = await asyncio.gather(*[
            analyze_with_limit(v) for v in videos
        ])
        
        # 生成课程大纲
        syllabus = generate_syllabus(results)
        
        return {
            'total_videos': len(videos),
            'analyzed': len([r for r in results if r]),
            'syllabus': syllabus,
            'estimated_learning_time': sum(r.duration for r in results if r)
        }
```

## 集成到学习循环

```python
# 在每日学习脚本中调用
async def daily_youtube_learning():
    """
    每日 YouTube 视频学习任务
    """
    learner = YouTubeLearner()
    
    # 1. 从订阅/推荐获取视频
    videos_to_learn = await discover_videos_from_subscriptions()
    
    # 2. 筛选高质量内容
    filtered = filter_by_quality_and_relevance(videos_to_learn)
    
    # 3. 批量分析 (每天最多5个)
    for video in filtered[:5]:
        result = await learner.analyze(video['id'])
        
        # 4. 提取技能
        if result.has_actionable_content:
            skill = await extract_skill(result)
            await create_or_update_skill(skill)
        
        # 5. 记录学习
        log_learning(video, result)
        
        # 6. 生成分享卡片 (可选)
        if result.quality_score > 0.9:
            await generate_share_card(result)
    
    # 7. 生成日报
    return generate_daily_learning_report()
```

## 最佳实践

### 1. 优先使用官方字幕
- YouTube 官方字幕质量最高
- 支持多语言选择
- 有时间戳信息

### 2. 处理长视频策略
- 按章节分段分析
- 提取关键片段
- 生成章节摘要

### 3. 质量评估
```python
def assess_video_quality(metadata: dict, transcript: str) -> QualityScore:
    """
    评估视频学习价值
    """
    scores = {
        'content_density': len(transcript) / metadata['duration'],
        'engagement': metadata['like_count'] / metadata['view_count'],
        'channel_reputation': get_channel_reputation(metadata['channel']),
        'production_quality': detect_production_quality(metadata),
        'educational_value': assess_educational_markers(transcript)
    }
    
    return calculate_weighted_score(scores)
```

### 4. 避免版权问题
- 只分析公开视频
- 不下载完整视频 (只提取音频/字幕)
- 遵守 YouTube ToS
- 用于个人学习目的

## 错误处理

```python
class YouTubeAnalysisError(Exception):
    pass

async def robust_analyze(video_id: str, max_retries: int = 3):
    """
    健壮的视频分析
    """
    for attempt in range(max_retries):
        try:
            return await analyze_video(video_id)
        except TranscriptsDisabled:
            # 尝试音频转录
            return await analyze_with_audio(video_id)
        except VideoUnavailable:
            raise YouTubeAnalysisError(f"视频不可用: {video_id}")
        except RateLimitError:
            await asyncio.sleep(60 * (attempt + 1))
            continue
    
    raise YouTubeAnalysisError(f"分析失败: {video_id}")
```

## 与 Bilibili 分析器对比

| 特性 | YouTube | Bilibili |
|------|---------|----------|
| 字幕质量 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| API 稳定性 | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 多语言支持 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 弹幕/评论 | ❌ | ✅ |
| 技术内容 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 中文内容 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**建议:** 两者结合使用，YouTube 用于国际技术内容，Bilibili 用于中文社区内容。

---

*"Learning from videos is not just watching, it's understanding and applying."*
