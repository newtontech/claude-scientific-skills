---
name: x-api
version: 1.0.0
description: |
  实时搜索 X (Twitter)，提取相关帖子。
  监控品牌提及、追踪热点、收集行业情报。
  支持 Twitter API v2 和 unofficial API。

author: Assistant
category: social
dependencies:
  - tweepy (Twitter API v2)
  - requests
  - python-dotenv
homepage: https://developer.twitter.com
---

# X (Twitter) API

## 概述

强大的 X (Twitter) 数据获取工具：
- 🔍 实时搜索推文
- 📊 监控品牌提及
- 🔥 追踪热点话题
- 📈 收集行业情报
- 👤 用户分析

## 安装

```bash
# 安装 Twitter API 库
pip install tweepy requests python-dotenv

# 或安装 unofficial API 客户端
pip install ntscraper  # 无需 API Key
```

## 快速开始

### Twitter API v2 (官方)

```python
import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

# 配置认证
client = tweepy.Client(
    bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
    consumer_key=os.getenv('TWITTER_API_KEY'),
    consumer_secret=os.getenv('TWITTER_API_SECRET'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_ACCESS_SECRET')
)

# 搜索推文
tweets = client.search_recent_tweets(
    query="OpenClaw",
    max_results=100,
    tweet_fields=['created_at', 'public_metrics', 'author_id']
)

for tweet in tweets.data:
    print(f"{tweet.created_at}: {tweet.text}")
```

### Unofficial API (无需 API Key)

```python
from ntscraper import Nitter

# 使用 Nitter 实例
scraper = Nitter()

# 搜索推文
tweets = scraper.get_tweets("OpenClaw", mode='term', number=50)

for tweet in tweets['tweets']:
    print(f"@{tweet['user']['username']}: {tweet['text']}")
```

## 核心功能

### 1. 实时搜索

```python
import asyncio
from datetime import datetime, timedelta

class TwitterSearcher:
    """Twitter 实时搜索"""
    
    def __init__(self, client):
        self.client = client
    
    async def search_tweets(self, query: str, max_results: int = 100, 
                           since: datetime = None) -> list:
        """搜索推文"""
        tweets = []
        
        # 构建查询
        if since:
            start_time = since.isoformat()
        else:
            start_time = (datetime.now() - timedelta(days=7)).isoformat()
        
        response = self.client.search_recent_tweets(
            query=query,
            max_results=min(max_results, 100),
            start_time=start_time,
            tweet_fields=['created_at', 'public_metrics', 'context_annotations'],
            user_fields=['username', 'public_metrics'],
            expansions=['author_id']
        )
        
        if response.data:
            for tweet in response.data:
                tweets.append({
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'metrics': tweet.public_metrics,
                    'author_id': tweet.author_id
                })
        
        return tweets
    
    async def search_with_filters(self, keyword: str, 
                                  exclude_retweets: bool = True,
                                  min_likes: int = 10) -> list:
        """带过滤条件的搜索"""
        query = keyword
        
        if exclude_retweets:
            query += " -is:retweet"
        
        if min_likes > 0:
            query += f" min_faves:{min_likes}"
        
        return await self.search_tweets(query)

# 使用
searcher = TwitterSearcher(client)
tweets = await searcher.search_tweets("#AI", max_results=50)
```

### 2. 品牌监控

```python
class BrandMonitor:
    """品牌提及监控"""
    
    def __init__(self, client, brand_keywords: list[str]):
        self.client = client
        self.keywords = brand_keywords
        self.mentions = []
    
    async def monitor_mentions(self, interval: int = 300):
        """持续监控品牌提及"""
        while True:
            for keyword in self.keywords:
                tweets = await self.search_mentions(keyword)
                
                for tweet in tweets:
                    if self.is_new_mention(tweet):
                        self.mentions.append(tweet)
                        await self.handle_mention(tweet)
            
            await asyncio.sleep(interval)
    
    async def search_mentions(self, keyword: str) -> list:
        """搜索品牌提及"""
        query = f"{keyword} -from:your_brand_account"
        
        tweets = self.client.search_recent_tweets(
            query=query,
            max_results=100,
            tweet_fields=['created_at', 'public_metrics', 'lang']
        )
        
        return tweets.data if tweets.data else []
    
    def is_new_mention(self, tweet) -> bool:
        """检查是否是新的提及"""
        return tweet.id not in [m.id for m in self.mentions]
    
    async def handle_mention(self, tweet):
        """处理品牌提及"""
        print(f"🚨 品牌提及: @{tweet.author_id}")
        print(f"内容: {tweet.text}")
        print(f"时间: {tweet.created_at}")
        print(f"互动: {tweet.public_metrics}")
        
        # 可以发送通知或保存到数据库
        await self.send_alert(tweet)
    
    async def send_alert(self, tweet):
        """发送提醒"""
        # 集成飞书/Slack
        message = f"""📢 品牌提及提醒

@{tweet.author_id}: {tweet.text[:100]}...

🔗 https://twitter.com/i/web/status/{tweet.id}
"""
        # await send_feishu_message(message)

# 使用
monitor = BrandMonitor(client, ["YourBrand", "YourProduct"])
await monitor.monitor_mentions()
```

