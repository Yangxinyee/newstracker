"""
去重模块
- URL 精确去重
- 标题相似度去重 (Jaccard + 前缀匹配)
"""

import re
from difflib import SequenceMatcher


def tokenize(text: str) -> set[str]:
    """文本分词"""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return set(text.split())


def title_similarity(title1: str, title2: str) -> float:
    """计算两个标题的相似度"""
    # 方法 1: Jaccard
    tokens1 = tokenize(title1)
    tokens2 = tokenize(title2)
    if not tokens1 or not tokens2:
        return 0.0

    jaccard = len(tokens1 & tokens2) / len(tokens1 | tokens2)

    # 方法 2: 字符级 SequenceMatcher
    seq_sim = SequenceMatcher(None, title1.lower()[:200], title2.lower()[:200]).ratio()

    return max(jaccard, seq_sim)


def deduplicate_articles(
    articles: list[dict],
    title_sim_threshold: float = 0.75,
) -> list[dict]:
    """
    去重：URL 精确 + 标题相似度
    保留 score 最高的那条
    """
    # 先按 source weight + score 排序
    from processing.cleaner import compute_weighted_score
    articles = sorted(articles, key=lambda a: compute_weighted_score(a), reverse=True)

    seen_urls = set()
    seen_title_tokens: list[set[str]] = []
    unique = []

    for article in articles:
        url = article.get("url", "").strip().rstrip("/")

        # URL 精确去重
        if url and url in seen_urls:
            continue

        # 标题相似度去重
        title = article.get("title", "").strip()
        if not title:
            continue

        tokens = tokenize(title)
        is_dup = False
        for prev_tokens in seen_title_tokens[-200:]:  # 只比较最近 200 条
            if not prev_tokens or not tokens:
                continue
            sim = len(tokens & prev_tokens) / max(len(tokens | prev_tokens), 1)
            if sim >= title_sim_threshold:
                is_dup = True
                break

        if is_dup:
            continue

        if url:
            seen_urls.add(url)
        seen_title_tokens.append(tokens)
        unique.append(article)

    return unique


def merge_multi_source_signals(articles: list[dict]) -> list[dict]:
    """
    检测多源共振：同一事件在不同数据源中出现
    如果同一标题在多个源出现，提升其权重
    """
    # 构建标题聚类
    clusters = []

    for article in articles:
        title = article.get("title", "")
        matched = False
        for cluster in clusters:
            for ref_title in cluster["titles"]:
                if title_similarity(title, ref_title) > 0.8:
                    cluster["articles"].append(article)
                    cluster["titles"].append(title)
                    cluster["sources"].add(article.get("source", ""))
                    matched = True
                    break
            if matched:
                break

        if not matched:
            clusters.append({
                "titles": [title],
                "sources": {article.get("source", "")},
                "articles": [article],
            })

    # 对多源共振的文章，提升 score
    for cluster in clusters:
        source_count = len(cluster["sources"])
        if source_count >= 3:
            bonus = source_count * 5  # 每个源 +5 分
            for article in cluster["articles"]:
                article["score"] = (article.get("score") or 0) + bonus
                article["_multi_source"] = True
                article["_source_count"] = source_count

    return articles
