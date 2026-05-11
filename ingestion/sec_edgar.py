"""
SEC EDGAR API 数据源
免费、无需 API Key，直接从 SEC 获取上市公司文件
获取最近的 8-K (重大事件), 10-K (年报), 10-Q (季报) 等
"""

import asyncio
from datetime import datetime, timedelta

import aiohttp

from database import insert_articles_batch

BASE_URL = "https://www.sec.gov"
SUBMISSIONS_URL = "https://data.sec.gov/submissions"

# SEC 要求 User-Agent 包含组织名称
HEADERS = {
    "User-Agent": "NewsTracker/1.0 (contact@example.com)",
    "Accept-Encoding": "gzip, deflate",
}


async def _fetch_cik(session: aiohttp.ClientSession, ticker: str) -> str | None:
    """将 ticker 转换为 CIK"""
    url = "https://www.sec.gov/files/company_tickers.json"
    try:
        async with session.get(url, headers=HEADERS, timeout=15) as resp:
            data = await resp.json()
            for cik_str, info in data.items():
                if info.get("ticker", "").upper() == ticker.upper():
                    return str(info["cik_str"]).zfill(10)
    except Exception:
        pass
    return None


async def _fetch_recent_filings(session: aiohttp.ClientSession, cik: str, ticker: str, category: str) -> list[dict]:
    """获取公司最近的文件"""
    url = f"{SUBMISSIONS_URL}/CIK{cik}.json"
    try:
        async with session.get(url, headers=HEADERS, timeout=15) as resp:
            data = await resp.json()
    except Exception:
        return []

    articles = []
    recent = data.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    descriptions = recent.get("primaryDocument", [])
    accession_numbers = recent.get("accessionNumber", [])

    important_forms = {"8-K", "10-K", "10-Q", "S-1", "S-3", "13F", "SC 13G", "SC 13D", "DEF 14A"}

    for i, form in enumerate(forms[:100]):
        if form in important_forms:
            acc_num = accession_numbers[i].replace("-", "")
            doc_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_num}/{descriptions[i]}"
            filing_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type={form}"

            articles.append({
                "source": "SEC EDGAR",
                "source_topic": form,
                "url": filing_url,
                "title": f"{ticker} filed {form} — {descriptions[i]}",
                "summary": f"{ticker} filed {form} on {dates[i]}. Document: {descriptions[i]}",
                "published_at": dates[i] if dates[i] else datetime.now().strftime("%Y-%m-%d"),
                "category": category,
                "language": "en",
                "_form_type": form,
                "_ticker": ticker,
                "_doc_url": doc_url,
            })
    return articles


# 核心追踪公司 (ticker → 领域)
TRACKED_COMPANIES = {
    # 半导体
    "NVDA": "semiconductor", "AMD": "semiconductor", "INTC": "semiconductor",
    "TSM": "semiconductor", "ASML": "semiconductor", "AVGO": "semiconductor",
    "QCOM": "semiconductor", "MU": "semiconductor", "AMAT": "semiconductor",
    # 科技
    "AAPL": "tech", "MSFT": "tech", "GOOGL": "tech", "META": "tech",
    "AMZN": "tech", "CRM": "tech", "ADBE": "tech",
    # 能源
    "TSLA": "energy", "ENPH": "energy", "FSLR": "energy", "NEE": "energy",
    # 加密货币相关
    "COIN": "crypto", "MSTR": "crypto",
}


async def ingest_sec_edgar() -> int:
    """SEC EDGAR 数据采集"""
    async with aiohttp.ClientSession() as session:
        # 获取 CIK 列表
        cik_map = {}
        for ticker in list(TRACKED_COMPANIES.keys())[:15]:  # 限制 15 只
            cik = await _fetch_cik(session, ticker)
            if cik:
                cik_map[ticker] = cik
            await asyncio.sleep(0.1)  # SEC rate limiting

        # 拉取每家公司最近的文件
        tasks = [
            _fetch_recent_filings(session, cik, ticker, TRACKED_COMPANIES.get(ticker, "investing"))
            for ticker, cik in cik_map.items()
        ]
        all_results = await asyncio.gather(*tasks, return_exceptions=True)

    all_articles = []
    for result in all_results:
        if isinstance(result, list):
            all_articles.extend(result)

    count = insert_articles_batch(all_articles)
    print(f"[SEC EDGAR] 获取 {len(all_articles)} 份文件，入库 {count} 份")
    return count
