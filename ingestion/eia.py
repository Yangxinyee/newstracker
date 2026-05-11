"""
EIA (U.S. Energy Information Administration) Open Data API
免费额度: 无限 (需 API Key)
覆盖美国能源全系列数据
"""

import asyncio
from datetime import datetime

import aiohttp

from config import EIA_API_KEY
from database import insert_market_data

BASE_URL = "https://api.eia.gov/v2"


# 关键能源数据系列
ENERGY_SERIES = [
    # 石油
    {"route": "petroleum/pri/spt/data", "params": {"frequency": "daily",
             "data[0]": "value", "facets[product][]": "EPCBRENT", "sort[0][column]": "period", "sort[0][direction]": "desc", "length": 5}},
    {"route": "petroleum/pri/spt/data", "params": {"frequency": "daily",
             "data[0]": "value", "facets[product][]": "EPCWTI", "sort[0][column]": "period", "sort[0][direction]": "desc", "length": 5}},
    # 天然气
    {"route": "natural-gas/pri/sum/data", "params": {"frequency": "monthly",
             "data[0]": "value", "sort[0][column]": "period", "sort[0][direction]": "desc", "length": 3}},
]


async def _fetch_eia_series(session: aiohttp.ClientSession, config: dict, label: str) -> dict | None:
    url = f"{BASE_URL}/{config['route']}"
    params = config["params"].copy()
    params["api_key"] = EIA_API_KEY

    try:
        async with session.get(url, params=params, timeout=15) as resp:
            data = await resp.json()
    except Exception as e:
        print(f"[EIA] {label} 请求失败: {e}")
        return None

    rows = data.get("response", {}).get("data", [])
    if not rows:
        return None

    return {"label": label, "data": rows}


async def ingest_eia() -> int:
    """EIA 能源数据采集"""
    if not EIA_API_KEY:
        print("[EIA] 跳过 (缺少 API Key)")
        return 0

    labels = ["Brent Crude", "WTI Crude", "Natural Gas"]
    async with aiohttp.ClientSession() as session:
        tasks = [_fetch_eia_series(session, config, label) for config, label in zip(ENERGY_SERIES, labels)]
        all_results = await asyncio.gather(*tasks, return_exceptions=True)

    count = 0
    for result in all_results:
        if not isinstance(result, dict) or not result:
            continue
        for row in result["data"][:3]:
            period = row.get("period", "")[:10]
            value = row.get("value")
            if period and value is not None:
                insert_market_data({
                    "ticker": f"ENERGY:{result['label']}",
                    "date": period,
                    "close": float(value),
                    "source": "EIA",
                })
                count += 1

    print(f"[EIA] 入库 {count} 条能源数据")
    return count
