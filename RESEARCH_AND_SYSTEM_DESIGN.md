# 全球科技与投资资讯追踪系统 — 调研与架构设计

> 目标：每天追踪互联网科技、加密货币、能源科技、半导体、美股投资五大领域的权威资讯，通过 AI 综合分析，识别行业趋势、美股多空影响、低估标的和低资金门槛的科技创业方向。

---

## 一、五大领域权威资讯来源总览

### 1. 互联网/科技 (Internet & Technology)

| 来源 | 类型 | 权威度 | 及时性 | 付费墙 | 说明 |
|------|------|--------|--------|--------|------|
| **MIT Technology Review** | 深度分析 | ⭐⭐⭐⭐⭐ | 中 | 部分 | 最权威的科技趋势分析，AI/生物/计算 |
| **IEEE Spectrum** | 工程技术 | ⭐⭐⭐⭐⭐ | 中 | 免费 | 工程级深度，半导体/能源/AI |
| **Ars Technica** | 深度科技 | ⭐⭐⭐⭐⭐ | 高 | 免费 | 技术细节最深的主流科技媒体 |
| **TechCrunch** | 创投新闻 | ⭐⭐⭐⭐ | 高 | 免费 | 创业公司/融资/产品发布 |
| **The Verge** | 消费科技 | ⭐⭐⭐⭐ | 高 | 免费 | 消费者科技/政策/文化 |
| **Wired** | 科技文化 | ⭐⭐⭐⭐ | 中 | 部分 | 科技对社会的影响 |
| **Hacker News** | 社区聚合 | ⭐⭐⭐⭐ | 极高 | 免费 | 开发者/创业者视角，最实时 |
| **TLDR Newsletter** | 每日精选 | ⭐⭐⭐⭐ | 极高 | 免费 | 每日人工精选科技摘要，是最佳起点 |
| **Techmeme** | 新闻聚合 | ⭐⭐⭐⭐ | 极高 | 免费 | 算法聚合重要科技新闻 |
| **The Information** | 独家深度 | ⭐⭐⭐⭐⭐ | 中 | 付费 | 硅谷最深入的独家报道 |
| **Bloomberg Tech** | 金融+科技 | ⭐⭐⭐⭐⭐ | 高 | 部分 | 科技商业/政策/反垄断 |
| **Stratechery (Ben Thompson)** | 战略分析 | ⭐⭐⭐⭐⭐ | 中 | 付费 | 科技战略分析标杆 |
| **arXiv.org** | 学术预印本 | ⭐⭐⭐⭐⭐ | 极高 | 免费 | CS/AI 最前沿研究论文 |

### 2. 加密货币/区块链 (Cryptocurrency & Blockchain)

| 来源 | 类型 | 权威度 | 及时性 | 付费墙 | 说明 |
|------|------|--------|--------|--------|------|
| **CoinDesk** | 新闻+数据 | ⭐⭐⭐⭐⭐ | 极高 | 免费 | 行业标杆，BTC/ETH 价格锚定 |
| **The Block** | 深度研究 | ⭐⭐⭐⭐⭐ | 高 | 部分 | 最深入的链上/协议研究 |
| **Messari** | 研究+数据 | ⭐⭐⭐⭐⭐ | 高 | 付费 | 机构级 crypto 研究 |
| **Decrypt** | 新闻 | ⭐⭐⭐⭐ | 高 | 免费 | 通俗易懂的 crypto 新闻 |
| **Cointelegraph** | 新闻 | ⭐⭐⭐⭐ | 极高 | 免费 | 覆盖面广 |
| **Bankless** | DeFi 分析 | ⭐⭐⭐⭐ | 高 | 免费 | DeFi 领域最权威 |
| **Glassnode** | 链上数据 | ⭐⭐⭐⭐⭐ | 高 | 付费 | 链上分析金标准 |
| **Dune Analytics** | 链上数据 | ⭐⭐⭐⭐⭐ | 高 | 免费 | 社区驱动的链上数据平台 |
| **CoinGecko** | 市场数据 | ⭐⭐⭐⭐ | 极高 | 免费 | 最全面的 crypto 市场数据 |
| **CoinMarketCap** | 市场数据 | ⭐⭐⭐⭐ | 极高 | 免费 | 市值排名权威 |
| **CryptoCompare** | 数据+分析 | ⭐⭐⭐⭐ | 高 | 免费 | 机构级数据 |
| **Blockchain.com** | 区块数据 | ⭐⭐⭐⭐ | 高 | 免费 | 最早的区块链浏览器 |

### 3. 能源科技 (Energy Technology)

| 来源 | 类型 | 权威度 | 及时性 | 付费墙 | 说明 |
|------|------|--------|--------|--------|------|
| **IEA (国际能源署)** | 数据+报告 | ⭐⭐⭐⭐⭐ | 中 | 部分 | 全球能源数据金标准 |
| **EIA (美国能源信息署)** | 政府数据 | ⭐⭐⭐⭐⭐ | 高 | 免费 | 美国最全面的能源数据 |
| **Bloomberg NEF** | 研究分析 | ⭐⭐⭐⭐⭐ | 中 | 付费 | 能源转型研究最权威 |
| **NREL (国家可再生能源实验室)** | 技术研究 | ⭐⭐⭐⭐⭐ | 中 | 免费 | 太阳能/风能/储能技术 |
| **Reuters Energy** | 新闻 | ⭐⭐⭐⭐ | 高 | 部分 | 能源大宗商品新闻 |
| **Canary Media** | 清洁能源 | ⭐⭐⭐⭐ | 高 | 免费 | 专注清洁能源转型 |
| **Utility Dive** | 电力行业 | ⭐⭐⭐⭐ | 高 | 免费 | 美国电力行业新闻 |
| **Electrek** | EV+清洁能源 | ⭐⭐⭐⭐ | 极高 | 免费 | EV/太阳能/储能 |
| **PV Magazine** | 光伏产业 | ⭐⭐⭐⭐ | 高 | 免费 | 太阳能行业垂直媒体 |
| **OilPrice.com** | 能源市场 | ⭐⭐⭐ | 极高 | 免费 | 油气/能源大宗商品 |
| **S&P Global Commodity Insights** | 能源数据 | ⭐⭐⭐⭐⭐ | 高 | 付费 | 机构级能源数据 |
| **Wood Mackenzie** | 能源咨询 | ⭐⭐⭐⭐⭐ | 中 | 付费 | 能源行业咨询标杆 |

### 4. 半导体 (Semiconductor)

