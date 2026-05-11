"""
NewsTracker — 每日科技与投资资讯追踪系统 主入口

用法:
    # 执行一次完整采集+分析
    python main.py

    # 只采集数据，不做 AI 分析
    python main.py --ingest-only

    # 只做 AI 分析（基于已有数据）
    python main.py --analyze-only

    # 启动定时调度模式
    python main.py --schedule

    # 查看帮助
    python main.py --help
"""

import argparse
import asyncio
import sys
from datetime import datetime
from pathlib import Path

from database import (
    init_db,
    get_todays_articles,
    get_recent_articles,
    insert_articles_batch,
    save_daily_brief,
)
from processing.cleaner import clean_title, clean_summary, is_junk_article, compute_weighted_score
from processing.dedup import deduplicate_articles, merge_multi_source_signals
from processing.ner import analyze_articles_entities, extract_entities
from ai_analysis.deepseek_client import analyze_daily, analyze_opportunities
from output.report import (
    generate_markdown_report,
    save_report,
    generate_market_summary,
    print_console_summary,
)

# ── 采集模块 ──
from ingestion.tldr import ingest_tldr
from ingestion.hackernews import ingest_hackernews
from ingestion.reddit import ingest_reddit
from ingestion.newsapi import ingest_newsapi
from ingestion.coingecko import ingest_coingecko
from ingestion.yfinance_data import ingest_yfinance
from ingestion.alphavantage import ingest_alphavantage
from ingestion.sec_edgar import ingest_sec_edgar
from ingestion.fred import ingest_fred
from ingestion.eia import ingest_eia
from ingestion.finnhub import ingest_finnhub


async def run_ingestion(verbose: bool = True) -> dict:
    """
    执行全部数据采集
    返回: {
        "articles": {domain: [articles]},
        "market_data": [...],
        "economic_data": [...],
        "stats": {source: count}
    }
    """
    stats = {}

    # TLDR (RSS + API) — 最先执行，作为基准信号
    if verbose:
        print("\n📡 [1/10] TLDR...")
    stats["tldr"] = await ingest_tldr()

    # Hacker News
    if verbose:
        print("\n📡 [2/10] Hacker News...")
    stats["hackernews"] = await ingest_hackernews(limit=100)

    # Reddit
    if verbose:
        print("\n📡 [3/10] Reddit...")
    stats["reddit"] = await ingest_reddit(per_sub_limit=20)

    # NewsAPI
    if verbose:
        print("\n📡 [4/10] NewsAPI...")
    stats["newsapi"] = await ingest_newsapi()

    # CoinGecko
    if verbose:
        print("\n📡 [5/10] CoinGecko...")
    stats["coingecko"] = await ingest_coingecko()

    # Yahoo Finance
    if verbose:
        print("\n📡 [6/10] Yahoo Finance...")
    stats["yfinance"] = await ingest_yfinance()

    # Alpha Vantage
    if verbose:
        print("\n📡 [7/10] Alpha Vantage...")
    stats["alphavantage"] = await ingest_alphavantage()

    # SEC EDGAR
    if verbose:
        print("\n📡 [8/10] SEC EDGAR...")
    stats["sec_edgar"] = await ingest_sec_edgar()

    # FRED
    if verbose:
        print("\n📡 [9/10] FRED...")
    stats["fred"] = await ingest_fred()

    # Finnhub + EIA
    if verbose:
        print("\n📡 [10/10] Finnhub + EIA...")
    finnhub_task = ingest_finnhub()
    eia_task = ingest_eia()
    stats["finnhub"], stats["eia"] = await asyncio.gather(finnhub_task, eia_task)

    return stats


def get_articles_by_domain() -> dict:
    """从数据库获取今日文章，按领域分组"""
    today = datetime.now().strftime("%Y-%m-%d")
    all_articles = get_todays_articles(today)

    if not all_articles:
        print("[WARNING] 今日数据库中没有文章，请先运行 --ingest-only")

    # 清理 + 过滤
    cleaned = []
    for a in all_articles:
        title = clean_title(a.get("title", ""))
        if is_junk_article(title):
            continue
        a["title"] = title
        a["summary"] = clean_summary(a.get("summary", ""))
        cleaned.append(a)

    # 去重
    cleaned = deduplicate_articles(cleaned)

    # 多源共振
    cleaned = merge_multi_source_signals(cleaned)

    # 计算加权分数
    for a in cleaned:
        a["weighted_score"] = compute_weighted_score(a)

    # 按分数排序
    cleaned.sort(key=lambda x: x.get("weighted_score", 0), reverse=True)

    # 按领域分组
    by_domain = {}
    for article in cleaned:
        domain = article.get("category", "tech")
        if domain not in by_domain:
            by_domain[domain] = []
        by_domain[domain].append(article)

    return by_domain


