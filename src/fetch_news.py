#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻收集模块 - 收集显示行业多语言新闻
"""

import feedparser
import json
import os
from datetime import datetime

def load_config():
    """加载新闻源配置"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'sources.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def fetch_rss(url, keywords=None, limit=30):
    """获取 RSS 源"""
    try:
        feed = feedparser.parse(url)
        items = []
        
        for entry in feed.entries[:limit]:
            title = entry.title
            
            # 关键词过滤
            if keywords:
                title_lower = title.lower()
                if not any(k.lower() in title_lower for k in keywords):
                    continue
            
            # 提取摘要
            summary = ""
            if hasattr(entry, 'summary'):
                summary = entry.summary[:500]  # 限制长度
            elif hasattr(entry, 'description'):
                summary = entry.description[:500]
            
            # 提取发布时间
            published = ""
            if hasattr(entry, 'published'):
                published = entry.published
            elif hasattr(entry, 'updated'):
                published = entry.updated
            
            items.append({
                "title": title,
                "link": entry.link,
                "summary": summary,
                "published": published,
                "language": "auto"
            })
        
        return items
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

def fetch_all_news():
    """收集所有语言新闻源"""
    config = load_config()
    all_news = []
    
    # 中文源
    for source in config.get("chinese", []):
        print(f"Fetching {source['name']}...")
        news = fetch_rss(source["url"], source.get("keywords"))
        for item in news:
            item["source"] = source["name"]
            item["language"] = "zh"
        all_news.extend(news)
    
    # 日文源
    for source in config.get("japanese", []):
        print(f"Fetching {source['name']}...")
        news = fetch_rss(source["url"], source.get("keywords"))
        for item in news:
            item["source"] = source["name"]
            item["language"] = "ja"
        all_news.extend(news)
    
    # 英文源
    for source in config.get("english", []):
        print(f"Fetching {source['name']}...")
        news = fetch_rss(source["url"], source.get("keywords"))
        for item in news:
            item["source"] = source["name"]
            item["language"] = "en"
        all_news.extend(news)
    
    # 去重 (按标题)
    seen = set()
    unique_news = []
    for item in all_news:
        if item["title"] not in seen:
            seen.add(item["title"])
            unique_news.append(item)
    
    print(f"Total collected: {len(unique_news)} unique news items")
    return unique_news

if __name__ == "__main__":
    news = fetch_all_news()
    
    # 保存为 JSON
    output_path = os.path.join(os.path.dirname(__file__), '..', 'raw_news.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(news, f, ensure_ascii=False, indent=2)
    
    print(f"Saved to {output_path}")