### 3. 热点追踪

```python
class TrendTracker:
    """热点话题追踪"""
    
    def __init__(self, client):
        self.client = client
    
    async def get_trending_topics(self, woeid: int = 1) -> list:
        """获取 trending topics"""
        trends = self.client.get_place_trends(id=woeid)
        
        trending = []
        for trend in trends[0]["trends"]:
            trending.append({
                'name': trend['name'],
                'volume': trend.get('tweet_volume', 0),
                'url': trend['url']
            })
        
        return sorted(trending, key=lambda x: x['volume'], reverse=True)
    
    async def track_hashtag(self, hashtag: str, duration_hours: int = 24) -> dict:
        """追踪特定话题标签"""
        query = f"#{hashtag}"
        
        tweets = await self.search_tweets(query, max_results=100)
        
        # 分析数据
        analysis = {
            'total_tweets': len(tweets),
            'total_likes': sum(t['metrics']['like_count'] for t in tweets),
            'total_retweets': sum(t['metrics']['retweet_count'] for t in tweets),
            'time_distribution': self._analyze_time_distribution(tweets),
            'top_tweets': sorted(tweets, 
                               key=lambda x: x['metrics']['like_count'], 
                               reverse=True)[:5]
        }
        
        return analysis
    
    def _analyze_time_distribution(self, tweets: list) -> dict:
        """分析时间分布"""
        from collections import Counter
        
        hours = [t['created_at'].hour for t in tweets]
        return dict(Counter(hours))

# 使用
tracker = TrendTracker(client)
trends = await tracker.get_trending_topics()
analysis = await tracker.track_hashtag("AI", duration_hours=24)
```

### 4. 行业情报收集

```python
class IndustryIntelligence:
    """行业情报收集"""
    
    def __init__(self, client):
        self.client = client
        self.keywords = []
    
    async def collect_intelligence(self, keywords: list[str], 
                                   days: int = 7) -> dict:
        """收集行业情报"""
        intelligence = {
            'keywords': keywords,
            'period': f"{days} days",
            'tweets': [],
            'top_influencers': [],
            'sentiment': {},
            'emerging_topics': []
        }
        
        for keyword in keywords:
            # 搜索相关推文
            tweets = await self.search_tweets(keyword, max_results=100)
            intelligence['tweets'].extend(tweets)
            
            # 分析情感
            intelligence['sentiment'][keyword] = self._analyze_sentiment(tweets)
        
        # 识别意见领袖
        intelligence['top_influencers'] = self._identify_influencers(
            intelligence['tweets']
        )
        
        # 发现新兴话题
        intelligence['emerging_topics'] = self._extract_topics(
            intelligence['tweets']
        )
        
        return intelligence
    
    def _analyze_sentiment(self, tweets: list) -> dict:
        """简单情感分析"""
        # 这里可以集成更复杂的情感分析
        positive_words = ['good', 'great', 'excellent', 'amazing', 'love']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst']
        
        sentiment = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        for tweet in tweets:
            text = tweet['text'].lower()
            pos_count = sum(1 for word in positive_words if word in text)
            neg_count = sum(1 for word in negative_words if word in text)
            
            if pos_count > neg_count:
                sentiment['positive'] += 1
            elif neg_count > pos_count:
                sentiment['negative'] += 1
            else:
                sentiment['neutral'] += 1
        
        return sentiment
    
    def _identify_influencers(self, tweets: list) -> list:
        """识别意见领袖"""
        from collections import defaultdict
        
        author_metrics = defaultdict(lambda: {'tweets': 0, 'total_engagement': 0})
        
        for tweet in tweets:
            author = tweet['author_id']
            metrics = tweet['metrics']
            engagement = metrics['like_count'] + metrics['retweet_count'] + metrics['reply_count']
            
            author_metrics[author]['tweets'] += 1
            author_metrics[author]['total_engagement'] += engagement
        
        # 按参与度排序
        sorted_influencers = sorted(
            author_metrics.items(),
            key=lambda x: x[1]['total_engagement'],
            reverse=True
        )
        
        return [
            {
                'author_id': author,
                'tweets': data['tweets'],
                'engagement': data['total_engagement']
            }
            for author, data in sorted_influencers[:10]
        ]

# 使用
intel = IndustryIntelligence(client)
result = await intel.collect_intelligence(
    ["AI", "Machine Learning", "OpenAI"],
    days=7
)
```

