#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网站构建模块 - 生成 GitHub Pages 静态文件
"""

import os
import shutil
from datetime import datetime
from pathlib import Path

def get_today_date():
    """获取今天日期"""
    return datetime.now().strftime("%Y-%m-%d")

def create_directory_structure():
    """创建目录结构"""
    docs_dir = Path(__file__).parent.parent / "docs"
    daily_dir = docs_dir / "daily"
    assets_dir = docs_dir / "assets"
    
    docs_dir.mkdir(exist_ok=True)
    daily_dir.mkdir(exist_ok=True)
    assets_dir.mkdir(exist_ok=True)
    
    return docs_dir, daily_dir, assets_dir

def copy_report(daily_dir):
    """复制日报到 daily 目录"""
    today = get_today_date()
    report_src = Path(__file__).parent.parent / "report.html"
    report_dest = daily_dir / f"{today}.html"
    
    if report_src.exists():
        shutil.copy(report_src, report_dest)
        print(f"Copied report to {report_dest}")
        return today
    else:
        print("Report not found!")
        return None

def generate_index_html(today_date):
    """生成首页 HTML"""
    
    index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>显示行业 AI 日报</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans SC", sans-serif;
            background: #f5f7fa;
            color: #2c3e50;
            line-height: 1.6;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 20px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        .header h1 {{ 
            font-size: 36px; 
            margin-bottom: 10px;
            font-weight: 700;
        }}
        .header p {{ 
            font-size: 18px; 
            opacity: 0.95;
            font-weight: 300;
        }}
        .date-badge {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 8px 20px;
            border-radius: 20px;
            margin-top: 15px;
            font-size: 14px;
        }}
        
        /* 搜索框 */
        .search-container {{
            max-width: 600px;
            margin: -30px auto 30px;
            padding: 0 20px;
            position: relative;
            z-index: 10;
        }}
        .search-box {{
            width: 100%;
            padding: 18px 30px;
            border: none;
            border-radius: 50px;
            font-size: 16px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.12);
            outline: none;
            transition: box-shadow 0.3s;
        }}
        .search-box:focus {{
            box-shadow: 0 8px 35px rgba(102,126,234,0.4);
        }}
        
        /* 内容区 */
        .container {{ 
            max-width: 1000px; 
            margin: 0 auto; 
            padding: 20px; 
        }}
        
        /* 今日日报 */
        .today-section {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }}
        .today-section h2 {{
            color: #667eea;
            margin-bottom: 25px;
            font-size: 28px;
            border-left: 5px solid #667eea;
            padding-left: 15px;
        }}
        .today-frame {{
            width: 100%;
            min-height: 1200px;
            border: none;
            border-radius: 10px;
        }}
        
        /* 历史归档 */
        .archive-section {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }}
        .archive-section h2 {{
            color: #667eea;
            margin-bottom: 25px;
            font-size: 28px;
            border-left: 5px solid #667eea;
            padding-left: 15px;
        }}
        .archive-list {{
            list-style: none;
        }}
        .archive-list li {{
            padding: 15px 0;
            border-bottom: 1px solid #f0f0f0;
            transition: background 0.2s;
        }}
        .archive-list li:hover {{
            background: #f9f9f9;
        }}
        .archive-list a {{
            color: #2c3e50;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
            display: block;
        }}
        .archive-list a:hover {{ 
            color: #667eea; 
        }}
        .archive-date {{
            color: #95a5a6;
            font-size: 14px;
            margin-left: 15px;
            font-weight: 400;
        }}
        
        /* 搜索结果 */
        .search-results {{
            display: none;
            margin-top: 20px;
            background: #f9f9f9;
            border-radius: 15px;
            padding: 25px;
        }}
        .search-results h3 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 20px;
        }}
        .search-result-item {{
            padding: 15px;
            border-bottom: 1px solid #e0e0e0;
            background: white;
            border-radius: 8px;
            margin-bottom: 10px;
        }}
        .search-result-item:last-child {{
            border-bottom: none;
        }}
        .search-result-item h4 {{
            color: #667eea;
            margin-bottom: 8px;
            font-size: 16px;
        }}
        .search-result-item h4 a {{
            color: inherit;
            text-decoration: none;
        }}
        .search-result-item h4 a:hover {{
            text-decoration: underline;
        }}
        .search-result-item p {{
            color: #666;
            font-size: 14px;
            line-height: 1.7;
        }}
        
        /* 页脚 */
        .footer {{
            text-align: center;
            padding: 40px 20px;
            color: #95a5a6;
            font-size: 14px;
        }}
        .footer a {{
            color: #667eea;
            text-decoration: none;
        }}
        
        /* 响应式 */
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 28px; }}
            .header p {{ font-size: 16px; }}
            .today-section, .archive-section {{ padding: 25px; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📺 显示行业 AI 日报</h1>
        <p>Display Industry Daily Report</p>
        <div class="date-badge">📅 每日更新 · 多语言新闻 · 专业摘要</div>
    </div>
    
    <div class="search-container">
        <input type="text" class="search-box" id="searchInput" placeholder="🔍 搜索历史日报 (关键词：面板、OLED、偏光片...)">
    </div>
    
    <div class="container">
        <!-- 今日日报 -->
        <div class="today-section">
            <h2>📅 今日日报 <span style="font-size: 18px; color: #95a5a6; font-weight: normal;">{today_date}</span></h2>
            <iframe class="today-frame" src="daily/{today_date}.html" frameborder="0"></iframe>
        </div>
        
        <!-- 搜索结果 -->
        <div class="archive-section search-results" id="searchResults" style="display: none;">
            <h3>🔍 搜索结果</h3>
            <div id="resultsContent"></div>
        </div>
        
        <!-- 历史归档 -->
        <div class="archive-section">
            <h2>📁 历史归档</h2>
            <ul class="archive-list" id="archiveList">
                <li style="text-align: center; color: #95a5a6; padding: 30px;">加载中...</li>
            </ul>
        </div>
    </div>
    
    <div class="footer">
        <p>Powered by AI · Data from global display industry sources</p>
        <p style="margin-top: 10px;">
            <a href="https://github.com/yourname/display-daily-report" target="_blank">GitHub</a> · 
            每天 7:00 自动更新
        </p>
    </div>
    
    <script>
        // 加载搜索索引和历史归档
        let searchIndex = [];
        
        fetch('search.json')
            .then(r => r.json())
            .then(data => {{
                searchIndex = data;
                renderArchive(data);
            }})
            .catch(err => {{
                console.error('Error loading search index:', err);
                document.getElementById('archiveList').innerHTML = 
                    '<li style="text-align: center; color: #95a5a6; padding: 30px;">暂无历史数据</li>';
            }});
        
        // 渲染归档列表
        function renderArchive(data) {{
            const list = document.getElementById('archiveList');
            if (data.length === 0) {{
                list.innerHTML = '<li style="text-align: center; color: #95a5a6; padding: 30px;">暂无历史数据</li>';
                return;
            }}
            
            // 按日期倒序排列
            data.sort((a, b) => new Date(b.date) - new Date(a.date));
            
            list.innerHTML = data.map(item => `
                <li>
                    <a href="${{item.url}}">${{item.title}}</a>
                    <span class="archive-date">${{item.date}}</span>
                </li>
            `).join('');
        }}
        
        // 搜索功能
        document.getElementById('searchInput').addEventListener('input', function(e) {{
            const query = e.target.value.toLowerCase().trim();
            const resultsDiv = document.getElementById('searchResults');
            const resultsContent = document.getElementById('resultsContent');
            
            if (query.length < 2) {{
                resultsDiv.style.display = 'none';
                return;
            }}
            
            const results = searchIndex.filter(item => 
                item.title.toLowerCase().includes(query) ||
                (item.content && item.content.toLowerCase().includes(query))
            );
            
            if (results.length > 0) {{
                resultsContent.innerHTML = results.map(item => `
                    <div class="search-result-item">
                        <h4><a href="${{item.url}}">${{item.title}}</a></h4>
                        <p>${{item.content ? item.content.substring(0, 200) + '...' : '无摘要'}}</p>
                    </div>
                `).join('');
                resultsDiv.style.display = 'block';
            }} else {{
                resultsDiv.style.display = 'none';
            }}
        }});
    </script>
</body>
</html>
"""
    
    return index_html