| 来源 | 类型 | 权威度 | 及时性 | 付费墙 | 说明 |
|------|------|--------|--------|--------|------|
| **IEEE Spectrum** | 技术深度 | ⭐⭐⭐⭐⭐ | 中 | 免费 | 芯片技术最深度的工程报道 |
| **SemiEngineering** | 工程深度 | ⭐⭐⭐⭐⭐ | 高 | 免费 | 芯片设计/制造/封装全链条 |
| **AnandTech** | 硬件评测 | ⭐⭐⭐⭐⭐ | 中 | 免费 | CPU/GPU/SoC 最深度评测 |
| **DigiTimes** | 供应链 | ⭐⭐⭐⭐ | 极高 | 付费 | 台湾/亚洲芯片供应链一手信息 |
| **EE Times** | 电子工程 | ⭐⭐⭐⭐⭐ | 高 | 免费 | 电子工程行业老牌媒体 |
| **SIA (半导体行业协会)** | 行业数据 | ⭐⭐⭐⭐⭐ | 中 | 免费 | 美国半导体行业官方数据 |
| **SEMI** | 制造设备 | ⭐⭐⭐⭐⭐ | 中 | 部分 | 芯片制造设备和材料 |
| **TrendForce** | 市场研究 | ⭐⭐⭐⭐ | 中 | 付费 | 存储器/面板/芯片市场数据 |
| **Nikkei Asia** | 亚洲芯片 | ⭐⭐⭐⭐⭐ | 高 | 部分 | 亚洲半导体产业最权威 |
| **Tom's Hardware** | 硬件新闻 | ⭐⭐⭐⭐ | 高 | 免费 | PC/芯片消费者视角 |
| **IC Insights** | 市场研究 | ⭐⭐⭐⭐ | 低 | 付费 | 芯片市场排名/预测 |
| **WCCF Tech** | 硬件泄漏 | ⭐⭐⭐ | 极高 | 免费 | 芯片/GPU 传闻和泄漏 |

### 5. 美股/投资 (US Stocks & Investment)

| 来源 | 类型 | 权威度 | 及时性 | 付费墙 | 说明 |
|------|------|--------|--------|--------|------|
| **SEC EDGAR** | 官方文件 | ⭐⭐⭐⭐⭐ | 高 | 免费 | 10-K/10-Q/8-K 官方来源 |
| **Bloomberg** | 财经终端 | ⭐⭐⭐⭐⭐ | 极高 | 付费 | 机构投资者标准配置 |
| **Reuters** | 财经新闻 | ⭐⭐⭐⭐⭐ | 极高 | 部分 | 全球财经通讯社 |
| **WSJ** | 财经新闻 | ⭐⭐⭐⭐⭐ | 高 | 付费 | 美国商业/金融标杆 |
| **Financial Times** | 全球财经 | ⭐⭐⭐⭐⭐ | 高 | 付费 | 全球视角的财经分析 |
| **CNBC** | 实时财经 | ⭐⭐⭐⭐ | 极高 | 免费 | 实时市场报道 |
| **Yahoo Finance** | 数据+新闻 | ⭐⭐⭐⭐ | 极高 | 免费 | 最广泛使用的免费财经平台 |
| **MarketWatch** | 市场新闻 | ⭐⭐⭐⭐ | 高 | 免费 | 道琼斯旗下市场新闻 |
| **Seeking Alpha** | 众包分析 | ⭐⭐⭐ | 高 | 部分 | 投资者社区分析 |
| **Barron's** | 投资分析 | ⭐⭐⭐⭐⭐ | 中 | 付费 | 深度投资分析 |
| **Morningstar** | 基金研究 | ⭐⭐⭐⭐⭐ | 低 | 部分 | 基金/股票基本面研究 |
| **FRED (美联储)** | 经济数据 | ⭐⭐⭐⭐⭐ | 高 | 免费 | 最权威的美国经济数据库 |
| **Benzinga** | 市场动态 | ⭐⭐⭐ | 极高 | 部分 | 市场异动/内幕交易 |

---

## 二、免费/有免费额度的 API 汇总

以下是经过验证的、可编程调用的免费 API 清单。

### A. 综合新闻类 API

| API | 免费额度 | 限制 | 覆盖范围 | 备注 |
|-----|---------|------|---------|------|
| **NewsAPI** | 100 req/天 | 24小时延迟，1个月历史 | 80,000+ 来源，含科技/商业类别 | 最易用的新闻聚合 API |
| **Mediastack** | 100 req/月 | 延迟数据 | 7,500+ 来源，50+ 国家 | 支持分类过滤 |
| **Hacker News API** | 无限 | 无 Key 需要 | 科技/创业社区，实时 | 官方 API，GitHub 开源 |
| **Reddit API** | 60 req/分钟 | OAuth | 所有 Subreddit | r/technology, r/cryptocurrency, r/stocks 等 |
| **The Guardian API** | 免费注册 | 无限 | 卫报全内容 | 深度调查报道 |
| **NYT Developer API** | 免费 | ~500 req/天 | 纽约时报 | Article Search, Top Stories |
| **GNews API** | 100 req/天 | - | Google 新闻聚合 | 支持多语言、多国家 |
| **TLDR Newsletter (非官方)** | 无限 (RSS + /api/latest/) | 无 Key 需要 | 科技/AI/Crypto 等 14+ 主题每日精选 | RSS 标准化；/api/latest/{topic} 返回完整内容 |

### B. 加密货币类 API

| API | 免费额度 | 限制 | 数据类型 | 备注 |
|-----|---------|------|---------|------|
| **CoinGecko API** | 30 req/分钟，10,000/月 | 免费 Key 可选 | 价格/市值/交易所/链上/NFT | 最全面的免费 crypto API |
| **CoinMarketCap API** | 有限免费 | 需要 Key | 价格/市值/排名 | 基础数据免费 |
| **CoinDesk BPI** | 无限 | 无需 Key | 比特币价格指数 | 最权威的 BTC 价格 |
| **CoinPaprika API** | 无限 | 无需 Key | 价格/交易所/ICO | 覆盖 3000+ 币种 |
| **Coinlore API** | 无限 | 无需 Key | 价格/市值/排名 | 极简的免费 API |
| **CryptoCompare API** | 100,000 req/月 | 免费 Key | 价格/新闻/交易数据 | 新闻接口很有价值 |
| **Etherscan API** | 5 req/秒 | 免费 Key | 以太坊链上数据 | ETH 生态必用 |
| **Blockchain.com API** | 有限 | 免费 Key | BTC 区块/交易/地址 | 最早的区块链 API |

### C. 股票/金融类 API

| API | 免费额度 | 限制 | 数据类型 | 备注 |
|-----|---------|------|---------|------|
| **Alpha Vantage** | 25 req/天 | 免费 Key | 股票/外汇/加密/技术指标/经济/新闻情绪 | 覆盖面最广的免费金融 API |
| **Finnhub** | 60 req/分钟 | 免费 Key | 实时报价/基本面/新闻/内幕交易/经济数据 | 新闻+基本面免费 |
| **Yahoo Finance (yfinance)** | 无限 | 非官方 Python 库 | 历史/报价/基本面/新闻 | 最方便的免费方案 |
| **Marketstack** | 100 req/月 | EOD 数据 | 全球 70+ 交易所 | 1年历史 |
| **Polygon.io** | 5 req/分钟 | 免费 Key | 实时/历史/新闻 | 延迟数据免费 |
| **IEX Cloud** | 免费额度 | 免费 Key | 美国股票实时数据 | IEX 交易所官方 |
| **SEC EDGAR API** | 无限 | 无需 Key | 10-K/10-Q/8-K/13F | 官方 API，最权威 |
| **FRED API** | 无限 | 免费 Key | 美国宏观经济全系列 | 美联储官方 |
| **Tiingo** | 有限免费 | 免费 Key | 股票/ETF 历史和实时 | 数据质量高 |
| **Twelve Data** | 8 req/分钟，800/天 | 免费 Key | 股票/外汇/加密/技术指标 | 延迟数据 |
| **Financial Modeling Prep** | 有限免费 | 免费 Key | 基本面/财务数据 | 适合价值分析 |

