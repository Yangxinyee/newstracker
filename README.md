# 📊 NewsTracker — AI-Powered Tech & Investment Intelligence

**Language:** [English](#english) | [中文](#中文)

---

<a name="english"></a>
## 🇺🇸 English

**NewsTracker** is an AI-powered daily news intelligence system that aggregates cutting-edge information across five domains — Internet/Tech, Cryptocurrency, Energy Tech, Semiconductors, and US Stocks — and uses DeepSeek AI to generate actionable daily briefings, stock impact assessments, and opportunity discovery.

### Features

- **11 News APIs** aggregated into one unified pipeline
- **AI-powered analysis** using DeepSeek v4 Pro with chain-of-thought reasoning
- **5 domains covered**: Tech, Crypto, Energy, Semiconductors, US Stocks
- **Streamlit web dashboard** for browsing and analysis
- **Scheduled automation** (daily 7:00 & 18:00 Beijing time)
- **Cost-efficient**: ~$60-150/month total (all free API tiers + AI API)

### Architecture

```
APIs (11 sources) → Ingestion → Processing (clean/dedup/NER) → SQLite
                                    ↓
                        DeepSeek AI Analysis
                                    ↓
              Markdown Report + Streamlit Dashboard
```

### Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up API keys
cp .env.example .env
# Edit .env with your keys (at minimum: DEEPSEEK_API_KEY)

# 3. Run full pipeline (ingest + AI analysis)
python main.py

# 4. Launch web dashboard
streamlit run app.py --server.port 8501
```

### API Keys Required

| API | Free Tier | Required |
|-----|-----------|----------|
| **DeepSeek** | Pay-per-use | ✅ Required for AI analysis |
| **TLDR, HackerNews, CoinGecko, Yahoo Finance, SEC EDGAR** | Unlimited/Generous | ❌ No key needed |
| **NewsAPI, Alpha Vantage, Finnhub, FRED, EIA, Reddit** | Free tiers | Optional (enhances coverage) |

### CLI Usage

```bash
python main.py                    # Full pipeline (ingest + analyze)
python main.py --ingest-only      # Only fetch data, no AI analysis
python main.py --analyze-only     # Only AI analysis on existing data
python main.py --schedule         # Start scheduled mode (auto-run daily)
python main.py --init-db          # Initialize database
```

### Project Structure

```
newstracker/
├── main.py                 # Main orchestrator
├── app.py                  # Streamlit web UI
├── config.py               # Configuration
├── database.py             # SQLite database layer
├── models.py               # Data models (Pydantic)
├── scheduler.py            # APScheduler for automation
├── ingestion/              # 11 API data sources
│   ├── tldr.py             # TLDR Newsletter (RSS)
│   ├── hackernews.py       # Hacker News
│   ├── reddit.py           # Reddit (25 subreddits)
│   ├── newsapi.py          # NewsAPI.org
│   ├── coingecko.py        # CoinGecko crypto data
│   ├── yfinance_data.py    # Yahoo Finance
│   ├── alphavantage.py     # Alpha Vantage (sentiment)
│   ├── sec_edgar.py        # SEC EDGAR filings
│   ├── fred.py             # FRED economic indicators
│   ├── eia.py              # EIA energy data
│   └── finnhub.py          # Finnhub (news + insider)
├── processing/             # Data processing pipeline
│   ├── cleaner.py          # HTML cleaning, junk filtering
│   ├── dedup.py            # Deduplication + multi-source detection
│   └── ner.py              # Entity extraction (tickers/tech keywords)
├── ai_analysis/
│   └── deepseek_client.py  # DeepSeek AI prompts + API calls
├── output/
│   └── report.py           # Markdown report generation + console output
└── data/                   # SQLite DB + reports (gitignored)
```

### Daily AI Analysis Output

1. **Domain highlights** — Top 3-5 stories per domain
2. **Cross-domain correlations** — Trend intersections (e.g., AI chips → energy demand)
3. **Stock impact** — Bullish/bearish signals for 5-10 stocks with confidence levels
4. **Undervalued targets** — 1-3 potentially undervalued opportunities
5. **Startup opportunities** — 1-3 low-capital frontier tech directions
6. **Risk alerts** — Negative signals to monitor

---

<a name="中文"></a>
## 🇨🇳 中文

**NewsTracker** 是一个 AI 驱动的每日科技与投资资讯追踪系统。它聚合五大领域（互联网/科技、加密货币、能源科技、半导体、美股投资）的前沿信息，并通过 DeepSeek AI 生成每日深度分析报告，涵盖股票多空判断、低估标的发现和科技创业机会识别。

### 核心功能

- **11 个新闻 API** 统一聚合到一条数据管道
- **DeepSeek v4 Pro AI 分析**，启用思维链深度推理
- **五大领域覆盖**：科技、加密、能源、半导体、美股
- **Streamlit Web 仪表盘**，中文界面
- **定时自动化**：每天北京时间 7:00 和 18:00 自动运行
- **极低成本**：月运营成本约 $60-150（全部使用免费 API 额度）

### 系统架构

```
11 个 API 源 → 数据采集 → 清洗/去重/实体识别 → SQLite
                              ↓
                    DeepSeek AI 分析
                              ↓
              Markdown 报告 + Streamlit 仪表盘
```

### 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 API Keys
cp .env.example .env
# 编辑 .env，至少填入 DEEPSEEK_API_KEY

# 3. 运行完整流程（采集 + AI 分析）
python main.py

# 4. 启动 Web 仪表盘
streamlit run app.py --server.port 8501
```

### 各 API Key 需求

| API | 免费额度 | 是否需要 Key |
|-----|---------|-------------|
| **DeepSeek** | 按量付费 | ✅ 必须（AI 分析核心） |
| **TLDR, HackerNews, CoinGecko, Yahoo Finance, SEC EDGAR** | 无限/充足 | ❌ 无需 Key |
| **NewsAPI, Alpha Vantage, Finnhub, FRED, EIA, Reddit** | 有免费层 | 可选（增强覆盖） |

### CLI 命令

```bash
python main.py                    # 完整流程（采集 + AI 分析）
python main.py --ingest-only      # 只采集数据
python main.py --analyze-only     # 只做 AI 分析（基于已有数据）
python main.py --schedule         # 启动定时调度（每天自动运行）
python main.py --init-db          # 初始化数据库
```

### 项目结构

```
newstracker/
├── main.py                 # 主编排器
├── app.py                  # Streamlit Web UI
├── config.py               # 全局配置
├── database.py             # SQLite 数据库层
├── models.py               # 数据模型 (Pydantic)
├── scheduler.py            # 定时调度 (APScheduler)
├── ingestion/              # 11 个 API 数据源
│   ├── tldr.py             # TLDR Newsletter (RSS)
│   ├── hackernews.py       # Hacker News
│   ├── reddit.py           # Reddit (25个子版)
│   ├── newsapi.py          # NewsAPI.org
│   ├── coingecko.py        # CoinGecko 加密货币数据
│   ├── yfinance_data.py    # Yahoo Finance
│   ├── alphavantage.py     # Alpha Vantage (新闻情绪)
│   ├── sec_edgar.py        # SEC EDGAR 公司文件
│   ├── fred.py             # FRED 宏观经济指标
│   ├── eia.py              # EIA 能源数据
│   └── finnhub.py          # Finnhub (新闻+内幕交易)
├── processing/             # 数据处理管道
│   ├── cleaner.py          # HTML清洗、垃圾过滤
│   ├── dedup.py            # 去重+多源共振检测
│   └── ner.py              # 实体识别（股票代码/技术关键词）
├── ai_analysis/
│   └── deepseek_client.py  # DeepSeek AI Prompts + API 调用
├── output/
│   └── report.py           # Markdown 报告 + 控制台输出
└── data/                   # 数据库 + 报告 (已加入 .gitignore)
```

### AI 每日分析输出

1. **每日要点** — 每个领域 3-5 条最关键动态
2. **跨领域关联** — 技术趋势交汇点分析
3. **美股影响分析** — 5-10 只股票多空判断（含置信度）
4. **低估标的发现** — 1-3 个潜在被低估的机会
5. **创业机会识别** — 1-3 个低资金门槛前沿科技方向
6. **风险预警** — 需要关注的负面信号

### 免责声明

⚠️ 本系统所有分析均由 AI 自动生成，仅供参考，**不构成投资建议**。投资有风险，决策需谨慎。

---

## 📄 License

MIT License
