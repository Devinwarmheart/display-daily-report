#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 生成日报模块 - 调用通义千问生成显示行业专业日报
"""

import json
import os
import requests
from datetime import datetime

def load_news():
    """加载原始新闻"""
    news_path = os.path.join(os.path.dirname(__file__), '..', 'raw_news.json')
    with open(news_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def format_news(news_list, limit=30):
    """格式化新闻列表 - 优化为紧凑格式"""
    formatted = []
    for i, news in enumerate(news_list[:limit], 1):
        # 紧凑格式：减少冗余文本
        formatted.append(f"{i}. [{news['source']}] {news['title']} | {news['summary'][:150]}...")
    return "\n".join(formatted)

def generate_display_industry_report(news_items):
    """生成显示行业专业日报 - 使用 Coding Plan API"""
    
    # 构建 Prompt (优化版 - 支持 30 条新闻)
    prompt = f"""
你是显示行业资深分析师，请根据以下{len(news_items)}条新闻生成专业日报。

【新闻列表】
{format_news(news_items, 30)}

请生成 HTML 格式日报，结构如下：

1. 📊 今日要闻 (3-5 条最重要)
2. 🏭 面板行业 (京东方/TCL 华星/LG/Samsung)
3. 🎞️ 偏光片行业
4. 🛡️ 表面处理膜行业
5. 📺 显示技术 (LCD/OLED/Mini LED/Micro LED)
6. 📱 应用市场 (手机/电视/车载/VR)
7. 💰 市场数据
8. 🌏 其他地区

要求：
- 日文/英文新闻翻译成中文
- 每条包含：标题 + 摘要 (100-150 字) + 来源 + 重要度 (⭐⭐⭐/⭐⭐/⭐) + 链接
- 专业术语准确
- HTML 格式，清晰排版，关键数字高亮

用中文输出，专业风格。
"""
    
    # 调用通义千问 Coding Plan API
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    api_url = "https://coding.dashscope.aliyuncs.com/v1/chat/completions"
    
    print(f"Calling Qwen API: {api_url}")
    print(f"API Key: {api_key[:10]}...{api_key[-5:] if api_key else 'NONE'}")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "qwen3.5-plus",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 6000  # 增加输出长度
    }
    
    try:
        print(f"Sending request with {len(news_items)} news items (timeout: 450s)...")
        response = requests.post(api_url, headers=headers, json=payload, timeout=450)
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            return content
        else:
            print(f"Error Response: {response.text}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

if __name__ == "__main__":
    # 加载新闻
    news = load_news()
    print(f"Loaded {len(news)} news items")
    
    # 生成日报
    report = generate_display_industry_report(news)
    
    if report:
        # 保存报告
        output_path = os.path.join(os.path.dirname(__file__), '..', 'report.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Report saved to {output_path}")
    else:
        print("Failed to generate report")
        exit(1)
