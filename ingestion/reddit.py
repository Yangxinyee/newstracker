"""
Reddit API 数据源
OAuth2 认证，覆盖五大领域 20+ 子版
"""

import asyncio
from datetime import datetime

import aiohttp

from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT
from database import insert_articles_batch

# 五大领域的 subreddit 映射
SUBREDDIT_CATEGORY_MAP = {
    # 互联网/科技
    "technology": "tech",
    "programming": "tech",
    "MachineLearning": "tech",
    "artificial": "tech",
    "singularity": "tech",
    "startups": "tech",
    # 加密货币
    "CryptoCurrency": "crypto",
    "Bitcoin": "crypto",
    "ethereum": "crypto",
    "defi": "crypto",
    "ethdev": "crypto",
    # 能源科技
    "energy": "energy",
    "solar": "energy",
    "electricvehicles": "energy",
    "teslamotors": "energy",
    "RenewableEnergy": "energy",
    "nuclear": "energy",
    "Futurology": "energy",
    # 半导体
    "hardware": "semiconductor",
    "Amd": "semiconductor",
    "intel": "semiconductor",
    "nvidia": "semiconductor",
    "chipdesign": "semiconductor",
    # 美股/投资
    "investing": "investing",
    "stocks": "investing",
    "StockMarket": "investing",
    "SecurityAnalysis": "investing",
    "Economics": "investing",
}

TARGET_SUBS = list(SUBREDDIT_CATEGORY_MAP.keys())


async def _get_token(session: aiohttp.ClientSession) -> str | None:
    """OAuth2 获取 Bearer Token"""
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        print("[Reddit] 未配置 CLIENT_ID/SECRET，跳过")
        return None

    auth = aiohttp.BasicAuth(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)
    headers = {"User-Agent": REDDIT_USER_AGENT}
    try:
        async with session.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=auth,
            data={"grant_type": "client_credentials"},
            headers=headers,
            timeout=15,
        ) as resp:
            data = await resp.json()
            return data.get("access_token")
    except Exception as e:
        print(f"[Reddit] 认证失败: {e}")
        return None


async def _fetch_subreddit(
    session: aiohttp.ClientSession,
    token: str,
    subreddit: str,
    listing: str = "hot",
    limit: int = 25,
) -> list[dict]:
    headers = {
        "Authorization": f"bearer {token}",
        "User-Agent": REDDIT_USER_AGENT,
    }
    url = f"https://oauth.reddit.com/r/{subreddit}/{listing}.json?limit={limit}"
    try:
        async with session.get(url, headers=headers, timeout=15) as resp:
            if resp.status != 200:
                return []
            data = await resp.json()
    except Exception:
        return []

    posts = []
    for child in data.get("data", {}).get("children", []):
        p = child["data"]
        # 跳过置顶帖
        if p.get("stickied"):
            continue
        posts.append({
            "source": "Reddit",
            "source_topic": subreddit,
            "url": p.get("url", f"https://reddit.com{p.get('permalink', '')}"),
            "title": p.get("title", ""),
            "summary": (p.get("selftext", "") or "")[:500],
            "published_at": datetime.fromtimestamp(p.get("created_utc", 0)).isoformat(),
            "category": SUBREDDIT_CATEGORY_MAP.get(subreddit, "tech"),
            "language": "en",
            "score": p.get("score", 0),
            "num_comments": p.get("num_comments", 0),
            "author": p.get("author", ""),
            "_upvote_ratio": p.get("upvote_ratio", 0),
            "_num_crossposts": p.get("num_crossposts", 0),
        })
    return posts


async def ingest_reddit(per_sub_limit: int = 20) -> int:
    """批量拉取所有目标 subreddit 的 hot 帖子"""
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        print("[Reddit] 跳过 (缺少 API 凭据)")
        return 0

    async with aiohttp.ClientSession() as session:
        token = await _get_token(session)
        if not token:
            return 0

        tasks = [
            _fetch_subreddit(session, token, sub, listing="hot", limit=per_sub_limit)
            for sub in TARGET_SUBS
        ]
        all_results = await asyncio.gather(*tasks, return_exceptions=True)

    all_articles = []
    for sub, result in zip(TARGET_SUBS, all_results):
        if isinstance(result, list):
            all_articles.extend(result)
        elif isinstance(result, Exception):
            print(f"[Reddit] r/{sub} 错误: {result}")

    # 按 score 降序
    all_articles.sort(key=lambda x: x.get("score", 0) or 0, reverse=True)

    count = insert_articles_batch(all_articles)
    print(f"[Reddit] 获取 {len(all_articles)} 帖，入库 {count} 帖")
    return count
