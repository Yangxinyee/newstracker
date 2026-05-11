"""
Finnhub API 数据源
免费额度: 60 req/分钟
提供实时报价、公司新闻、内幕交易、经济数据等
"""

import asyncio
from datetime import datetime

import aiohttp

from config import FINNHUB_KEY
from database import insert_articles_batch

BASE_URL = "https://finnhub.io/api/v1"


async def _call_finnhub(session: aiohttp.ClientSession, endpoint: str, **params) -> dict | None:
    p = {**params, "token": FINNHUB_KEY}
    url = f"{BASE_URL}/{endpoint}"
    try:
        async with session.get(url, params=p, timeout=15) as resp:
            if resp.status != 200:
                return None
            return await resp.json()
    except Exception:
        return None


async def fetch_company_news(session: aiohttp.ClientSession, ticker: str, category: str) -> list[dict]:
    """获取公司新闻 — Finnhub 最核心的功能"""
    today = datetime.now().strftime("%Y-%m-%d")
    from_date = (datetime.now().replace(day=datetime.now().day - 2)).strftime("%Y-%m-%d")

    data = await _call_finnhub(session, "company-news", symbol=ticker, _from=from_date, to=today)
    if not isinstance(data, list):
        return []

    articles = []
    for n in data[:10]:
        articles.append({
            "source": "Finnhub",
            "source_topic": ticker,
            "url": n.get("url", ""),
            "title": n.get("headline", ""),
            "summary": n.get("summary", "") or "",
            "published_at": datetime.fromtimestamp(n.get("datetime", 0)).isoformat() if n.get("datetime") else "",
            "category": category,
            "language": "en",
            "author": n.get("source", ""),
            "_ticker": ticker,
        })
    return articles


async def fetch_insider_transactions(session: aiohttp.ClientSession, ticker: str) -> list[dict]:
    """获取内幕交易 — 极有价值的信号"""
    today = datetime.now().strftime("%Y-%m-%d")
    from_date = (datetime.now().replace(month=datetime.now().month - 1)).strftime("%Y-%m-%d")

    data = await _call_finnhub(session, "stock/insider-transactions", symbol=ticker, _from=from_date, to=today)
    if not data or "data" not in data:
        return []

    articles = []
    for t in data["data"][:20]:
        name = t.get("name", "")
        change = t.get("change", 0)
        if abs(change) > 10000:  # 过滤小额交易
            direction = "买入" if change > 0 else "卖出"
            articles.append({
                "source": "Finnhub",
                "source_topic": "insider_trading",
                "url": f"https://finnhub.io/insider/{ticker}",
                "title": f"{ticker} 内幕交易: {name} {direction} {abs(change)} 股",
                "summary": f"{name} ({t.get('share', 0):.0f} 股) @ ${t.get('transactionPrice', 0):.2f}, 交易日期: {t.get('transactionDate', '')}",
                "published_at": t.get("transactionDate", ""),
                "category": "investing",
                "language": "en",
                "_ticker": ticker,
                "_insider_name": name,
                "_change_shares": change,
            })
    return articles


async def fetch_market_news(session: aiohttp.ClientSession) -> list[dict]:
    """获取市场综合新闻"""
    data = await _call_finnhub(session, "news", category="general")
    if not isinstance(data, list):
        return []

    articles = []
    for n in data[:30]:
        articles.append({
            "source": "Finnhub",
            "source_topic": "market_news",
            "url": n.get("url", ""),
            "title": n.get("headline", ""),
            "summary": n.get("summary", "") or "",
            "published_at": datetime.fromtimestamp(n.get("datetime", 0)).isoformat() if n.get("datetime") else "",
            "category": "investing",
            "language": "en",
            "author": n.get("source", ""),
        })
    return articles


# 核心追踪股票
FINNHUB_TRACKED = {
    "NVDA": "semiconductor", "AMD": "semiconductor", "AVGO": "semiconductor",
    "TSM": "semiconductor",
    "AAPL": "tech", "MSFT": "tech", "GOOGL": "tech", "META": "tech",
    "AMZN": "tech",
    "TSLA": "energy",
    "COIN": "crypto", "MSTR": "crypto",
    "JPM": "investing", "SPY": "investing", "QQQ": "investing",
}


async def ingest_finnhub() -> int:
    """Finnhub 数据采集"""
    if not FINNHUB_KEY:
        print("[Finnhub] 跳过 (缺少 API Key)")
        return 0

    async with aiohttp.ClientSession() as session:
        # 并行拉取: 公司新闻 (10 只), 市场新闻, 内幕交易 (10 只)
        stock_news_tasks = [
            fetch_company_news(session, t, FINNHUB_TRACKED[t])
            for t in list(FINNHUB_TRACKED.keys())[:10]
        ]
        insider_tasks = [
            fetch_insider_transactions(session, t)
            for t in list(FINNHUB_TRACKED.keys())[:10]
        ]
        market_task = fetch_market_news(session)

        all_tasks = stock_news_tasks + insider_tasks + [market_task]
        all_results = await asyncio.gather(*all_tasks, return_exceptions=True)

    all_articles = []
    for result in all_results:
        if isinstance(result, list):
            all_articles.extend(result)

    count = insert_articles_batch(all_articles)
    print(f"[Finnhub] 获取 {len(all_articles)} 条，入库 {count} 条 (含公司新闻、内幕交易、市场新闻)")
    return count