def build_search_index(daily_dir):
    """构建搜索索引"""
    import re
    
    search_data = []
    
    # 遍历所有历史日报
    for html_file in sorted(daily_dir.glob("*.html")):
        date = html_file.stem  # YYYY-MM-DD
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取纯文本 (简单版)
            text = re.sub(r'<[^>]+>', ' ', content)
            text = text.replace('\n', ' ').strip()
            text = ' '.join(text.split())[:2000]  # 限制长度
            
            search_data.append({
                "date": date,
                "url": f"daily/{date}.html",
                "title": f"显示行业日报 {date}",
                "content": text
            })
        except Exception as e:
            print(f"Error processing {html_file}: {e}")
    
    # 保存搜索索引
    search_path = Path(__file__).parent.parent / "docs" / "search.json"
    with open(search_path, 'w', encoding='utf-8') as f:
        json.dump(search_data, f, ensure_ascii=False, indent=2)
    
    print(f"Built search index with {len(search_data)} articles")
    return search_data

if __name__ == "__main__":
    import json
    
    # 创建目录
    docs_dir, daily_dir, assets_dir = create_directory_structure()
    
    # 复制今日日报
    today = copy_report(daily_dir)
    
    if today:
        # 生成首页
        index_html = generate_index_html(today)
        index_path = docs_dir / "index.html"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_html)
        print(f"Generated index.html")
        
        # 构建搜索索引
        build_search_index(daily_dir)
        
        print("Site build complete!")
    else:
        print("Failed to build site (no report)")