### D. 能源类 API

| API | 免费额度 | 限制 | 数据类型 | 备注 |
|-----|---------|------|---------|------|
| **EIA Open Data API** | 无限 | 免费 Key | 美国能源全系列数据 | 官方最权威 |
| **NREL Developer API** | 有限免费 | 免费 Key | 太阳能辐射/风能/生物质 | 技术数据 |
| **ElectricityMap API** | 免费层 | 免费 Key | 全球电网碳排放实时数据 | 碳强度追踪 |
| **Open Charge Map API** | 有限免费 | 免费 Key | 全球 EV 充电站数据 | EV 基础设施 |
| **OpenAQ API** | 无限 | 无需 Key | 全球空气质量 | 环境相关 |

### E. 学术/研究类 API

| API | 免费额度 | 限制 | 数据类型 | 备注 |
|-----|---------|------|---------|------|
| **arXiv API** | 无限 | 无需 Key | CS/AI/物理预印本 | 前沿研究追踪 |
| **Semantic Scholar API** | 无限 | 免费 Key | 学术论文+引用+影响力 | AI 驱动的学术搜索 |
| **CrossRef API** | 无限 | 无需 Key | 学术 DOI 元数据 | 学术出版数据库 |
| **PubMed API** | 无限 | 无需 Key | 生物医学论文 | 健康/生物科技 |

---

## 二-B、三大核心免费 API 详解

这三个 API 是系统最重要的免费实时信号源，以下逐一展开。

### 🔴 Hacker News API — 科技/创投社区实时信号

**官方 API 地址**：`https://github.com/HackerNews/API`
**Base URL**：`https://hacker-news.firebaseio.com/v0/`
**认证**：无需 API Key，完全开放
**速率限制**：无限（Firebase 托管，无官方限制）
**数据格式**：JSON

**核心端点**：

| 端点 | 说明 | 用途 |
|------|------|------|
| `/topstories.json` | 当前 Top 500 故事 ID 列表 | 每日必拉，获取当天最热科技新闻 |
| `/newstories.json` | 最新 500 故事 ID 列表 | 实时追踪，发现早期信号 |
| `/beststories.json` | 最佳故事 ID 列表 | 高质量内容筛选 |
| `/askstories.json` | Ask HN 问题列表 | 创业者/开发者关注的话题 |
| `/showstories.json` | Show HN 展示列表 | 新产品/项目发布，创业灵感 |
| `/jobstories.json` | 招聘信息列表 | 行业人才需求风向标 |
| `/item/{id}.json` | 单个条目详情（含评论） | 获取标题/链接/正文/评论树 |
| `/user/{id}.json` | 用户信息 | 追踪特定 KOL 的动态 |
| `/updates.json` | 最近更新的条目和用户 | 增量更新，减少重复拉取 |

**对我们系统的价值 — 五大领域覆盖**：

| 领域 | HN 覆盖度 | 说明 |
|------|----------|------|
| 互联网/科技 | ⭐⭐⭐⭐⭐ | 核心覆盖，AI/编程/产品/创业 |
| 加密货币 | ⭐⭐⭐⭐ | 区块链/Web3/DeFi 讨论活跃 |
| 能源科技 | ⭐⭐⭐ | 核聚变/太阳能/储能时有深度讨论 |
| 半导体 | ⭐⭐⭐ | 芯片架构/制造工艺的技术讨论 |
| 美股/投资 | ⭐⭐⭐ | 科技公司财报/IPO/VC 融资讨论 |

**实战调用示例**：

```python
import asyncio
import aiohttp

BASE = "https://hacker-news.firebaseio.com/v0"

async def fetch_top_stories(limit=50):
    """拉取 Top 50 故事的标题、链接和评分"""
    async with aiohttp.ClientSession() as session:
        # 1. 获取 top stories ID 列表
        async with session.get(f"{BASE}/topstories.json") as resp:
            ids = await resp.json()

        # 2. 并发获取每个 story 的详情
        tasks = []
        for sid in ids[:limit]:
            tasks.append(fetch_item(session, sid))
        stories = await asyncio.gather(*tasks)
        return [s for s in stories if s is not None]

async def fetch_item(session, item_id):
    async with session.get(f"{BASE}/item/{item_id}.json") as resp:
        return await resp.json()

async def fetch_stories_with_comments(session, stories, min_score=50, min_comments=30):
    """筛选高互动内容：评分>=50 且评论>=30"""
    return [
        s for s in stories
        if s.get("score", 0) >= min_score
        and s.get("descendants", 0) >= min_comments
    ]

# 增量更新策略
async def fetch_updates():
    """只拉取最近更新的条目，避免全量重拉"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE}/updates.json") as resp:
            data = await resp.json()
            # data["items"] = 最近更新的条目 ID
            # data["profiles"] = 最近更新的用户 ID
            return data["items"]
```

**关键使用策略**：
- **Top Stories** 每小时拉一次（故事排序变化快）
- **New Stories** 每 15 分钟拉一次（捕捉早期信号）
- **评论挖掘**：高评分+高评论的故事，评论本身常含深度分析和反对意见
- **关键词过滤**：标题/评论中匹配 "AI", "LLM", "chip", "semiconductor", "solar", "crypto", "IPO", "acquisition" 等
- **Show HN** 是创业灵感金矿：每天能看到社区用户发布的创新产品

---

### 🔴 Reddit API — 社区情绪与实时讨论信号

**官方 API 文档**：`https://www.reddit.com/dev/api/`
**认证方式**：OAuth2（需注册 Reddit App，免费）
**速率限制**：60 req/分钟（免费，OAuth 认证后）；10 req/分钟（未认证）
**数据格式**：JSON

**认证配置**：
1. 前往 `https://www.reddit.com/prefs/apps` 创建 "script" 类型 App
2. 获取 `client_id` 和 `client_secret`
3. 使用 OAuth2 获取 bearer token

**核心端点**：

| 端点 | 说明 | 用途 |
|------|------|------|
| `/r/{subreddit}/hot.json` | 热门帖子 | 每日必拉 |
| `/r/{subreddit}/new.json` | 最新帖子 | 实时信号 |
| `/r/{subreddit}/top.json?t=day` | 今日最佳 | 每日精华 |
| `/r/{subreddit}/rising.json` | 正在上升的帖子 | 趋势检测 |
| `/r/{subreddit}/comments/{post_id}.json` | 帖子评论 | 深度舆情 |
| `/search.json?q={query}&restrict_sr=on` | 子版搜索 | 关键词追踪 |
| `/api/info.json?id={id}` | 获取特定帖子/评论 | 增量拉取 |

