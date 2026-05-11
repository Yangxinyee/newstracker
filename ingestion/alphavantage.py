"""
Alpha Vantage API 数据源
免费额度: 25 req/天
覆盖: 股票/外汇/加密/技术指标/经济数据/新闻情绪
"""

import asyncio
from datetime import datetime

import aiohttp

from config import ALPHA_VANTAGE_KEY
from database import insert_articles_batch, insert_market_data

BASE_URL = "https://www.alphavantage.co/query"


async def _call_av(session: aiohttp.ClientSession, function: str, **params) -> dict | None:
    p = {"function": function, "apikey": ALPHA_VANTAGE_KEY, **params}
    try:
        headers = {"Accept-Encoding": "gzip, deflate"}
        async with session.get(BASE_URL, params=p, timeout=15, headers=headers) as resp:
            data = await resp.json()
            if "Error Message" in data or "Note" in data:
                print(f"[AlphaVantage] {function} 错误: {data}")
                return None
            return data
    except Exception as e:
        print(f"[AlphaVantage] {function} 请求失败: {e}")
        return None


async def fetch_news_sentiment(session: aiohttp.ClientSession, tickers: list[str]) -> list[dict]:
    """获取新闻情绪数据 — Alpha Vantage 的核心价值"""
    all_articles = []
    for ticker in tickers[:5]:  # 限制 5 个避免超出免费额度
        data = await _call_av(session, "NEWS_SENTIMENT", tickers=ticker, limit=10)
        if not data:
            continue
        for item in data.get("feed", []):
            all_articles.append({
                "source": "AlphaVantage",
                "source_topic": "news_sentiment",
                "url": item.get("url", ""),
                "title": item.get("title", ""),
                "summary": item.get("summary", "") or "",
                "published_at": item.get("time_published", ""),
                "category": "investing",
                "language": "en",
                "score": float(item.get("overall_sentiment_score", 0)) * 10,
                "author": item.get("source", ""),
                "_ticker_sentiment": item.get("ticker_sentiment", []),
                "_sentiment_label": item.get("overall_sentiment_label", ""),
            })
    return all_articles


async def fetch_market_quote(session: aiohttp.ClientSession, ticker: str) -> dict | None:
    """获取单只股票最新报价"""
    data = await _call_av(session, "GLOBAL_QUOTE", symbol=ticker)
    if not data or "Global Quote" not in data:
        return None
    q = data["Global Quote"]
    if not q or not q.get("05. price"):
        return None
    return {
        "ticker": ticker,
        "date": q.get("07. latest trading day", datetime.now().strftime("%Y-%m-%d")),
        "open": float(q.get("02. open", 0) or 0),
        "high": float(q.get("03. high", 0) or 0),
        "low": float(q.get("04. low", 0) or 0),
        "close": float(q.get("05. price", 0) or 0),
        "volume": int(q.get("06. volume", 0) or 0),
        "source": "AlphaVantage",
    }


async def fetch_crypto_quote(session: aiohttp.ClientSession, symbol: str) -> dict | None:
    """获取加密货币报价"""
    data = await _call_av(session, "CURRENCY_EXCHANGE_RATE", from_currency=symbol, to_currency="USD")
    if not data or "Realtime Currency Exchange Rate" not in data:
        return None
    r = data["Realtime Currency Exchange Rate"]
    return {
        "ticker": f"CRYPTO:{symbol}",
        "date": r.get("6. Last Refreshed", "")[:10],
        "close": float(r.get("5. Exchange Rate", 0) or 0),
        "source": "AlphaVantage",
    }


async def fetch_fx_rate(session: aiohttp.ClientSession) -> dict | None:
    """获取美元指数 DXY"""
    data = await _call_av(session, "CURRENCY_EXCHANGE_RATE", from_currency="USD", to_currency="EUR")
    if not data:
        return None
    return {"source": "AlphaVantage", "raw": data}


async def ingest_alphavantage() -> int:
    """Alpha Vantage 数据采集"""
    if not ALPHA_VANTAGE_KEY:
        print("[AlphaVantage] 跳过 (缺少 API Key)")
        return 0

    async with aiohttp.ClientSession() as session:
        # 1. 新闻情绪（最大价值）
        core_tickers = ["NVDA", "TSLA", "AAPL", "MSFT", "META"]
        articles = await fetch_news_sentiment(session, core_tickers)

        # 2. 核心股票报价
        quote_tickers = ["NVDA", "AMD", "TSLA", "AAPL", "MSFT", "QQQ", "SPY"]
        quote_tasks = [fetch_market_quote(session, t) for t in quote_tickers]
        quotes = await asyncio.gather(*quote_tasks, return_exceptions=True)

        # 3. 加密货币报价
        crypto_tasks = [fetch_crypto_quote(session, c) for c in ["BTC", "ETH", "SOL"]]
        crypto_quotes = await asyncio.gather(*crypto_tasks, return_exceptions=True)

    article_count = insert_articles_batch(articles)
    for q in quotes:
        if isinstance(q, dict) and q:
            insert_market_data(q)
    for cq in crypto_quotes:
        if isinstance(cq, dict) and cq:
            insert_market_data(cq)

    print(f"[AlphaVantage] 入库 {article_count} 条新闻情绪, {sum(1 for q in quotes if isinstance(q, dict) and q)} 条股票报价, {sum(1 for c in crypto_quotes if isinstance(c, dict) and c)} 条 crypto 报价")
    return article_count
