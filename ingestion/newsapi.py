"""
NewsAPI.org 数据源
免费额度: 100 req/天
"""

import asyncio

import aiohttp

from config import NEWSAPI_KEY
from database import insert_articles_batch

BASE_URL = "https://newsapi.org/v2"

# 五大领域搜索配置
DOMAIN_CONFIGS = [
    # 互联网/科技
    {"domain": "tech", "type": "top-headlines", "category": "technology", "label": "Tech Headlines"},
    {"domain": "tech", "type": "everything",
     "q": "(AI OR \"artificial intelligence\" OR LLM OR \"large language model\") AND (launch OR breakthrough OR release)",
     "sortBy": "publishedAt", "label": "AI Breakthroughs"},
    # 加密货币
    {"domain": "crypto", "type": "everything",
     "q": "(Bitcoin OR Ethereum OR crypto OR blockchain OR DeFi) AND (regulation OR ETF OR hack OR upgrade)",
     "sortBy": "publishedAt", "label": "Crypto Major Events"},
    # 能源科技
    {"domain": "energy", "type": "everything",
     "q": "(\"solar power\" OR \"wind energy\" OR \"nuclear fusion\" OR \"battery storage\" OR \"green hydrogen\") AND (breakthrough OR record OR innovation)",
     "sortBy": "publishedAt", "label": "Clean Energy Tech"},
    {"domain": "energy", "type": "everything",
     "q": "(\"electric vehicle\" OR \"EV battery\" OR \"solid state battery\") AND (launch OR production OR factory)",
     "sortBy": "publishedAt", "label": "EV & Battery"},
    # 半导体
    {"domain": "semiconductor", "type": "everything",
     "q": "(semiconductor OR chip OR foundry OR fab) AND (TSMC OR Intel OR Samsung OR NVIDIA OR AMD OR ASML)",
     "sortBy": "publishedAt", "label": "Chip Industry"},
    {"domain": "semiconductor", "type": "everything",
     "q": "\"chip manufacturing\" OR \"advanced packaging\" OR \"lithography\" OR \"3nm\" OR \"2nm\" OR \"EUV\"",
     "sortBy": "publishedAt", "label": "Chip Manufacturing"},
    # 美股/投资
    {"domain": "investing", "type": "top-headlines", "category": "business", "label": "Business Headlines"},
    {"domain": "investing", "type": "everything",
     "q": "(\"earnings report\" OR \"beat estimates\" OR \"missed estimates\" OR \"guidance\") AND (stock OR shares)",
     "sortBy": "publishedAt", "label": "Earnings Reports"},
    {"domain": "investing", "type": "everything",
     "q": "(\"Fed\" OR \"Federal Reserve\" OR \"interest rate\" OR \"inflation\" OR \"CPI\") AND (decision OR outlook OR forecast)",
     "sortBy": "publishedAt", "label": "Macro & Fed"},
]


async def _fetch_domain(session: aiohttp.ClientSession, config: dict) -> list[dict]:
    params = {
        "apiKey": NEWSAPI_KEY,
        "pageSize": 30,
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

    headers = {"Accept-Encoding": "gzip, deflate"}
    try:
        async with session.get(url, params=params, timeout=15, headers=headers) as resp:
            data = await resp.json()
    except Exception as e:
        print(f"[NewsAPI] {config['label']} 请求失败: {e}")
        return []

    if data.get("status") != "ok":
        print(f"[NewsAPI] {config['label']} API 错误: {data.get('message', '')}")
        return []

    articles = []
    for a in data.get("articles", []):
        title = a.get("title", "")
        if not title or title == "[Removed]":
            continue
        articles.append({
            "source": "NewsAPI",
            "source_topic": config["label"],
            "url": a.get("url", ""),
            "title": title,
            "summary": a.get("description", "") or "",
            "content_preview": a.get("content", "") or "",
            "published_at": a.get("publishedAt", ""),
            "category": config["domain"],
            "language": "en",
            "author": a.get("author", ""),
            "_source_name": a.get("source", {}).get("name", ""),
        })
    return articles


def _dedup_by_title(articles: list[dict]) -> list[dict]:
    seen = set()
    unique = []
    for a in articles:
        key = a["title"][:100].lower().strip()
        if key and key not in seen:
            seen.add(key)
            unique.append(a)
    return unique


async def ingest_newsapi() -> int:
    """NewsAPI 全量采集"""
    if not NEWSAPI_KEY:
        print("[NewsAPI] 跳过 (缺少 API Key)")
        return 0

    async with aiohttp.ClientSession() as session:
        tasks = [_fetch_domain(session, config) for config in DOMAIN_CONFIGS]
        all_results = await asyncio.gather(*tasks, return_exceptions=True)

    all_articles = []
    for result in all_results:
        if isinstance(result, list):
            all_articles.extend(result)

    all_articles = _dedup_by_title(all_articles)
    count = insert_articles_batch(all_articles)
    print(f"[NewsAPI] 获取 {len(all_articles)} 篇，入库 {count} 篇 (使用了 {len(DOMAIN_CONFIGS)} 次请求)")
    return count
