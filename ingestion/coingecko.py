"""
CoinGecko API 数据源
免费额度: 30 req/分钟, 10,000/月
"""

import asyncio
from datetime import datetime

import aiohttp

from database import insert_articles_batch, insert_market_data

BASE_URL = "https://api.coingecko.com/api/v3"


async def fetch_trending(session: aiohttp.ClientSession) -> list[dict]:
    """获取 CoinGecko Trending 币种"""
    url = f"{BASE_URL}/search/trending"
    try:
        async with session.get(url, timeout=15) as resp:
            data = await resp.json()
    except Exception as e:
        print(f"[CoinGecko] Trending 请求失败: {e}")
        return []

    articles = []
    for coin in data.get("coins", [])[:15]:
        item = coin.get("item", {})
        name = item.get("name", "")
        symbol = item.get("symbol", "")

        articles.append({
            "source": "CoinGecko",
            "source_topic": "trending",
            "url": f"https://www.coingecko.com/en/coins/{item.get('id', '')}",
            "title": f"Trending: {name} ({symbol.upper()}) — Rank #{item.get('market_cap_rank', 'N/A')}",
            "summary": f"{name} ({symbol.upper()}) is trending on CoinGecko. Market cap rank: {item.get('market_cap_rank', 'N/A')}",
            "published_at": datetime.now().strftime("%Y-%m-%d"),
            "category": "crypto",
            "language": "en",
            "score": item.get("market_cap_rank", 0) * -1 + 1000,  # 排名越高分越高
            "_coin_id": item.get("id"),
            "_symbol": symbol,
        })
    return articles


async def fetch_global_data(session: aiohttp.ClientSession) -> dict | None:
    """获取全球 crypto 市场数据"""
    url = f"{BASE_URL}/global"
    try:
        async with session.get(url, timeout=10) as resp:
            return await resp.json()
    except Exception:
        return None


async def fetch_top_coins(session: aiohttp.ClientSession, limit: int = 20) -> list[dict]:
    """获取市值 Top 币种数据"""
    url = f"{BASE_URL}/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": "false",
    }
    try:
        async with session.get(url, params=params, timeout=15) as resp:
            data = await resp.json()
    except Exception as e:
        print(f"[CoinGecko] coins/markets 请求失败: {e}")
        return []

    results = []
    for coin in data:
        results.append({
            "ticker": f"CRYPTO:{coin.get('symbol', '').upper()}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "close": coin.get("current_price"),
            "source": "CoinGecko",
            "_coin_name": coin.get("name", ""),
            "_market_cap": coin.get("market_cap", 0),
            "_price_change_24h_pct": coin.get("price_change_percentage_24h", 0),
        })
    return results


async def ingest_coingecko() -> int:
    """CoinGecko 数据采集"""
    async with aiohttp.ClientSession() as session:
        trending_articles = await fetch_trending(session)
        top_coins = await fetch_top_coins(session, limit=20)

    count = insert_articles_batch(trending_articles)
    for coin_data in top_coins:
        insert_market_data(coin_data)

    print(f"[CoinGecko] 入库 {count} 条 trend，{len(top_coins)} 条行情")
    return count