**五大领域对应的核心 Subreddit**：

```
# ── 互联网/科技 ──
r/technology          # 1500万+ 成员，综合科技新闻
r/programming         #  600万+ 成员，开发者社区
r/MachineLearning     #  300万+ 成员，AI/ML 前沿
r/artificial          #  AI 综合讨论
r/singularity         #  AGI/未来学讨论
r/startups            #  创业讨论
r/webdev              #  Web 开发趋势
r/opensource          #  开源项目

# ── 加密货币 ──
r/CryptoCurrency      #  800万+ 成员，crypto 综合
r/Bitcoin             #  600万+ 成员，BTC 专注
r/ethereum            #  300万+ 成员，ETH 生态
r/defi                #  DeFi 深度讨论
r/CryptoTechnology    #  Crypto 技术层面
r/ethdev              #  ETH 开发者

# ── 能源科技 ──
r/energy              #  能源行业综合
r/solar               #  太阳能
r/electricvehicles    #  EV 产业
r/teslamotors         #  Tesla 讨论（EV 风向标）
r/nuclear             #  核能
r/RenewableEnergy     #  可再生能源
r/Futurology          #  未来趋势（含能源）

# ── 半导体 ──
r/hardware            # 硬件综合
r/Amd                 # AMD 讨论
r/intel               # Intel 讨论
r/nvidia              # NVIDIA 讨论
r/chipdesign          # 芯片设计
r/FPGA                # FPGA
r/semiconductors      # 半导体（成员较少但专业）

# ── 美股/投资 ──
r/investing           # 投资综合
r/stocks              # 美股讨论
r/StockMarket         # 股市
r/wallstreetbets      # 市场情绪极端信号
r/SecurityAnalysis    # 价值投资（格雷厄姆风格）
r/dividends           # 股息投资
r/SPACs               # SPAC 动态
r/Economics           # 宏观经济
```

**实战调用示例**：

```python
import aiohttp
import asyncio

# Reddit API 认证
AUTH = aiohttp.BasicAuth("YOUR_CLIENT_ID", "YOUR_CLIENT_SECRET")
USER_AGENT = "NewsTracker/1.0 (by /u/YOUR_USERNAME)"

async def get_reddit_token(session):
    """获取 OAuth2 Bearer Token"""
    data = {
        "grant_type": "client_credentials",
    }
    headers = {"User-Agent": USER_AGENT}
    async with session.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=AUTH,
        data=data,
        headers=headers,
    ) as resp:
        result = await resp.json()
        return result["access_token"]

async def fetch_subreddit_posts(session, token, subreddit, listing="hot", limit=25):
    """拉取指定 subreddit 的帖子"""
    headers = {
        "Authorization": f"bearer {token}",
        "User-Agent": USER_AGENT,
    }
    url = f"https://oauth.reddit.com/r/{subreddit}/{listing}.json?limit={limit}"
    async with session.get(url, headers=headers) as resp:
        data = await resp.json()
        posts = []
        for child in data["data"]["children"]:
            p = child["data"]
            posts.append({
                "id": p["id"],
                "title": p["title"],
                "selftext": p.get("selftext", "")[:500],  # 前 500 字符
                "score": p["score"],
                "num_comments": p["num_comments"],
                "upvote_ratio": p.get("upvote_ratio", 0),
                "url": p.get("url", ""),
                "permalink": f"https://reddit.com{p['permalink']}",
                "created_utc": p["created_utc"],
                "author": p["author"],
                "flair": p.get("link_flair_text", ""),
                "subreddit": p["subreddit"],
                "is_self": p["is_self"],
            })
        return posts

# 批量拉取所有目标 subreddits
TARGET_SUBS = [
    "technology", "programming", "MachineLearning",
    "CryptoCurrency", "Bitcoin", "ethereum",
    "energy", "electricvehicles", "solar",
    "hardware", "nvidia", "Amd",
    "investing", "stocks", "StockMarket",
]

async def batch_fetch_all(session, token):
    """并发拉取所有目标 subreddits"""
    tasks = [
        fetch_subreddit_posts(session, token, sub, listing="hot", limit=20)
        for sub in TARGET_SUBS
    ]
    all_results = await asyncio.gather(*tasks, return_exceptions=True)

    aggregated = []
    for sub, posts in zip(TARGET_SUBS, all_results):
        if isinstance(posts, list):
            for post in posts:
                post["source_subreddit"] = sub
            aggregated.extend(posts)
    return aggregated

# 趋势检测：发现正在快速上升的话题
async def detect_trending(session, token):
    """拉取 rising 排序的帖子，发现趋势信号"""
    tasks = []
    for sub in TARGET_SUBS:
        tasks.append(
            fetch_subreddit_posts(session, token, sub, listing="rising", limit=10)
        )
    results = await asyncio.gather(*tasks, return_exceptions=True)
    # rising 中的高 upvote_ratio 帖子 = 即将爆发的信号
    trending = []
    for posts in results:
        if isinstance(posts, list):
            trending.extend([p for p in posts if p["upvote_ratio"] > 0.85])
    return sorted(trending, key=lambda x: x["score"], reverse=True)
```

**关键使用策略**：
- **upvote_ratio** (< 0.7) = 有争议，可能有反对观点值得看
- **评论区挖掘**：高评分帖子的 top 评论常比原文更有洞察
- **flair 标签**：很多子版有标签系统（如 `r/CryptoCurrency` 的 "TECHNOLOGY", "EXCHANGES", "SECURITY"）
- **跨子版对比**：同一新闻在不同子版的讨论角度不同（如芯片突破在 r/hardware vs r/investing）
- **WallStreetBets 独立处理**：r/wallstreetbets 的信号噪声比极低，需要独立的情感过滤管道

---

### 🔴 NewsAPI.org — 全球新闻聚合搜索

**官方文档**：`https://newsapi.org/docs`
**Base URL**：`https://newsapi.org/v2/`
**认证**：API Key（免费注册）
**免费额度**：100 req/天，24小时延迟，1个月历史
**付费价格**：$449/月起（商业使用）
**数据格式**：JSON

**核心端点**：

| 端点 | 免费版 | 说明 |
|------|--------|------|
| `GET /v2/top-headlines` | ✅ 100 req/天 | 按国家/分类/关键词获取头条 |
| `GET /v2/everything` | ✅ 100 req/天 | 全文搜索新闻，1个月历史 |
| `GET /v2/sources` | ✅ 100 req/天 | 获取可用新闻源列表 |

**支持的分类**：`business`, `entertainment`, `general`, `health`, `science`, `sports`, `technology`

**五大领域搜索策略**：

