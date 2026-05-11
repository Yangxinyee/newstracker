"""
Hacker News API 数据源
官方 API (Firebase): https://github.com/HackerNews/API
Base URL: https://hacker-news.firebaseio.com/v0/
"""

import asyncio
from datetime import datetime

import aiohttp

from database import insert_articles_batch

BASE_URL = "https://hacker-news.firebaseio.com/v0"

# 领域关键词映射 (小写匹配)
DOMAIN_KEYWORDS = {
    "crypto": ["bitcoin", "ethereum", "crypto", "blockchain", "defi", "web3", "nft", "stablecoin", "solana"],
    "energy": ["solar", "nuclear", "fusion", "battery", "ev ", "electric vehicle", "renewable", "energy", "tesla",
               "grid", "wind", "hydrogen", "geothermal"],
    "semiconductor": ["chip", "semiconductor", "tsmc", "intel", "amd", "nvidia", "gpu", "cpu", "foundry", "n3",
                      "n2", "3nm", "2nm", "lithography", "euv", "hbm", "arm ", "risc-v", "fpga", "asic",
                      "broadcom", "qualcomm", "micron", "samsung foundry", "asml"],
    "investing": ["ipo", "acquisition", "acquired", "funding", "series a", "series b", "stock", "market cap",
                  "valuation", "revenue", "earnings", "merger", "spac", "went public", "raised $"],
}


async def fetch_item(session: aiohttp.ClientSession, item_id: int) -> dict | None:
    url = f"{BASE_URL}/item/{item_id}.json"
    try:
        async with session.get(url, timeout=10) as resp:
            if resp.status == 200:
                return await resp.json()
    except Exception:
        pass
    return None


async def fetch_stories(session: aiohttp.ClientSession, story_type: str, limit: int = 50) -> list[dict]:
    """通用故事拉取: topstories, newstories, beststories, showstories, askstories"""
    url = f"{BASE_URL}/{story_type}.json"
    try:
        async with session.get(url, timeout=15) as resp:
            ids = await resp.json()
    except Exception:
        return []

    tasks = [fetch_item(session, sid) for sid in ids[:limit]]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    stories = []
    for r in results:
        if isinstance(r, dict) and r is not None and r.get("type") == "story":
            stories.append(r)
    return stories


def _classify_hackernews(title: str) -> str:
    """根据标题分类到五大领域"""
    title_lower = title.lower()
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in title_lower:
                return domain
    return "tech"


async def ingest_hackernews(limit: int = 100) -> int:
    """采集 HN 多类故事并存入数据库"""
    async with aiohttp.ClientSession() as session:
        story_types = ["topstories", "newstories", "beststories", "showstories"]
        all_tasks = [fetch_stories(session, st, limit) for st in story_types]
        all_results = await asyncio.gather(*all_tasks, return_exceptions=True)

    seen_ids = set()
    articles = []

    for story_type, stories in zip(story_types, all_results):
        if not isinstance(stories, list):
            continue
        for s in stories:
            sid = s.get("id")
            if sid in seen_ids:
                continue
            seen_ids.add(sid)

            title = s.get("title", "")
            if not title:
                continue

            # Show HN / Ask HN 没有外部链接时用 HN 讨论页
            url = s.get("url") or f"https://news.ycombinator.com/item?id={sid}"

            articles.append({
                "source": "HackerNews",
                "source_topic": story_type.replace("stories", ""),
                "url": url,
                "title": title,
                "summary": s.get("text", "")[:500] if s.get("text") else "",
                "published_at": datetime.fromtimestamp(s.get("time", 0)).isoformat() if s.get("time") else None,
                "category": _classify_hackernews(title),
                "language": "en",
                "score": s.get("score", 0),
                "num_comments": s.get("descendants", 0),
                "author": s.get("by", ""),
            })

    # 按 score 降序排序
    articles.sort(key=lambda x: x.get("score", 0) or 0, reverse=True)

    count = insert_articles_batch(articles)
    print(f"[HackerNews] 获取 {len(articles)} 篇，入库 {count} 篇")
    return count