def get_market_data() -> tuple[list, list]:
    """获取市场数据和经济数据"""
    from database import get_conn
    conn = get_conn()
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        market_rows = conn.execute("""
            SELECT DISTINCT ticker, date, close, open, high, low, source
            FROM market_data
            WHERE date >= ?
            ORDER BY ticker, date DESC
        """, (today,)).fetchall()
        market_data = [dict(r) for r in market_rows]

        econ_rows = conn.execute("""
            SELECT ticker, date, close, source
            FROM market_data
            WHERE ticker LIKE 'ECON:%' OR ticker LIKE 'ENERGY:%'
            ORDER BY date DESC
            LIMIT 30
        """).fetchall()
        economic_data = [dict(r) for r in econ_rows]

        return market_data, economic_data
    finally:
        conn.close()


async def run_full_pipeline():
    """执行完整采集 + AI 分析"""
    start_time = datetime.now()
    print(f"\n{'='*60}")
    print(f"🚀 NewsTracker 开始执行 — {start_time.isoformat()}")
    print(f"{'='*60}")

    # 确保数据库初始化
    init_db()

    # ── 阶段 1: 数据采集 ──
    print("\n" + "─" * 40)
    print("📥 阶段 1: 数据采集")
    print("─" * 40)

    stats = await run_ingestion(verbose=True)

    total_fetched = sum(v for v in stats.values() if isinstance(v, int))
    print(f"\n📊 采集统计: {json.dumps(stats, indent=2)}")
    print(f"📊 总计入库: {total_fetched} 篇")

    # ── 阶段 2: 数据处理 ──
    print("\n" + "─" * 40)
    print("🔧 阶段 2: 数据处理与 NER")
    print("─" * 40)

    articles_by_domain = get_articles_by_domain()
    market_data, economic_data = get_market_data()

    total_articles = sum(len(v) for v in articles_by_domain.values())
    print(f"处理后文章数: {total_articles} (去重过滤后)")

    # 实体识别
    all_articles_flat = []
    for articles in articles_by_domain.values():
        all_articles_flat.extend(articles)
    entity_analysis = analyze_articles_entities(all_articles_flat)
    print(f"识别到 {len(entity_analysis['top_tickers'])} 个高频股票, {len(entity_analysis['top_tech_keywords'])} 个技术关键词")

    # ── 阶段 3: AI 分析 ──
    print("\n" + "─" * 40)
    print("🤖 阶段 3: DeepSeek AI 分析")
    print("─" * 40)

    recent_articles = get_recent_articles(days=7)

    print("  → 调用 DeepSeek 综合每日分析...")
    ai_analysis = analyze_daily(
        articles_by_domain=articles_by_domain,
        market_data=market_data,
        economic_data=economic_data,
        recent_articles=recent_articles[:30],
    )

    print("  → 调用 DeepSeek 发现投资/创业机会...")
    opportunities = analyze_opportunities(
        top_articles=all_articles_flat[:30],
        tech_trends=entity_analysis["top_tech_keywords"],
    )

    # 合并 AI 结果
    full_ai_response = f"{ai_analysis}\n\n---\n\n## 💡 机会发现\n\n{opportunities}"

    # ── 阶段 4: 输出 ──
    print("\n" + "─" * 40)
    print("📄 阶段 4: 生成报告")
    print("─" * 40)

    market_summary = generate_market_summary(market_data, economic_data)
    report = generate_markdown_report(
        ai_analysis=full_ai_response,
        articles_by_domain=articles_by_domain,
        market_summary=market_summary,
    )

    date_str = datetime.now().strftime("%Y-%m-%d")
    filepath = save_report(report, date_str)
    print(f"完整报告: {filepath}")

    # 保存 AI 分析到数据库 (UI 读取)
    for domain, articles in articles_by_domain.items():
        top_stories = []
        for a in articles[:10]:
            top_stories.append({
                "title": a.get("title", ""),
                "source": a.get("source", ""),
                "url": a.get("url", ""),
                "score": a.get("weighted_score", 0),
            })
        save_daily_brief({
            "date": date_str,
            "domain": domain,
            "top_stories": top_stories,
            "summary": "",
            "market_impact": [],
            "opportunities": [],
            "raw_ai_response": "",
        })

    # 保存完整的 AI 分析结果
    save_daily_brief({
        "date": date_str,
        "domain": "all",
        "top_stories": [],
        "summary": "",
        "market_impact": [],
        "opportunities": [],
        "raw_ai_response": full_ai_response,
    })
    print("AI 分析已存入数据库")

    # ── 控制台摘要 ──
    print_console_summary(
        articles_by_domain=articles_by_domain,
        total_fetched=total_fetched,
        total_saved=total_articles,
        ai_chars=len(full_ai_response),
    )

    elapsed = (datetime.now() - start_time).total_seconds()
    print(f"\n✅ 全部完成! 耗时 {elapsed:.1f}s")
    return report