```python
import aiohttp
import asyncio

API_KEY = "YOUR_NEWSAPI_KEY"
BASE_URL = "https://newsapi.org/v2"

async def fetch_domain_news(session, domain_config):
    """按领域配置拉取新闻"""
    all_articles = []

    for config in domain_config:
        params = {
            "apiKey": API_KEY,
            "pageSize": 30,  # 免费版最大 100
            "language": "en",
        }

        if config["type"] == "top-headlines":
            url = f"{BASE_URL}/top-headlines"
            if "category" in config:
                params["category"] = config["category"]
            if "q" in config:
                params["q"] = config["q"]
        else:
            url = f"{BASE_URL}/everything"
            params["q"] = config["q"]
            params["sortBy"] = config.get("sortBy", "publishedAt")

        async with session.get(url, params=params) as resp:
            data = await resp.json()
            if data["status"] == "ok":
                for article in data["articles"]:
                    article["_domain"] = config["domain"]
                    article["_query"] = config.get("label", config["q"])
                all_articles.extend(data["articles"])

    return all_articles

# 五大领域搜索配置
DOMAIN_CONFIGS = [
    # ── 互联网/科技 ──
    {
        "domain": "tech",
        "type": "top-headlines",
        "category": "technology",
        "label": "Tech Headlines"
    },
    {
        "domain": "tech",
        "type": "everything",
        "q": "(AI OR \"artificial intelligence\" OR LLM OR \"large language model\") AND (launch OR breakthrough OR release)",
        "sortBy": "publishedAt",
        "label": "AI Breakthroughs"
    },
    {
        "domain": "tech",
        "type": "everything",
        "q": "\"startup\" OR \"raised\" OR \"Series A\" OR \"venture capital\"",
        "sortBy": "publishedAt",
        "label": "Startup Funding"
    },

    # ── 加密货币 ──
    {
        "domain": "crypto",
        "type": "everything",
        "q": "(Bitcoin OR Ethereum OR crypto OR blockchain OR DeFi) AND (regulation OR ETF OR halving OR upgrade OR hack)",
        "sortBy": "publishedAt",
        "label": "Crypto Major Events"
    },
    {
        "domain": "crypto",
        "type": "everything",
        "q": "\"stablecoin\" OR \"CBDC\" OR \"SEC crypto\" OR \"crypto regulation\"",
        "sortBy": "publishedAt",
        "label": "Crypto Regulation"
    },

    # ── 能源科技 ──
    {
        "domain": "energy",
        "type": "everything",
        "q": "(\"solar power\" OR \"wind energy\" OR \"nuclear fusion\" OR \"battery storage\" OR \"green hydrogen\") AND (breakthrough OR record OR innovation)",
        "sortBy": "publishedAt",
        "label": "Clean Energy Tech"
    },
    {
        "domain": "energy",
        "type": "everything",
        "q": "(\"electric vehicle\" OR \"EV battery\" OR \"solid state battery\") AND (launch OR production OR factory)",
        "sortBy": "publishedAt",
        "label": "EV & Battery"
    },
    {
        "domain": "energy",
        "type": "everything",
        "q": "\"carbon capture\" OR \"nuclear reactor\" OR \"fusion energy\" OR \"geothermal\"",
        "sortBy": "publishedAt",
        "label": "Next-Gen Energy"
    },

    # ── 半导体 ──
    {
        "domain": "semiconductor",
        "type": "everything",
        "q": "(semiconductor OR chip OR foundry OR fab) AND (TSMC OR Intel OR Samsung OR NVIDIA OR AMD OR ASML)",
        "sortBy": "publishedAt",
        "label": "Chip Industry"
    },
    {
        "domain": "semiconductor",
        "type": "everything",
        "q": "\"chip manufacturing\" OR \"advanced packaging\" OR \"lithography\" OR \"3nm\" OR \"2nm\" OR \"EUV\"",
        "sortBy": "publishedAt",
        "label": "Chip Manufacturing"
    },
    {
        "domain": "semiconductor",
        "type": "everything",
        "q": "(\"GPU\" OR \"AI chip\" OR \"HBM\" OR \"memory chip\") AND (NVIDIA OR AMD OR \"SK Hynix\" OR Micron)",
        "sortBy": "publishedAt",
        "label": "AI Chips & Memory"
    },

    # ── 美股/投资 ──
    {
        "domain": "investing",
        "type": "top-headlines",
        "category": "business",
        "label": "Business Headlines"
    },
    {
        "domain": "investing",
        "type": "everything",
        "q": "(\"earnings report\" OR \"beat estimates\" OR \"missed estimates\" OR \"guidance\") AND (stock OR shares OR NASDAQ OR \"S&P 500\")",
        "sortBy": "publishedAt",
        "label": "Earnings Reports"
    },
    {
        "domain": "investing",
        "type": "everything",
        "q": "(\"merger\" OR \"acquisition\" OR \"IPO\" OR \"spin-off\" OR \"buyback\") AND (billion OR million)",
        "sortBy": "publishedAt",
        "label": "M&A and IPO"
    },
    {
        "domain": "investing",
        "type": "everything",
        "q": "(\"Fed\" OR \"Federal Reserve\" OR \"interest rate\" OR \"inflation\" OR \"CPI\") AND (decision OR outlook OR forecast)",
        "sortBy": "publishedAt",
        "label": "Macro & Fed"
    },
]

async def daily_newsapi_fetch():
    """每日 NewsAPI 采集（注意 100 req/天的限制）"""
    async with aiohttp.ClientSession() as session:
        articles = await fetch_domain_news(session, DOMAIN_CONFIGS)

        # 去重（按 title 相似度）
        seen = set()
        unique = []
        for a in articles:
            key = a.get("title", "")[:80].lower()
            if key and key not in seen:
                seen.add(key)
                unique.append(a)
        return unique
```

**NewsAPI 使用注意事项**：
- **100 req/天限制**：上述示例共 ~14 个查询配置，剩 86 个补充请求
- **24 小时延迟**：免费版文章有延迟，不适用于日内实时交易
- **内容截断**：API 返回的 `content` 字段被截断，需点 `url` 阅读全文
- **source 过滤**：可用 `/sources` 端点预先筛选高质量的科技/财经源
- **付费墙内容**：WSJ、FT 等付费源的文章也会出现在结果中，但只返回摘要
- **开发模式**：API Key 只能在 localhost 使用，生产环境需购买付费计划

---

### 🔴 TLDR Newsletter — 人工精选每日科技摘要

**网站**：`https://tldr.tech`
**RSS**：`https://tldr.tech/rss`（标准化 XML，无限拉取）
**非官方 API**：`https://tldr.tech/api/latest/{topic}`（返回完整 HTML 内容）
**认证**：无需任何认证
**速率限制**：无明显限制
**数据格式**：RSS 为 XML；`/api/latest/` 返回 HTML（需解析）

**TLDR 系列 Newsletter 覆盖**：

