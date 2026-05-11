"""
FRED (Federal Reserve Economic Data) API 数据源
免费额度: 无限 (需 API Key)
提供美国宏观经济全系列数据
"""

import asyncio
from datetime import datetime

import aiohttp

from config import FRED_API_KEY
from database import insert_market_data

BASE_URL = "https://api.stlouisfed.org/fred"


# 关键经济指标
KEY_SERIES = {
    "GDP": "国内生产总值 (季度)",
    "CPIAUCSL": "消费者价格指数 CPI",
    "UNRATE": "失业率",
    "FEDFUNDS": "联邦基金利率",
    "T10Y2Y": "10年-2年国债利差 (收益率曲线)",
    "T10YIE": "10年期通胀预期",
    "DGS10": "10年期国债收益率",
    "DGS2": "2年期国债收益率",
    "M2SL": "M2 货币供应量",
    "INDPRO": "工业生产指数",
    "RETAILSMNSA": "零售额 (未经季节调整)",
    "HOUST": "新屋开工",
    "TOTALSA": "汽车销量",
    "WTI": "WTI 原油价格",
    "NATURALGAS": "天然气价格",
}


async def _fetch_series(session: aiohttp.ClientSession, series_id: str) -> dict | None:
    """获取单个经济指标最新值"""
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 5,
    }
    url = f"{BASE_URL}/series/observations"
    try:
        async with session.get(url, params=params, timeout=15) as resp:
            data = await resp.json()
    except Exception as e:
        print(f"[FRED] {series_id} 请求失败: {e}")
        return None

    observations = data.get("observations", [])
    if not observations:
        return None

    values = []
    for obs in observations:
        if obs.get("value") and obs["value"] != ".":
            values.append({
                "date": obs["date"],
                "value": float(obs["value"]),
            })

    return {
        "series_id": series_id,
        "name": KEY_SERIES.get(series_id, series_id),
        "latest": values[0] if values else None,
        "history": values,
    }


async def ingest_fred() -> int:
    """FRED 经济数据采集"""
    if not FRED_API_KEY:
        print("[FRED] 跳过 (缺少 API Key)")
        return 0

    async with aiohttp.ClientSession() as session:
        tasks = [_fetch_series(session, sid) for sid in KEY_SERIES]
        all_results = await asyncio.gather(*tasks, return_exceptions=True)

    count = 0
    for result in all_results:
        if not isinstance(result, dict) or not result:
            continue
        latest = result.get("latest")
        if latest:
            insert_market_data({
                "ticker": f"ECON:{result['series_id']}",
                "date": latest["date"],
                "close": latest["value"],
                "source": "FRED",
                "_name": result.get("name", ""),
            })
            count += 1

    print(f"[FRED] 入库 {count} 条经济指标")
    return count
