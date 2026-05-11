"""
实体识别模块 (NER)
轻量实现: 基于关键词词典 + 规则，提取公司名、股票代码、人物、技术关键词
"""

import re

# 核心公司名 → Ticker 映射
COMPANY_TICKER_MAP = {
    # 半导体
    "nvidia": ("NVDA", "semiconductor"),
    "amd": ("AMD", "semiconductor"),
    "intel": ("INTC", "semiconductor"),
    "tsmc": ("TSM", "semiconductor"),
    "asml": ("ASML", "semiconductor"),
    "broadcom": ("AVGO", "semiconductor"),
    "qualcomm": ("QCOM", "semiconductor"),
    "micron": ("MU", "semiconductor"),
    "applied materials": ("AMAT", "semiconductor"),
    "lam research": ("LRCX", "semiconductor"),
    "kla": ("KLAC", "semiconductor"),
    "arm holdings": ("ARM", "semiconductor"),
    "synopsys": ("SNPS", "semiconductor"),
    "cadence": ("CDNS", "semiconductor"),
    "samsung": ("SSNLF", "semiconductor"),
    "sk hynix": ("HXSCL", "semiconductor"),
    "analog devices": ("ADI", "semiconductor"),
    "texas instruments": ("TXN", "semiconductor"),
    "marvell": ("MRVL", "semiconductor"),
    "globalfoundries": ("GFS", "semiconductor"),
    "onn": ("ON", "semiconductor"),
    # 科技
    "apple": ("AAPL", "tech"),
    "microsoft": ("MSFT", "tech"),
    "alphabet": ("GOOGL", "tech"),
    "google": ("GOOGL", "tech"),
    "meta": ("META", "tech"),
    "amazon": ("AMZN", "tech"),
    "tesla": ("TSLA", "energy"),
    "salesforce": ("CRM", "tech"),
    "adobe": ("ADBE", "tech"),
    "oracle": ("ORCL", "tech"),
    "palantir": ("PLTR", "tech"),
    "snowflake": ("SNOW", "tech"),
    "cloudflare": ("NET", "tech"),
    "crowdstrike": ("CRWD", "tech"),
    "uber": ("UBER", "tech"),
    "airbnb": ("ABNB", "tech"),
    "netflix": ("NFLX", "tech"),
    "openai": (None, "tech"),
    "anthropic": (None, "tech"),
    "deepseek": (None, "tech"),
    # 能源
    "rivian": ("RIVN", "energy"),
    "lucid": ("LCID", "energy"),
    "enphase": ("ENPH", "energy"),
    "first solar": ("FSLR", "energy"),
    "nextera energy": ("NEE", "energy"),
    "constellation energy": ("CEG", "energy"),
    "vistra": ("VST", "energy"),
    "ge vernova": ("GEV", "energy"),
    "solar edge": ("SEDG", "energy"),
    "plug power": ("PLUG", "energy"),
    "bloom energy": ("BE", "energy"),
    # 加密
    "coinbase": ("COIN", "crypto"),
    "marathon digital": ("MARA", "crypto"),
    "riot platforms": ("RIOT", "crypto"),
    "microstrategy": ("MSTR", "crypto"),
    # 金融
    "jpmorgan": ("JPM", "investing"),
    "goldman sachs": ("GS", "investing"),
    "blackrock": ("BLK", "investing"),
    "morgan stanley": ("MS", "investing"),
}

