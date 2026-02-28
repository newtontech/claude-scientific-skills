---
name: get-tldr
version: 1.0.0
description: |
  调用 get-tldr.com API 快速总结长文章。
  30 秒拿到核心要点，信息过载时代的生存技能。

author: Assistant
category: productivity
dependencies:
  - curl
  - jq
homepage: https://get-tldr.com
---

# Get-TLDR 文章总结

## 概述

快速总结长文章，提取核心要点。适合：
- 没时间读长文？30 秒拿到核心要点
- 信息过载时代的生存技能
- 快速了解文章价值决定是否深入阅读

## 安装

### 方法 1: 直接调用 API

```bash
# 使用 curl 调用 get-tldr API
curl -s "https://api.get-tldr.com/summarize" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/article"}'
```

### 方法 2: 使用 Python

```python
import requests

def summarize_article(url: str) -> dict:
    """总结文章"""
    response = requests.post(
        "https://api.get-tldr.com/summarize",
        json={"url": url},
        headers={"Content-Type": "application/json"}
    )
    return response.json()

# 使用
result = summarize_article("https://example.com/long-article")
print(result['summary'])
print(result['key_points'])
```

## 使用示例

### 示例 1: 快速总结网页

```bash
# 总结一篇文章
tldr summarize "https://techcrunch.com/some-article"

# 输出格式：
# 📄 文章标题
# 📝 一句话总结
# 🎯 核心要点 (3-5 条)
# ⏱️ 阅读时间: X 分钟
```

### 示例 2: 批量总结

```python
async def batch_summarize(urls: list[str]) -> list[dict]:
    """批量总结多篇文章"""
    results = []
    for url in urls:
        try:
            summary = await summarize_article(url)
            results.append({
                'url': url,
                'title': summary['title'],
                'summary': summary['summary'],
                'key_points': summary['key_points']
            })
        except Exception as e:
            results.append({'url': url, 'error': str(e)})
    return results

# 使用
articles = [
    "https://example.com/article1",
    "https://example.com/article2",
    "https://example.com/article3"
]
summaries = await batch_summarize(articles)
```

### 示例 3: 与阅读列表集成

```python
class ReadingListSummarizer:
    """自动总结阅读列表"""
    
    def __init__(self):
        self.summarized = []
    
    async def process_reading_list(self, urls: list[str]):
        """处理整个阅读列表"""
        for url in urls:
            summary = await summarize_article(url)
            
            # 根据质量评分决定是否保留
            if summary['quality_score'] > 0.7:
                self.summarized.append({
                    'url': url,
                    'title': summary['title'],
                    'summary': summary['summary'],
                    'worth_reading': True
                })
            else:
                self.summarized.append({
                    'url': url,
                    'title': summary['title'],
                    'worth_reading': False
                })
        
        return self.summarized
```

## 输出格式

```json
{
  "title": "文章标题",
  "summary": "一句话总结",
  "key_points": [
    "要点1",
    "要点2",
    "要点3"
  ],
  "reading_time": "5 min",
  "quality_score": 0.85,
  "original_length": 5000,
  "summary_length": 300
}
```

## 高级用法

### 自定义总结长度

```python
def summarize_with_length(url: str, max_length: int = 500) -> dict:
    """自定义总结长度"""
    response = requests.post(
        "https://api.get-tldr.com/summarize",
        json={
            "url": url,
            "max_length": max_length,
            "language": "zh"  # 中文总结
        }
    )
    return response.json()
```

### 保存到笔记

```python
def save_summary_to_notes(summary: dict, notes_file: str):
    """保存总结到笔记文件"""
    with open(notes_file, 'a') as f:
        f.write(f"## {summary['title']}\n\n")
        f.write(f"**链接**: {summary['url']}\n\n")
        f.write(f"**总结**: {summary['summary']}\n\n")
        f.write("**要点**:\n")
        for point in summary['key_points']:
            f.write(f"- {point}\n")
        f.write("\n---\n\n")
```

## 与 Feishu/Slack 集成

```python
async def summarize_and_share(url: str, channel: str):
    """总结并分享到群聊"""
    summary = await summarize_article(url)
    
    message = f"""📄 {summary['title']}

📝 {summary['summary']}

🎯 核心要点:
{chr(10).join(f"• {p}" for p in summary['key_points'])}

⏱️ 阅读时间: {summary['reading_time']}
🔗 {url}"""
    
    # 发送到指定频道
    await send_message(channel, message)
```

## 最佳实践

1. **批量处理**: 一次总结 5-10 篇文章，避免 API 限制
2. **质量过滤**: 只保留 quality_score > 0.7 的文章
3. **定期清理**: 每周清理一次已读列表
4. **分类存储**: 按主题分类保存总结

## 相关技能

- [tavily-search](../tavily-search/SKILL.md) - 搜索相关文章
- [content-research-writer](../content-research-writer/SKILL.md) - 内容写作
- [feishu](../feishu/SKILL.md) - 飞书集成
- [slack](../slack/SKILL.md) - Slack 集成

---

*"Don't read everything. Read what matters."*
