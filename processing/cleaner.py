"""
数据清洗模块
- HTML 标签清理
- 空白字符标准化
- 无意义内容过滤
- URL 标准化
"""

import re
from html import unescape


def clean_html(text: str) -> str:
    """移除 HTML 标签"""
    if not text:
        return ""
    clean = re.sub(r"<[^>]+>", "", text)
    clean = unescape(clean)
    return clean


def normalize_whitespace(text: str) -> str:
    """标准化空白字符"""
    if not text:
        return ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r" +", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_title(title: str) -> str:
    """清理标题"""
    if not title:
        return ""
    title = clean_html(title)
    title = normalize_whitespace(title)
    title = title.strip()
    return title


def clean_summary(summary: str, max_length: int = 1000) -> str:
    """清理摘要"""
    if not summary:
        return ""
    summary = clean_html(summary)
    summary = normalize_whitespace(summary)
    if len(summary) > max_length:
        summary = summary[:max_length].rsplit(" ", 1)[0] + "..."
    return summary


def is_junk_article(title: str, summary: str = "") -> bool:
    """过滤无意义的内容"""
    title_lower = title.lower()
    junk_keywords = [
        "advertisement", "sponsored", "subscribe now", "click here",
        "sign up", "privacy policy", "terms of service",
        "[removed]", "[deleted]", "404", "page not found",
    ]
    for kw in junk_keywords:
        if kw in title_lower:
            return True

    # 标题太短
    if len(title.strip()) < 10:
        return True

    return False


def extract_ticker_symbols(text: str) -> list[str]:
    """从文本中提取可能的股票代码（大写 1-5 字母）"""
    if not text:
        return []
    # 查找 $TICKER 或单独的大写 ticker
    pattern = r'\$([A-Z]{1,5})\b|\b([A-Z]{2,5})\b'
    matches = re.findall(pattern, text)
    tickers = set()
    for m in matches:
        ticker = m[0] or m[1]
        # 排除常见英文单词
        common_words = {
            "THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU", "ALL", "CAN",
            "HAS", "HAD", "WAS", "ONE", "OUT", "WILL", "NEW", "NOW", "ITS",
            "A", "I", "AN", "AT", "BE", "DO", "GO", "HE", "IF", "IN", "IS",
            "IT", "ME", "MY", "NO", "OF", "ON", "OR", "SO", "TO", "UP", "US",
            "WE", "AM", "PM", "CEO", "CFO", "AI", "API", "CEO", "CTO", "USA",
            "UK", "EU", "IPO", "ETF", "REIT", "YTD",
        }
        if ticker and ticker not in common_words and len(ticker) >= 2:
            tickers.add(ticker)
    return list(tickers)


def compute_weighted_score(article: dict) -> float:
    """
    综合计算文章权重分数
    考虑: 来源、评分、评论数、是否多源验证
    """
    score = 0.0

    # 来源基础分
    source_weights = {
        "TLDR": 9.0, "TLDR AI": 8.5, "TLDR Crypto": 8.5,
        "HackerNews": 7.0, "Reddit": 5.0,
        "NewsAPI": 6.0, "Finnhub": 6.5,
        "AlphaVantage": 6.0, "SEC EDGAR": 8.0,
        "YahooFinance": 5.5, "CoinGecko": 6.0,
    }
    score += source_weights.get(article.get("source", ""), 4.0)

    # platform score
    platform_score = article.get("score") or 0
    if platform_score > 0:
        score += min(platform_score / 20, 5)

    # 评论
    num_comments = article.get("num_comments") or 0
    if num_comments > 0:
        score += min(num_comments / 10, 3)

    return round(score, 1)