# 技术关键词 (用于趋势识别)
TECH_KEYWORDS = {
    "ai_coverage": [
        "artificial intelligence", "machine learning", "deep learning",
        "large language model", "llm", "gpt", "transformer",
        "neural network", "reinforcement learning", "computer vision",
        "natural language processing", "nlp", "generative ai",
        "agent", "autonomous agent", "rag", "fine-tuning",
    ],
    "semiconductor_coverage": [
        "3nm", "2nm", "1.4nm", "angstrom", "euv", "high-na",
        "chiplet", "advanced packaging", "hbm", "hbm3", "hbm4",
        "gpu", "tpu", "npu", "ai accelerator", "inference chip",
        "wafer", "fab", "foundry", "backside power", "gate-all-around",
    ],
    "energy_coverage": [
        "solid state battery", "lithium", "lfp", "sodium ion",
        "perovskite", "tandem solar", "green hydrogen", "electrolyzer",
        "nuclear fusion", "smr", "small modular reactor", "carbon capture",
        "long duration storage", "virtual power plant", "v2g",
    ],
    "crypto_coverage": [
        "defi", "layer 2", "rollup", "zero knowledge", "zk proof",
        "restaking", "avs", "eigenlayer", "celestia",
        "bitcoin etf", "ethereum etf", "rwa", "tokenization",
        "stablecoin", "cbdc", "solana", "sui", "aptos",
    ],
    "investing_coverage": [
        "ipo", "direct listing", "spac", "merger", "acquisition",
        "buyback", "dividend", "stock split", "guidance",
        "earnings surprise", "beat", "miss", "revenue growth",
        "margin expansion", "layoff", "restructuring",
    ],
}


def extract_entities(text: str) -> list[dict]:
    """从文本中提取实体"""
    if not text:
        return []

    text_lower = text.lower()
    entities = []

    # 1. 公司名匹配
    for company_name, (ticker, sector) in COMPANY_TICKER_MAP.items():
        if company_name in text_lower:
            entities.append({
                "entity_name": company_name.title() if len(company_name) > 3 else company_name.upper(),
                "entity_type": "COMPANY",
                "ticker": ticker,
                "sector": sector,
                "relevance_score": 1.0,
            })

    # 2. 技术关键词匹配
    for tech_group, keywords in TECH_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                entities.append({
                    "entity_name": kw,
                    "entity_type": "TECHNOLOGY",
                    "ticker": None,
                    "sector": tech_group,
                    "relevance_score": 0.7,
                })

    # 3. Ticker 显式提及 (如 $NVDA)
    ticker_pattern = r'\$([A-Z]{1,5})\b'
    for match in re.finditer(ticker_pattern, text):
        ticker = match.group(1)
        # 找到对应的公司名
        company_name = None
        sector = None
        for cn, (t, s) in COMPANY_TICKER_MAP.items():
            if t == ticker:
                company_name = cn.title()
                sector = s
                break
        entities.append({
            "entity_name": ticker,
            "entity_type": "TICKER",
            "ticker": ticker,
            "sector": sector,
            "relevance_score": 0.9,
        })

    # 去重
    seen = set()
    unique_entities = []
    for e in entities:
        key = (e["entity_name"], e["entity_type"], e.get("ticker"))
        if key not in seen:
            seen.add(key)
            unique_entities.append(e)

    return unique_entities


def analyze_articles_entities(articles: list[dict]) -> dict:
    """
    分析一批文章的实体分布
    返回: 最常提及的公司、技术趋势
    """
    ticker_count: dict[str, int] = {}
    tech_count: dict[str, int] = {}

    for article in articles:
        title = article.get("title", "")
        summary = article.get("summary", "")
        combined = f"{title} {summary}"[:2000]

        entities = extract_entities(combined)
        for entity in entities:
            if entity["entity_type"] in ("COMPANY", "TICKER") and entity.get("ticker"):
                tk = entity["ticker"]
                ticker_count[tk] = ticker_count.get(tk, 0) + 1
            if entity["entity_type"] == "TECHNOLOGY":
                tech_count[entity["entity_name"]] = tech_count.get(entity["entity_name"], 0) + 1

    return {
        "top_tickers": sorted(ticker_count.items(), key=lambda x: x[1], reverse=True)[:20],
        "top_tech_keywords": sorted(tech_count.items(), key=lambda x: x[1], reverse=True)[:20],
    }