## 高级用法

### 流式 API (实时监控)

```python
import tweepy.streaming

class TweetStreamListener(tweepy.StreamingClient):
    """流式推文监听"""
    
    def on_tweet(self, tweet):
        print(f"New tweet: {tweet.text}")
        # 处理推文
        
    def on_error(self, status):
        print(f"Error: {status}")

# 使用
stream = TweetStreamListener(bearer_token=os.getenv('TWITTER_BEARER_TOKEN'))
stream.add_rules(tweepy.StreamRule("OpenClaw"))
stream.filter()
```

### 用户分析

```python
async def analyze_user(username: str) -> dict:
    """分析用户档案"""
    user = client.get_user(username=username, user_fields=['public_metrics', 'created_at'])
    
    # 获取用户推文
    tweets = client.get_users_tweets(
        user.data.id,
        max_results=100,
        tweet_fields=['public_metrics', 'created_at']
    )
    
    analysis = {
        'username': username,
        'followers': user.data.public_metrics['followers_count'],
        'following': user.data.public_metrics['following_count'],
        'total_tweets': user.data.public_metrics['tweet_count'],
        'recent_activity': len(tweets.data) if tweets.data else 0,
        'avg_engagement': self._calculate_avg_engagement(tweets.data) if tweets.data else 0
    }
    
    return analysis
```

## 与 OpenClaw 集成

```python
# 在 OpenClaw 中监控 Twitter
async def twitter_monitoring_task():
    """Twitter 监控任务"""
    
    monitor = BrandMonitor(client, ["OpenClaw", "Clawdbot"])
    
    # 运行 1 小时
    await asyncio.wait_for(
        monitor.monitor_mentions(interval=60),
        timeout=3600
    )
```

## 最佳实践

### 1. 速率限制处理

```python
import time

class RateLimitHandler:
    """处理 API 速率限制"""
    
    def __init__(self):
        self.last_request_time = 0
        self.min_interval = 1  # 秒
    
    async def make_request(self, func, *args, **kwargs):
        """带速率限制的请求"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            await asyncio.sleep(self.min_interval - elapsed)
        
        try:
            result = await func(*args, **kwargs)
            self.last_request_time = time.time()
            return result
        except tweepy.TooManyRequests:
            print("Rate limited, waiting 15 minutes...")
            await asyncio.sleep(900)  # 15 分钟
            return await self.make_request(func, *args, **kwargs)
```

### 2. 数据存储

```python
import json
from datetime import datetime

class TweetDatabase:
    """推文数据库"""
    
    def __init__(self, db_path: str = "tweets.json"):
        self.db_path = db_path
    
    def save_tweets(self, tweets: list):
        """保存推文"""
        with open(self.db_path, 'a') as f:
            for tweet in tweets:
                record = {
                    'id': tweet['id'],
                    'text': tweet['text'],
                    'created_at': tweet['created_at'].isoformat(),
                    'saved_at': datetime.now().isoformat()
                }
                f.write(json.dumps(record) + '\n')
```

## 相关技能

- [bird](../bird/SKILL.md) - X/Twitter CLI (已有基础功能)
- [content-research-writer](../content-research-writer/SKILL.md) - 内容写作
- [get-tldr](../get-tldr/SKILL.md) - 文章总结
- [slack](../slack/SKILL.md) - 通知集成

---

*"Social listening is not just monitoring, it's understanding the pulse of the conversation."*
