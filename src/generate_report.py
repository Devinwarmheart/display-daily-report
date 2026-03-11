#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 生成日报模块 - 调用通义千问生成显示行业专业日报
"""

import json
import os
from datetime import datetime
from dashscope import Generation

def load_news():
    """加载原始新闻"""
    news_path = os.path.join(os.path.dirname(__file__), '..', 'raw_news.json')
    with open(news_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def format_news(news_list, limit=20):
    """格式化新闻列表"""
    formatted = []
    for i, news in enumerate(news_list[:limit], 1):
        formatted.append(f"""
[{i}] {news['title']}
    来源：{news['source']} ({news['language']})
    链接：{news['link']}
    摘要：{news['summary'][:300]}
""")
    return "\n".join(formatted)

def generate_display_industry_report(news_items):
    """生成显示行业专业日报"""
    
    # 构建 Prompt
    prompt = f"""
你是显示行业资深分析师，请根据以下新闻生成一份专业日报。

【新闻列表】(共{len(news_items)}条)
{format_news(news_items, 30)}

请按以下结构整理：

## 1. 📊 今日要闻 (⭐⭐⭐ 重要新闻，3-5 条)
   - 每条包含：标题 + 详细摘要 (200 字) + 影响分析

## 2. 🏭 面板行业动态
   - 按公司分类：京东方、TCL 华星、LG Display、Samsung Display 等
   - 包含：产能、技术、投资、合作

## 3. 🎞️ 偏光片行业
   - 原材料价格、供应商动态、技术进展

## 4. 🛡️ 表面处理膜行业
   - 新产品、技术应用、市场动态

## 5. 📺 显示技术进展
   - LCD/OLED/Mini LED/Micro LED 新技术
   - 专利、论文、研发成果

## 6. 📱 应用市场
   - 手机/电视/车载/VR 等应用领域需求

## 7. 💰 市场数据
   - 出货量、价格趋势、市场份额

## 8. 🌏 其他地区新闻
   - 中国、日本、韩国、台湾、欧美

要求：
1. 每条新闻必须包含：
   - 中文标题 (日文/英文需翻译)
   - 详细摘要 (150-250 字，包含关键数据)
   - 来源 + 原语言
   - 重要度 (⭐⭐⭐/⭐⭐/⭐)
   - 原文链接

2. 专业术语保持准确：
   - 技术名词：LCD, OLED, LTPS, IGZO, etc.
   - 公司名：保留英文 + 中文注释
   - 数据：单位统一 (如：万片/月，亿美元)

3. 输出完整 HTML 格式，要求：
   - 专业简洁的排版
   - 清晰的分类标题
   - 数据用表格展示
   - 关键数字高亮显示
   - 包含日期和总览

请用中文输出，专业严谨风格。
"""
    
    # 调用通义千问
    print("Calling Qwen API to generate report...")
    response = Generation.call(
        model="qwen-max",
        prompt=prompt,
        api_key=os.environ.get("DASHSCOPE_API_KEY")
    )
    
    if response.status_code == 200:
        return response.output.text
    else:
        print(f"Error: {response.status_code} - {response.message}")
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
