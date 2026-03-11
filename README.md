# 📺 显示行业 AI 日报 (Display Industry Daily Report)

自动收集显示行业、面板、偏光片、表面处理膜行业的全球新闻，AI 生成详细摘要日报。

## 🎯 功能特点

- **多语言新闻源**: 中文 + 日文 + 英文
- **AI 详细摘要**: 每条新闻 150-250 字摘要
- **专业分类**: 面板/偏光片/表面处理膜/显示技术
- **自动发布**: 每天早上 7 点 (北京时间) 自动更新
- **搜索功能**: 可搜索所有历史日报
- **GitHub Pages 托管**: 免费、稳定、自动部署

## 📁 项目结构

```
display-daily-report/
├── .github/workflows/daily-report.yml  # GitHub Actions 配置
├── src/
│   ├── fetch_news.py          # 新闻收集
│   ├── generate_report.py     # AI 生成日报
│   ├── build_site.py          # 网站生成
│   └── build_search.py        # 搜索索引
├── config/sources.json        # 新闻源配置
├── docs/                      # GitHub Pages 输出
└── requirements.txt           # Python 依赖
```

## 🚀 部署步骤

### 1. Fork/创建仓库

```bash
# 创建新仓库
github.com/yourname/display-daily-report
```

### 2. 配置 Secrets

在 GitHub 仓库 Settings → Secrets and variables → Actions 中添加：

```
DASHSCOPE_API_KEY=sk-xxx  # 通义千问 API Key
```

### 3. 启用 GitHub Pages

Settings → Pages → Source: GitHub Actions

### 4. 测试运行

Actions → 手动触发 "Generate Report"

### 5. 访问网站

```
https://yourname.github.io/display-daily-report/
```

## 📰 新闻源

### 中文
- 显示网、集微网、WitDisplay、中国电子报

### 日文
- 日経 xTECH、Display Bank、Impress Watch

### 英文
- Display Daily、OLED-Info、DSCC、FlatPanelHD

## ⏰ 发布时间

每天早上 7:00 (北京时间) 自动发布

## 💰 成本

- GitHub Actions: 免费 (2000 分钟/月)
- GitHub Pages: 免费
- 通义 API: 约 0.5 元/天 (新用户有免费额度)

## 📝 License

MIT