# ── CLI ──

import json  # noqa: E402 (需要放在顶部但为了避免冲突放这里)


def main():
    parser = argparse.ArgumentParser(
        description="NewsTracker — 每日科技与投资资讯追踪系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py                  # 完整采集 + AI 分析
  python main.py --ingest-only    # 只采集数据
  python main.py --analyze-only   # 只用已有数据做分析
  python main.py --schedule       # 启动定时调度（早7点+晚6点）
        """,
    )
    parser.add_argument("--ingest-only", action="store_true", help="只采集数据，不做 AI 分析")
    parser.add_argument("--analyze-only", action="store_true", help="基于已有数据做 AI 分析")
    parser.add_argument("--schedule", action="store_true", help="启动定时调度模式")
    parser.add_argument("--init-db", action="store_true", help="初始化数据库")

    args = parser.parse_args()

    # 初始化数据库
    init_db()

    if args.init_db:
        print("✅ 数据库已初始化")
        return

    if args.schedule:
        from scheduler import start_scheduler
        start_scheduler()
        return

    if args.ingest_only:
        print("📡 仅采集模式...")
        init_db()
        stats = asyncio.run(run_ingestion(verbose=True))
        total = sum(v for v in stats.values() if isinstance(v, int))
        print(f"\n✅ 采集完成! 入库 {total} 篇")
        return

    if args.analyze_only:
        print("🤖 仅分析模式...")
        init_db()
        articles_by_domain = get_articles_by_domain()
        market_data, economic_data = get_market_data()

        all_flat = []
        for articles in articles_by_domain.values():
            all_flat.extend(articles)
        entity_analysis = analyze_articles_entities(all_flat)

        recent = get_recent_articles(days=7)
        ai_analysis = analyze_daily(articles_by_domain, market_data, economic_data, recent[:30])
        opportunities = analyze_opportunities(all_flat[:30], entity_analysis["top_tech_keywords"])
        full_response = f"{ai_analysis}\n\n---\n\n## 💡 机会发现\n\n{opportunities}"

        market_summary = generate_market_summary(market_data, economic_data)
        report = generate_markdown_report(full_response, articles_by_domain, market_summary)
        filepath = save_report(report)
        date_str = datetime.now().strftime("%Y-%m-%d")

        # 保存领域数据
        for domain, articles in articles_by_domain.items():
            save_daily_brief({
                "date": date_str, "domain": domain,
                "top_stories": [{"title": a.get("title",""), "source": a.get("source",""), "url": a.get("url",""), "score": a.get("weighted_score",0)} for a in articles[:10]],
                "summary": "", "market_impact": [], "opportunities": [], "raw_ai_response": "",
            })
        # 保存完整 AI 分析
        save_daily_brief({
            "date": date_str, "domain": "all",
            "top_stories": [], "summary": "", "market_impact": [], "opportunities": [],
            "raw_ai_response": full_response,
        })

        print(f"✅ 分析完成! 报告: {filepath}")
        print_console_summary(articles_by_domain, 0, sum(len(v) for v in articles_by_domain.values()), len(full_response))
        return

    # 默认: 完整采集 + AI 分析
    asyncio.run(run_full_pipeline())


if __name__ == "__main__":
    main()