| 主题 | RSS/API | 对我们系统的价值 | 订阅人数 |
|------|---------|-----------------|---------|
| **TLDR** (主刊) | `/rss`, `/api/latest/tech` | 科技+创业+编程综合精选 | 160 万+ |
| **TLDR AI** | `/api/latest/ai` | AI/ML 每日精选 | 92 万+ |
| **TLDR Crypto** | `/api/latest/crypto` | Crypto/Web3 每日精选 | 50 万+ |
| **TLDR Fintech** | `/api/latest/fintech` | 金融科技 | 10 万+ |
| **TLDR DevOps** | `/api/latest/devops` | 基础设施/云 | - |
| **TLDR InfoSec** | `/api/latest/infosec` | 安全技术 | - |
| **TLDR Design** | `/api/latest/design` | 设计/UX | - |
| **TLDR Marketing** | `/api/latest/marketing` | 营销科技 | - |
| **TLDR Hardware** | 即将上线 | 半导体/芯片（最期待） | 即将 |
| **另有**：Web Dev, Mobile Dev, Product, Engineering, Founders 等 |

**对我们五大领域的覆盖**：

| 领域 | TLDR 对应 | 覆盖度 |
|------|----------|--------|
| 互联网/科技 | TLDR (主刊), TLDR AI, TLDR Web Dev | ⭐⭐⭐⭐⭐ |
| 加密货币 | TLDR Crypto, TLDR Fintech | ⭐⭐⭐⭐⭐ |
| 能源科技 | TLDR (主刊) 偶有涉及 | ⭐⭐⭐ |
| 半导体 | TLDR Hardware（即将） | ⭐⭐ (待上线) |
| 美股/投资 | TLDR Fintech | ⭐⭐⭐ |

**实战调用示例**：

```python
import aiohttp
import asyncio
import feedparser  # pip install feedparser
from bs4 import BeautifulSoup  # pip install beautifulsoup4
import re

# ── 方法 1: RSS Feed（推荐，结构化数据）──
async def fetch_tldr_rss():
    """通过 RSS 获取 TLDR 主刊最新内容"""
    url = "https://tldr.tech/rss"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            rss_content = await resp.text()

    # feedparser 是同步的，在 asyncio 中用 run_in_executor
    loop = asyncio.get_event_loop()
    feed = await loop.run_in_executor(None, feedparser.parse, rss_content)

    articles = []
    for entry in feed.entries:
        articles.append({
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": entry.get("summary", ""),
            "category": entry.get("category", ""),
            "source": "TLDR",
        })
    return articles

# ── 方法 2: /api/latest/ 端点（内容更完整）──
TLDR_TOPICS = {
    "tech": "TLDR (主刊)",
    "ai": "TLDR AI",
    "crypto": "TLDR Crypto",
    "fintech": "TLDR Fintech",
    "devops": "TLDR DevOps",
    "infosec": "TLDR InfoSec",
}

async def fetch_tldr_topic(session, topic):
    """通过 /api/latest/{topic} 获取指定主题的完整内容"""
    url = f"https://tldr.tech/api/latest/{topic}"
    async with session.get(url) as resp:
        if resp.status != 200:
            return None
        html = await resp.text()

    soup = BeautifulSoup(html, "html.parser")

    # 提取日期
    date_el = soup.find("h2")
    date_str = date_el.text.strip() if date_el else ""

    # 提取各板块文章
    sections = []
    current_section = None
    current_articles = []

    for elem in soup.find_all(["h3", "p", "a"]):
        if elem.name == "h3":
            # 保存上一个 section
            if current_section and current_articles:
                sections.append({
                    "section": current_section,
                    "articles": current_articles,
                })
            current_section = elem.text.strip()
            current_articles = []
        elif elem.name == "a" and elem.get("href"):
            href = elem["href"]
            # 过滤掉 sponsor/nav/subscribe 链接
            if "tldr.tech" not in href and "mailto:" not in href:
                text = elem.text.strip()
                if text and len(text) > 10:
                    current_articles.append({
                        "title": text,
                        "url": href,
                    })

    # 保存最后一个 section
    if current_section and current_articles:
        sections.append({"section": current_section, "articles": current_articles})

    return {
        "topic": TLDR_TOPICS.get(topic, topic),
        "date": date_str,
        "sections": sections,
    }

async def fetch_all_tldr_topics():
    """并发拉取所有 TLDR 主题"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_tldr_topic(session, t) for t in TLDR_TOPICS]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    all_data = {}
    for topic, result in zip(TLDR_TOPICS, results):
        if isinstance(result, dict):
            all_data[topic] = result
    return all_data

# ── 方法 3: RSS 获取所有可用的 TLDR RSS 订阅 ──
TLDR_RSS_FEEDS = {
    "tech": "https://tldr.tech/rss",
    # 其他主题可能也有 RSS，尝试同名路径
    # 已验证 /rss 返回主刊，其他主题当前以 /api/latest/ 为主
}

async def extract_tldr_articles_combined():
    """
    综合方案：
    1. RSS 获取主刊（结构化、稳定）
    2. /api/latest/ 获取垂直主题（内容更丰富但需 HTML 解析）
    """
    articles = []

    # RSS 获取主刊
    rss_articles = await fetch_tldr_rss()
    for a in rss_articles:
        a["source_topic"] = "tech"
    articles.extend(rss_articles)

    # HTML 解析获取垂直主题
    topic_data = await fetch_all_tldr_topics()
    for topic, data in topic_data.items():
        for section in data.get("sections", []):
            for art in section.get("articles", []):
                articles.append({
                    "title": art["title"],
                    "link": art["url"],
                    "published": data.get("date", ""),
                    "summary": section["section"],
                    "source": f"TLDR {TLDR_TOPICS.get(topic, topic)}",
                    "source_topic": topic,
                })

    # 去重（按 URL）
    seen_urls = set()
    unique = []
    for a in articles:
        url = a.get("link", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique.append(a)
    return unique
```

**TLDR 的独特价值**：

1. **人工精选**：与算法聚合（HN/Reddit）不同，TLDR 是真人编辑筛选的最重要新闻
2. **高质量摘要**：每条新闻都有编辑写好的 2-5 句摘要，可直接喂给 AI
3. **覆盖广度**：主刊+AI+Crypto 三个订阅就覆盖了系统最核心的 3 个领域
4. **作为"基准信号"**：如果一条新闻同时出现在 TLDR + HN + Reddit，那就是当日最重要的信号
5. **零成本**：无需 API Key，RSS 标准格式，解析极简

**使用注意事项**：
- `/api/latest/` 是非官方端点，URL 结构可能变化（RSS 更稳定）
- HTML 解析依赖页面结构，建议加异常处理和降级到 RSS
- TLDR 有 sponsor 广告内容，需过滤
- 内容每日更新一次（早上 EST），每天拉取 1-2 次即可
- RSS 只覆盖主刊；垂直主题（AI/Crypto 等）需用 `/api/latest/` 端点

---

### 四大 API 协作策略

