"""
TLDR Newsletter 数据源
- RSS (主刊): https://tldr.tech/rss
- 非官方 API: https://tldr.tech/api/latest/{topic}
"""

import asyncio
from datetime import datetime

import aiohttp
import feedparser
from bs4 import BeautifulSoup

from config import BASE_DIR
from database import insert_articles_batch

TLDR_TOPICS = {
    "tech": "TLDR",
    "ai": "TLDR AI",
    "crypto": "TLDR Crypto",
    "fintech": "TLDR Fintech",
}


async def fetch_tldr_rss(session: aiohttp.ClientSession) -> list[dict]:
    """通过 RSS 获取主刊"""
    url = "https://tldr.tech/rss"
    headers = {"Accept-Encoding": "gzip, deflate"}
    try:
        async with session.get(url, timeout=30, headers=headers) as resp:
            rss_content = await resp.text()
    except Exception as e:
        print(f"[TLDR RSS] 请求失败: {e}")
        return []

    loop = asyncio.get_event_loop()
    feed = await loop.run_in_executor(None, feedparser.parse, rss_content)

    articles = []
    for entry in feed.entries:
        published = entry.get("published", "")
        articles.append({
            "source": "TLDR",
            "source_topic": "tech",
            "url": entry.get("link", ""),
            "title": entry.get("title", ""),
            "summary": entry.get("summary", ""),
            "published_at": published,
            "category": _classify_topic("tech"),
            "language": "en",
            "score": 9.0,  # 编辑精选 = 高价值
        })
    print(f"[TLDR RSS] 获取 {len(articles)} 篇文章")
    return articles


async def fetch_tldr_topic(session: aiohttp.ClientSession, topic: str) -> list[dict]:
    """通过 /api/latest/{topic} 获取指定主题"""
    url = f"https://tldr.tech/api/latest/{topic}"
    headers = {"Accept-Encoding": "gzip, deflate"}
    try:
        async with session.get(url, timeout=30, headers=headers) as resp:
            if resp.status != 200:
                print(f"[TLDR {topic}] HTTP {resp.status}")
                return []
            html = await resp.text()
    except Exception as e:
        print(f"[TLDR {topic}] 请求失败: {e}")
        return []

    soup = BeautifulSoup(html, "html.parser")
    articles = []
    source_name = TLDR_TOPICS.get(topic, f"TLDR {topic}")

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        text = a_tag.get_text(strip=True)
        # 过滤无关链接
        if not text or len(text) < 15:
            continue
        if any(skip in href for skip in ["tldr.tech", "mailto:", "javascript:", "#"]):
            continue
        if any(skip in text.lower() for skip in ["subscribe", "sponsor", "advertise", "join", "readers"]):
            continue

        articles.append({
            "source": source_name,
            "source_topic": topic,
            "url": href,
            "title": text,
            "summary": "",
            "published_at": datetime.now().strftime("%Y-%m-%d"),
            "category": _classify_topic(topic),
            "language": "en",
            "score": 8.5,
        })

    print(f"[TLDR {topic}] 获取 {len(articles)} 篇文章")
    return articles


def _classify_topic(topic: str) -> str:
    """TLDR topic 映射到系统五大领域"""
    mapping = {
        "tech": "tech",
        "ai": "tech",
        "crypto": "crypto",
        "fintech": "investing",
    }
    return mapping.get(topic, "tech")


async def ingest_tldr() -> int:
    """采集全部 TLDR 主题并存入数据库"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_tldr_rss(session)]
        tasks += [fetch_tldr_topic(session, t) for t in TLDR_TOPICS if t != "tech"]

        all_results = await asyncio.gather(*tasks, return_exceptions=True)

    all_articles = []
    for result in all_results:
        if isinstance(result, list):
            all_articles.extend(result)

    count = insert_articles_batch(all_articles)
    print(f"[TLDR] 总计入库 {count} 篇 (去重后)")
    return count
