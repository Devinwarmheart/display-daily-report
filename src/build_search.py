#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜索索引构建模块
"""

import json
import re
from pathlib import Path

def build_search_index():
    """构建搜索索引"""
    
    docs_dir = Path(__file__).parent.parent / "docs"
    daily_dir = docs_dir / "daily"
    
    search_data = []
    
    # 遍历所有历史日报
    for html_file in sorted(daily_dir.glob("*.html")):
        date = html_file.stem  # YYYY-MM-DD
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取纯文本
            text = re.sub(r'<[^>]+>', ' ', content)
            text = text.replace('\n', ' ').strip()
            text = ' '.join(text.split())[:2000]  # 限制长度
            
            search_data.append({
                "date": date,
                "url": f"daily/{date}.html",
                "title": f"显示行业日报 {date}",
                "content": text
            })
            
            print(f"Indexed: {date}")
        except Exception as e:
            print(f"Error processing {html_file}: {e}")
    
    # 保存搜索索引
    search_path = docs_dir / "search.json"
    with open(search_path, 'w', encoding='utf-8') as f:
        json.dump(search_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nBuilt search index with {len(search_data)} articles")
    return search_data

if __name__ == "__main__":
    build_search_index()
