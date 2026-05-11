"""
NewsTracker Web UI — Streamlit 仪表盘
启动: streamlit run app.py
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

from database import (
    init_db, get_conn, get_todays_articles, get_recent_articles,
    get_daily_brief,
)
from processing.cleaner import compute_weighted_score
from processing.dedup import deduplicate_articles, merge_multi_source_signals
from processing.ner import analyze_articles_entities

st.set_page_config(
    page_title="NewsTracker — 每日科技与投资资讯",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 初始化数据库
init_db()

# ── 侧边栏 ──
with st.sidebar:
    st.title("📊 NewsTracker")
    st.caption("AI 驱动的每日科技与投资资讯追踪")

    st.divider()

    # 日期选择
    selected_date = st.date_input(
        "📅 选择日期",
        value=datetime.now().date(),
        max_value=datetime.now().date(),
    )
    date_str = selected_date.strftime("%Y-%m-%d")

    # 快速跳转
    st.divider()
    show_section = st.radio(
        "📑 导航",
        ["📋 总览", "🤖 AI 深度分析", "📰 科技新闻", "🪙 加密货币", "⚡ 能源科技", "🔧 半导体", "📈 美股/投资", "💹 市场数据"],
    )

    st.divider()
    st.caption(f"⏰ 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")


# ── 数据加载 ──
@st.cache_data(ttl=300)
def load_data(date_str):
    """加载指定日期的数据"""
    articles = get_todays_articles(date_str)
    if not articles:
        # 如果没有今日数据，从最近7天加载
        articles = get_recent_articles(days=1)

    # 清理和去重
    from processing.cleaner import clean_title, clean_summary, is_junk_article
    cleaned = []
    for a in articles:
        a_dict = dict(a)
        title = clean_title(a_dict.get("title", ""))
        if is_junk_article(title):
            continue
        a_dict["title"] = title
        a_dict["summary"] = clean_summary(a_dict.get("summary", ""))
        cleaned.append(a_dict)

    cleaned = deduplicate_articles(cleaned)
    cleaned = merge_multi_source_signals(cleaned)

    for a in cleaned:
        a["weighted_score"] = compute_weighted_score(a)

    cleaned.sort(key=lambda x: x.get("weighted_score", 0), reverse=True)

    # 按领域分组
    by_domain = {}
    for a in cleaned:
        domain = a.get("category", "tech")
        if domain not in by_domain:
            by_domain[domain] = []
        by_domain[domain].append(a)

    # 获取 AI 分析
    briefs = get_daily_brief(date_str)

    # 获取市场数据
    conn = get_conn()
    market_rows = conn.execute("""
        SELECT DISTINCT ticker, date, close, open, high, low, volume, source
        FROM market_data
        WHERE date >= ?
        ORDER BY ticker, date DESC
    """, (date_str,)).fetchall()
    market_data = [dict(r) for r in market_rows]

    econ_rows = conn.execute("""
        SELECT ticker, date, close, source
        FROM market_data
        WHERE ticker LIKE 'ECON:%' OR ticker LIKE 'ENERGY:%'
        ORDER BY date DESC
        LIMIT 20
    """).fetchall()
    economic_data = [dict(r) for r in econ_rows]
    conn.close()

    # 实体分析
    all_flat = []
    for articles in by_domain.values():
        all_flat.extend(articles)
    entity_analysis = analyze_articles_entities(all_flat)

    return by_domain, market_data, economic_data, entity_analysis, briefs


by_domain, market_data, economic_data, entity_analysis, briefs = load_data(date_str)

total_articles = sum(len(v) for v in by_domain.values())

DOMAINS = {
    "tech": ("📰 互联网/科技", "科技"),
    "crypto": ("🪙 加密货币", "加密"),
    "energy": ("⚡ 能源科技", "能源"),
    "semiconductor": ("🔧 半导体", "半导体"),
    "investing": ("📈 美股/投资", "投资"),
}


def render_article_card(article, show_score=True):
    """渲染单篇文章卡片"""
    source_colors = {
        "TLDR": "#FF6B35", "TLDR AI": "#FF6B35", "TLDR Crypto": "#FF6B35",
        "HackerNews": "#FF6600", "Reddit": "#FF4500",
        "NewsAPI": "#2196F3", "Finnhub": "#4CAF50",
        "AlphaVantage": "#9C27B0", "SEC EDGAR": "#607D8B",
        "YahooFinance": "#7B1FA2", "CoinGecko": "#8BC34A",
    }
    color = source_colors.get(article.get("source", ""), "#999")

    with st.container():
        cols = st.columns([20, 1])
        with cols[0]:
            title = article.get("title", "")[:120]
            url = article.get("url", "")
            if url:
                st.markdown(f"**[{title}]({url})**")
            else:
                st.markdown(f"**{title}**")

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(f'<span style="color:{color};font-size:0.8em;">📌 {article.get("source", "")}</span>', unsafe_allow_html=True)
            with c2:
                if show_score and article.get("weighted_score"):
                    st.caption(f"⭐ {article['weighted_score']:.1f}")
            with c3:
                if article.get("score") or article.get("num_comments"):
                    st.caption(f"💬 {article.get('num_comments', 0)} 评论")
            with c4:
                if article.get("_multi_source"):
                    st.caption(f"🔗 {article.get('_source_count', 0)} 源共振")

            summary = article.get("summary", "")
            if summary:
                with st.expander("📄 摘要"):
                    st.write(summary[:500])


# ── 主页面渲染 ──

st.title("📊 NewsTracker — AI 科技与投资资讯追踪")

# 顶部统计卡片
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("📰 今日资讯", total_articles)
with col2:
    has_ai = any(b.get("domain") == "all" and b.get("raw_ai_response") for b in briefs)
    st.metric("🤖 AI 分析", "✅ 已生成" if has_ai else "待运行")
with col3:
    st.metric("💹 市场数据", len(market_data))
with col4:
    st.metric("🔬 技术关键词", len(entity_analysis.get("top_tech_keywords", [])))
with col5:
    st.metric("🏢 高频股票", len(entity_analysis.get("top_tickers", [])))

st.divider()

# ── 按导航渲染内容 ──

if show_section == "📋 总览":
    st.subheader("📋 今日资讯总览")

    # 各领域 Top 新闻
    for domain, (icon_label, short_label) in DOMAINS.items():
        articles = by_domain.get(domain, [])
        if not articles:
            continue
        st.markdown(f"### {icon_label} ({len(articles)} 条)")
        for article in articles[:5]:
            render_article_card(article)
        if len(articles) > 5:
            st.caption(f"... 还有 {len(articles) - 5} 条")
        st.divider()

elif show_section == "🤖 AI 深度分析":
    st.subheader("🤖 AI 深度分析")

    # 找到 all domain 的完整 AI 分析
    all_brief = None
    domain_briefs = {}
    for b in briefs:
        if b.get("domain") == "all":
            all_brief = b
        else:
            domain_briefs[b.get("domain", "")] = b

    if all_brief and all_brief.get("raw_ai_response"):
        raw = all_brief["raw_ai_response"]
        # AI 分析全文直接展示（不隐藏）
        st.markdown(raw)
    elif briefs:
        # 有领域数据但还没有 AI 分析
        st.info("📊 数据已采集，但 AI 分析尚未生成。请运行 `python main.py --analyze-only`")
    else:
        st.warning("""
        ⚠️ 今日暂无数据。

        请先在终端运行:
        ```
        cd /Users/charlie/all_code_projects/newstracker
        python main.py
        ```
        """)

        # 即使没有 AI 分析，也展示各领域数据概览
        st.divider()
        st.markdown("### 今日数据概览")

        cols = st.columns(5)
        for i, (domain, (icon_label, _)) in enumerate(DOMAINS.items()):
            with cols[i]:
                articles = by_domain.get(domain, [])
                st.metric(icon_label, len(articles))

        # 高频股票
        if entity_analysis["top_tickers"]:
            st.markdown("### 🏢 今日高频提及股票")
            ticker_df = pd.DataFrame(
                entity_analysis["top_tickers"][:15],
                columns=["股票", "提及次数"]
            )
            st.bar_chart(ticker_df.set_index("股票"))

        # 技术关键词
        if entity_analysis["top_tech_keywords"]:
            st.markdown("### 🔬 今日技术趋势关键词")
            tech_df = pd.DataFrame(
                entity_analysis["top_tech_keywords"][:15],
                columns=["关键词", "提及次数"]
            )
            st.bar_chart(tech_df.set_index("关键词"))

elif show_section in ["📰 科技新闻", "🪙 加密货币", "⚡ 能源科技", "🔧 半导体", "📈 美股/投资"]:
    domain_map = {
        "📰 科技新闻": "tech",
        "🪙 加密货币": "crypto",
        "⚡ 能源科技": "energy",
        "🔧 半导体": "semiconductor",
        "📈 美股/投资": "investing",
    }
    domain = domain_map[show_section]
    icon_label, short_label = DOMAINS[domain]
    articles = by_domain.get(domain, [])

    st.subheader(f"{icon_label} ({len(articles)} 条)")

    if not articles:
        st.info(f"今日暂无 {short_label} 领域的资讯。请先运行数据采集。")
    else:
        # 排序选项
        sort_by = st.selectbox("排序方式", ["综合权重", "热度评分", "评论数"], key=f"sort_{domain}")

        if sort_by == "热度评分":
            articles = sorted(articles, key=lambda x: x.get("score") or 0, reverse=True)
        elif sort_by == "评论数":
            articles = sorted(articles, key=lambda x: x.get("num_comments") or 0, reverse=True)

        # 分页
        page_size = 20
        page = st.number_input("页码", min_value=1, max_value=max(1, (len(articles) - 1) // page_size + 1), value=1, key=f"page_{domain}")
        start = (page - 1) * page_size
        end = start + page_size

        for article in articles[start:end]:
            render_article_card(article)

        st.caption(f"第 {page} 页，共 {len(articles)} 条")

elif show_section == "💹 市场数据":
    st.subheader("💹 市场数据")

    if market_data:
        # 关键股票筛选
        key_tickers = ["NVDA", "AMD", "TSLA", "AAPL", "MSFT", "QQQ", "SPY", "INTC", "AVGO", "COIN"]
        stock_data = [d for d in market_data if d["ticker"] in key_tickers]
        if stock_data:
            st.markdown("### 核心股票行情")
            stock_rows = []
            for d in stock_data:
                stock_rows.append({
                    "股票": d["ticker"],
                    "收盘价": f"${d.get('close', 'N/A')}" if d.get("close") else "N/A",
                    "最高": f"${d.get('high', 'N/A')}" if d.get("high") else "N/A",
                    "最低": f"${d.get('low', 'N/A')}" if d.get("low") else "N/A",
                    "数据源": d.get("source", ""),
                })
            df = pd.DataFrame(stock_rows).drop_duplicates(subset=["股票"], keep="first")
            st.dataframe(df, use_container_width=True, hide_index=True)

    if economic_data:
        st.markdown("### 宏观经济 & 能源指标")
        econ_rows = []
        for d in economic_data:
            ticker = d["ticker"].replace("ECON:", "").replace("ENERGY:", "")
            econ_rows.append({
                "指标": ticker,
                "数值": d.get("close", "N/A"),
                "日期": d.get("date", ""),
                "数据源": d.get("source", ""),
            })
        if econ_rows:
            df = pd.DataFrame(econ_rows)
            st.dataframe(df, use_container_width=True, hide_index=True)

    # 技术趋势
    if entity_analysis["top_tickers"]:
        st.markdown("### 🏢 新闻中高频提及股票 TOP 15")
        ticker_df = pd.DataFrame(entity_analysis["top_tickers"][:15], columns=["股票代码", "提及次数"])
        st.bar_chart(ticker_df.set_index("股票代码"), use_container_width=True)

    if entity_analysis["top_tech_keywords"]:
        st.markdown("### 🔬 技术趋势关键词 TOP 15")
        kw_df = pd.DataFrame(entity_analysis["top_tech_keywords"][:15], columns=["关键词", "提及次数"])
        st.bar_chart(kw_df.set_index("关键词"), use_container_width=True)


# ── 页脚 ──
st.divider()
st.caption("⚠️ 本系统所有分析仅供参考，不构成投资建议。数据来源包括 TLDR、Hacker News、Reddit、NewsAPI、CoinGecko、Yahoo Finance、SEC EDGAR、Alpha Vantage、Finnhub、FRED、EIA。")
st.caption(f"© 2026 NewsTracker | 数据更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