```
时间线                    数据源                    目的
──────────────────────────────────────────────────────────
05:00   TLDR 拉取          拉取主刊 RSS + AI/Crypto  获取编辑精选，作为基准信号
05:30   HN /newstories     拉取过去12小时的新提交     捕捉夜间（美西时间）新信号
06:00   HN /topstories     拉取当前 Top 100          获取当日最重要的科技讨论
07:00   Reddit 批量拉取     拉取15+子版 hot+rising    获取社区情绪和趋势
07:30   NewsAPI 批量搜索    拉取14个配置的新闻        获取专业媒体新闻
08:00   ── AI 综合分析 ──   整合四大来源             去重、关联、生成上午简报
10:00   Reddit rising      增量拉取 rising            捕捉日间新出现的趋势
12:00   HN /topstories     对比早上排名的变化         发现日间热度迁移
14:00   NewsAPI 补充搜索    用新发现的关键词补充搜索   追踪突发事件
16:00   Reddit 日内更新    拉取各子版 top?t=day      获取当日最佳帖子
18:00   ── 晚间 AI 总结 ──  整合全天数据             生成晚间简报
```

**信号权重设计**（用于去重排序时的评分）：

| 信号 | 权重 | 说明 |
|------|------|------|
| TLDR + HN + Reddit 三源共振 | 15 分 | 最强信号：编辑+社区+媒体同时确认 |
| HN Top 10 故事 | 10 分 | 科技圈最认可的内容 |
| TLDR 编辑精选 | 9 分 | 专业编辑判断为重要 |
| HN 评分 > 100 | 8 分 | 高价值内容 |
| Reddit 帖子 > 1000 upvotes | 7 分 | 社区高度认可 |
| Reddit 多子版同时讨论 | 9 分 | 跨社区共振信号 |
| NewsAPI 被多家媒体报道 | 8 分 | 主流媒体确认的信号 |
| 四大源同时出现 | +5 分加成 | 最强的信号确认 |

---

## 三、API 优先级排序（按实用性综合评估）

结合覆盖面、数据质量、免费额度和调用便利性，推荐以下 API 作为系统核心：

### Tier 1 — 核心必备（免费额度充足，覆盖关键领域）

1. **TLDR Newsletter** (RSS + /api/latest/) — 编辑精选每日摘要，最佳起点信号
2. **Hacker News API** — 科技/创投社区最实时信号
3. **CoinGecko API** — 最全面的免费 crypto 数据
4. **Yahoo Finance (yfinance)** — 美股数据最方便方案
5. **Alpha Vantage** — 多资产数据+技术指标+新闻情绪
6. **SEC EDGAR API** — 官方公司文件
7. **FRED API** — 宏观经济数据
8. **EIA Open Data API** — 能源数据权威
9. **arXiv API** — 前沿科研追踪

### Tier 2 — 强力补充（有免费额度但有限制）

10. **Finnhub** — 新闻+基本面+内幕交易
11. **CryptoCompare API** — crypto 新闻+数据
12. **NewsAPI** — 综合新闻搜索
13. **Reddit API** — 社区情绪信号
14. **Mediastack** — 多源新闻聚合
15. **Twelve Data** — 备用股票数据

### Tier 3 — 按需扩展

16. **Polygon.io** — 更实时的美股数据
17. **The Guardian / NYT API** — 深度报道
18. **Semantic Scholar** — 学术引用追踪
19. **NREL API** — 可再生能源技术数据

---

## 四、系统架构设计

### 整体架构图

```
┌──────────────────────────────────────────────────────┐
│                    调度层 (Scheduler)                   │
│              Apache Airflow / Prefect / Cron           │
└──────────┬───────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────┐
│                数据采集层 (Ingestion)                    │
│                                                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ News APIs│ │Crypto APIs│ │Stock APIs│ │Energy APIs│ │
│  │TLDR API  │ │CoinGecko │ │yfinance  │ │EIA Open  │ │
│  │NewsAPI   │ │CC Compare│ │Alpha Van │ │NREL      │ │
│  │HN API    │ │CoinPaprika│ │Finnhub   │ │ElecMap   │ │
│  │Reddit    │ │Etherscan │ │SEC EDGAR │ │          │ │
│  │Mediastack│ │          │ │          │ │          │ │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ │
└───────┼────────────┼────────────┼────────────┼───────┘
        │            │            │            │
        ▼            ▼            ▼            ▼
┌──────────────────────────────────────────────────────┐
│              数据处理层 (Processing)                    │
│                                                        │
│  ┌──────────────────┐  ┌──────────────────┐          │
│  │ 数据清洗/Normalize│  │ 去重 Dedup       │          │
│  └────────┬─────────┘  └────────┬─────────┘          │
│           │                     │                     │
│  ┌────────▼─────────────────────▼─────────┐          │
│  │         实体识别 (NER)                    │          │
│  │  公司名/股票代码/人物/技术关键词/产品      │          │
│  └────────┬───────────────────────────────┘          │
│           │                                          │
│  ┌────────▼───────────────────────────────┐          │
│  │       关联映射 (Linking)                  │          │
│  │  新闻 → 股票代码 → 行业 → 赛道           │          │
│  └────────┬───────────────────────────────┘          │
│           │                                          │
│  ┌────────▼───────────────────────────────┐          │
│  │       情感分析 (Sentiment)                │          │
│  │  正面/负面/中性 + 影响程度评分            │          │
│  └────────────────────────────────────────┘          │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│                存储层 (Storage)                         │
│                                                        │
│  ┌──────────────────┐  ┌──────────────────┐          │
│  │   PostgreSQL      │  │   ChromaDB/      │          │
│  │   结构化数据       │  │   Qdrant         │          │
│  │   新闻/价格/财务   │  │   向量存储        │          │
│  │   关系型查询       │  │   语义搜索        │          │
│  └──────────────────┘  └──────────────────┘          │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│                AI 分析层 (AI Analysis)                  │
│                                                        │
│  ┌─────────────────────────────────────┐             │
│  │  每日摘要生成 (DeepSeek / Claude)     │             │
│  │  - 五大领域 Top 10 新闻摘要          │             │
│  │  - 跨领域关联分析                    │             │
│  │  - 趋势识别和预测                    │             │
│  └──────────────┬──────────────────────┘             │
│                 │                                     │
│  ┌──────────────▼──────────────────────┐             │
│  │  投资影响分析 (DeepSeek / Claude)     │             │
│  │  - 新闻 → 相关股票映射               │             │
│  │  - 利多/利空判断 + 置信度            │             │
│  │  - 影响时间维度（短期/中期/长期）      │             │
│  │  - 情绪变化趋势追踪                  │             │
│  └──────────────┬──────────────────────┘             │
│                 │                                     │
│  ┌──────────────▼──────────────────────┐             │
│  │  价值发现引擎 (DeepSeek / Claude)     │             │
│  │  - 低估标的识别（P/E, P/B, PEG等）   │             │
│  │  - 催化事件匹配（技术突破→受益股）    │             │
│  │  - 赛道轮动分析                      │             │
│  │  - 风险提示                          │             │
│  └──────────────┬──────────────────────┘             │
│                 │                                     │
│  ┌──────────────▼──────────────────────┐             │
│  │  创业机会识别 (DeepSeek / Claude)     │             │
│  │  - 技术趋势 → 商业机会映射           │             │
│  │  - 低资金门槛方向筛选                │             │
│  │  - 竞争格局分析                      │             │
│  │  - 时间窗口评估                      │             │
│  └─────────────────────────────────────┘             │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│                输出层 (Output)                          │
│                                                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ 每日邮件  │ │Web 仪表盘│ │ 移动推送  │ │ API 接口  │ │
│  │ Markdown │ │Streamlit │ │Telegram  │ │ REST API │ │
│  │ HTML邮件 │ │ /Next.js│ │ Bot通知  │ │ 供扩展   │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
└──────────────────────────────────────────────────────┘
```

