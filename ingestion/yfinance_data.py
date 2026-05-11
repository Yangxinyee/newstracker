"""
Yahoo Finance 数据源 (通过 yfinance 库)
免费无限量
"""

import asyncio
from datetime import datetime, timedelta

from database import insert_market_data, insert_articles_batch

# 核心追踪股票列表 (五大领域)
WATCHED_TICKERS = {
    # 半导体
    "NVDA": "semiconductor", "AMD": "semiconductor", "INTC": "semiconductor",
    "TSM": "semiconductor", "ASML": "semiconductor", "AVGO": "semiconductor",
    "QCOM": "semiconductor", "MU": "semiconductor", "AMAT": "semiconductor",
    "LRCX": "semiconductor", "KLAC": "semiconductor", "ARM": "semiconductor",
    # 科技
    "AAPL": "tech", "MSFT": "tech", "GOOGL": "tech", "META": "tech",
    "AMZN": "tech", "CRM": "tech", "ADBE": "tech", "ORCL": "tech",
    "PLTR": "tech", "SNOW": "tech", "NET": "tech", "CRWD": "tech",
    # 能源/EV
    "TSLA": "energy", "RIVN": "energy", "LCID": "energy",
    "ENPH": "energy", "FSLR": "energy", "NEE": "energy",
    "CEG": "energy", "VST": "energy",
    # 加密货币相关
    "COIN": "crypto", "MARA": "crypto", "RIOT": "crypto", "MSTR": "crypto",
    # 金融/投资
    "JPM": "investing", "GS": "investing", "BLK": "investing",
    "SPY": "investing", "QQQ": "investing", "IWM": "investing",
}


async def _fetch_one_ticker(ticker: str, category: str) -> list[dict]:
    """使用 yfinance 获取单只股票数据（在线程池中运行，因为 yfinance 是同步的）"""
    import yfinance as yf
    loop = asyncio.get_event_loop()

    def _get():
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d")
            if hist.empty:
                return []
        except Exception:
            return []

        results = []
        for idx, row in hist.iterrows():
            date_str = idx.strftime("%Y-%m-%d") if hasattr(idx, 'strftime') else str(idx)[:10]
            results.append({
                "ticker": ticker,
                "date": date_str,
                "open": float(row.get("Open", 0)) if row.get("Open") else None,
                "high": float(row.get("High", 0)) if row.get("High") else None,
                "low": float(row.get("Low", 0)) if row.get("Low") else None,
                "close": float(row.get("Close", 0)) if row.get("Close") else None,
                "volume": int(row.get("Volume", 0)) if row.get("Volume") else None,
                "source": "YahooFinance",
                "_category": category,
            })
        return results

    return await loop.run_in_executor(None, _get)


async def _fetch_news_for_ticker(ticker: str, category: str) -> list[dict]:
    """获取股票相关的新闻（yfinance 内置）"""
    import yfinance as yf
    loop = asyncio.get_event_loop()

    def _get():
        try:
            stock = yf.Ticker(ticker)
            news = stock.news
            if not news:
                return []
        except Exception:
            return []

        articles = []
        for n in news[:10]:
            content = n.get("content", {})
            articles.append({
                "source": "YahooFinance",
                "source_topic": ticker,
                "url": content.get("canonicalUrl", {}).get("url", n.get("link", "")),
                "title": content.get("title", n.get("title", "")),
                "summary": content.get("summary", "") or "",
                "published_at": content.get("pubDate", datetime.now().isoformat()),
                "category": category,
                "language": "en",
                "_ticker": ticker,
                "_provider": content.get("provider", {}).get("displayName", ""),
            })
        return articles

    return await loop.run_in_executor(None, _get)


async def ingest_yfinance(tickers: list[str] | None = None) -> int:
    """采集股票数据和新闻"""
    if tickers is None:
        tickers = list(WATCHED_TICKERS.keys())

    # 拉取行情数据
    price_tasks = [_fetch_one_ticker(t, WATCHED_TICKERS.get(t, "investing")) for t in tickers]
    price_results = await asyncio.gather(*price_tasks, return_exceptions=True)

    # 拉取新闻（只拉前 20 只核心股票的新闻）
    core_tickers = list(WATCHED_TICKERS.keys())[:20]
    news_tasks = [_fetch_news_for_ticker(t, WATCHED_TICKERS.get(t, "investing")) for t in core_tickers]
    news_results = await asyncio.gather(*news_tasks, return_exceptions=True)

    # 入库行情
    price_count = 0
    for result in price_results:
        if isinstance(result, list):
            for item in result:
                insert_market_data(item)
                price_count += 1

    # 入库新闻
    all_news = []
    for result in news_results:
        if isinstance(result, list):
            all_news.extend(result)
    news_count = insert_articles_batch(all_news)

    print(f"[YahooFinance] 入库 {price_count} 条行情, {news_count} 条新闻")
    return news_count