### 技术栈推荐

| 层级 | 技术选型 | 理由 |
|------|---------|------|
| **调度** | Python + APScheduler (轻量) 或 Prefect (生产级) | 免费开源，Python 生态 |
| **数据采集** | Python + aiohttp + asyncio | 异步并发获取，效率高 |
| **数据清洗** | Pandas + Pydantic | 数据转换和验证 |
| **实体识别** | spaCy + 自定义规则 | 轻量 NER，提取公司名/股票代码 |
| **情感分析** | DeepSeek API | 比传统 NLP 库准确得多 |
| **数据库** | SQLite (MVP) → PostgreSQL + pgvector | 结构化+向量搜索一体 |
| **缓存** | Redis (可选) | API 缓存，减少重复请求 |
| **AI 引擎** | DeepSeek v4-pro | 输入 $0.435/M token, 输出 $0.87/M token |
| **仪表盘** | Streamlit | 最快搭建数据看板 |
| **部署** | 本地运行 / Docker + VPS | 轻量部署 |

### 数据流设计

```
每天北京时间 07:00 (美东 19:00)
         │
         ▼
┌─────────────────────┐
│ 1. 定时触发采集任务   │  cron: 0 7 * * *
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ 2. 并发拉取所有 API   │  asyncio.gather()
│    20+ APIs 并行     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ 3. 数据清洗+去重     │  pandas + dedup
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ 4. NER 实体提取      │  spaCy Ner
│    公司→股票→行业    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ 5. AI 综合分析 (Claude)│
│  - 各领域摘要        │
│  - 跨领域关联        │
│  - 投资影响评估      │
│  - 机会发现          │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ 6. 生成每日报告      │  
│  - 保存到数据库      │
│  - 发送邮件/推送     │
│  - 更新仪表盘        │
└─────────────────────┘
```

### 数据库核心表设计

```sql
-- 原始新闻
news_articles (
    id, source, url, title, summary, content_preview,
    published_at, fetched_at, category, language,
    sentiment_score, impact_score, unique_hash
)

-- 实体-新闻关联
entity_mentions (
    id, article_id, entity_name, entity_type (COMPANY|TICKER|PERSON|TECH|PRODUCT),
    ticker, sector, relevance_score
)

-- 市场数据
market_data (
    id, ticker, date, open, high, low, close, volume,
    source, fetched_at
)

-- 每日摘要
daily_briefs (
    id, date, domain,
    top_stories (JSONB),
    summary (TEXT),           -- AI 生成的摘要
    market_impact (JSONB),     -- 对美股的影响分析
    opportunities (JSONB),     -- 发现的机会
    raw_ai_response (TEXT),    -- 原始 AI 输出
    created_at
)

-- 追踪标的
watched_stocks (
    ticker, company_name, sector, subsector,
    watch_reason, added_at, last_reviewed_at
)

-- AI 分析历史
ai_insights (
    id, date, insight_type,
    content, related_tickers, related_news_ids,
    confidence_score, created_at
)
```

### 每日 AI Prompt 框架

系统会构建以下结构化的 Prompt 发送给 Claude：

```
## 角色
你是世界顶级的科技和投资分析师，拥有深度科技背景和华尔街分析经验。

## 今日资讯
[按领域组织的今日 Top 新闻，每条含：来源/标题/摘要/关联股票]

## 历史背景
[过去7天相关新闻汇总]
[相关股票近期表现]

## 分析任务
1. **每日要点**（每领域 3-5 条最关键动态，用中文总结）
2. **跨领域关联**（识别跨领域的技术趋势交汇点）
3. **美股影响分析**（列出受影响股票，判断利多/利空/中性，给出置信度）
4. **低估标的发现**（结合技术趋势+基本面，发现可能被低估的标的）
5. **创业机会识别**（识别低资金门槛、超前的科技创业方向）
6. **风险预警**（需要关注的负面信号）

## 输出格式
结构化 JSON，便于前端渲染和存储。
```

### 成本估算

| 项目 | 月成本 | 说明 |
|------|-------|------|
| VPS (可选) | ~$20 | Hetzner/DigitalOcean，本地运行则为 $0 |
| 新闻 API 源 | $0 | 全部使用免费额度 |
| AI 分析 (DeepSeek v4-pro) | <$1 | 输入 $0.435/M token, 输出 $0.87/M token (折扣价)。每次运行约 $0.01-0.02，每日两次约 $0.02-0.04/天 |

唯一实质花费是 DeepSeek API 调用，成本取决于每日运行次数和新闻量。

---

## 五、实施路线图

### Phase 1 — 最小可行产品 (MVP) — 1-2 周

- [ ] 搭建 Python 项目结构
- [ ] 接入 7 个 Tier 1 API (TLDR, HN, CoinGecko, yfinance, Alpha Vantage, SEC EDGAR, FRED)
- [ ] 实现基础数据采集和存储 (SQLite 即可)
- [ ] 编写 Claude API 调用脚本，生成每日摘要
- [ ] Markdown/文本格式的每日邮件输出

### Phase 2 — 增强分析 — 3-4 周

- [ ] 添加 Tier 2 API (TLDR 垂直主题, Finnhub, CryptoCompare, NewsAPI, Reddit)
- [ ] 切换到 PostgreSQL
- [ ] 实现实体识别 (NER) 和股票映射
- [ ] AI 情感分析管线
- [ ] 结构化 JSON 输出
- [ ] Streamlit 仪表盘

### Phase 3 — 智能化 — 5-8 周

- [ ] 向量数据库 + 语义搜索 (历史相似事件查找)
- [ ] 趋势时间序列分析
- [ ] 自动化估值模型集成
- [ ] Telegram Bot 实时推送
- [ ] 历史回测：AI 分析的准确性追踪

---

## 六、关键注意事项

1. **API 限流管理**：需要实现速率限制器，避免被 Ban。建议用 Redis 做令牌桶。
2. **数据版权**：不要全文存储付费源内容，只存摘要和链接。
3. **AI 幻觉控制**：所有 AI 输出标注"仅供参考，不构成投资建议"，重要结论需关联源链接。
4. **时区处理**：美股交易时间、亚洲/欧洲市场时间不同，采集时间需考虑信息时效。
5. **渐进增强**：先跑通核心流程，再逐步添加 API 源和分析模块。
6. **回测验证**：定期回溯 AI 的历史判断准确率，持续优化 Prompt。
