"""
DeepSeek AI 分析客户端
使用 OpenAI SDK 连接到 DeepSeek API
参考代码: reasoning_effort="high", extra_body={"thinking": {"type": "enabled"}}
"""

import json
import os
from datetime import datetime

from openai import OpenAI

from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL

client = OpenAI(
    api_key=DEEPSEEK_API_KEY or os.environ.get("DEEPSEEK_API_KEY", ""),
    base_url=DEEPSEEK_BASE_URL,
)

SYSTEM_PROMPT = """你是一位世界顶级的科技与投资分析师，具备以下背景：
- 曾在顶级对冲基金做科技行业研究
- 深谙半导体、能源、AI、加密、互联网五大科技赛道
- 熟悉美股市场，能精准判断新闻对股价的多空影响
- 擅长识别技术趋势与投资机会的交叉点

你的分析风格：精准、有洞察力、不模棱两可。每条结论都要有依据。
回复语言：中文。

重要：所有分析均需标注"⚠️ 仅供参考，不构成投资建议"。"""


def _build_analysis_prompt(articles_by_domain: dict, market_data: list, economic_data: list, recent_articles: list) -> str:
    """构建分析 Prompt"""
    today = datetime.now().strftime("%Y-%m-%d")
    domains = {
        "tech": "互联网/科技",
        "crypto": "加密货币/区块链",
        "energy": "能源科技",
        "semiconductor": "半导体",
        "investing": "美股/投资",
    }

    sections = []
    for domain, label in domains.items():
        articles = articles_by_domain.get(domain, [])
        if not articles:
            sections.append(f"## {label}\n今日无数据。")
            continue

        lines = [f"## {label} ({len(articles)} 条)"]
        for i, a in enumerate(articles[:15]):
            lines.append(f"\n### {i+1}. {a.get('title', '')}")
            lines.append(f"- 来源: {a.get('source', '')} | 热度: {a.get('score', 'N/A')}")
            if a.get("summary"):
                lines.append(f"- 摘要: {a.get('summary', '')[:300]}")
            if a.get("url"):
                lines.append(f"- 链接: {a.get('url', '')}")
            if a.get("num_comments"):
                lines.append(f"- 评论数: {a.get('num_comments', 0)}")
        sections.append("\n".join(lines))

    news_section = "\n\n".join(sections)

    # 市场数据
    market_lines = ["## 市场数据"]
    for d in market_data[:30]:
        market_lines.append(
            f"- {d.get('ticker', '')}: ${d.get('close', 'N/A')} "
            f"(O:{d.get('open', 'N/A')} H:{d.get('high', 'N/A')} L:{d.get('low', 'N/A')})"
        )
    market_section = "\n".join(market_lines)

    # 经济数据
    econ_lines = ["## 宏观经济指标"]
    for d in economic_data[:15]:
        econ_lines.append(f"- {d.get('ticker', '')}: {d.get('close', 'N/A')} ({d.get('date', '')})")
    econ_section = "\n".join(econ_lines)

    # 近7天热点回顾
    recent_lines = ["## 近7天热点回顾"]
    for a in recent_articles[:20]:
        recent_lines.append(f"- [{a.get('source', '')}] {a.get('title', '')}")
    recent_section = "\n".join(recent_lines)

    return f"""# 每日科技与投资资讯分析 — {today}

{news_section}

{market_section}

{econ_section}

{recent_section}

---
请基于以上信息，完成以下分析任务：

## 任务
1. **每日要点**：每个领域总结 3-5 条最关键动态，用中文简洁总结，突出最重要的内容。
2. **跨领域关联**：识别跨领域的技术趋势交汇点（如：AI芯片突破→利好半导体设备→影响能源需求）。
3. **美股影响分析**：列出受影响最大的 5-10 只股票，判断利多/利空/中性，给出置信度（高/中/低），说明理由。
4. **低估标的发现**：基于今日资讯+历史趋势，发现 1-3 个可能被市场低估的投资标的，说明理由。
5. **创业机会识别**：识别 1-3 个低资金门槛、前沿的科技创业方向，说明为什么现在是好时机。
6. **风险预警**：列出今日值得关注的 3-5 个负面信号或风险。

## 输出格式
用结构化的 Markdown 格式输出，每个部分用 ## 标题分隔。每个结论要有具体依据，标注信息来源。"""


def analyze_daily(
    articles_by_domain: dict,
    market_data: list,
    economic_data: list,
    recent_articles: list,
) -> str:
    """执行每日 AI 综合分析"""
    if not DEEPSEEK_API_KEY and not os.environ.get("DEEPSEEK_API_KEY"):
        return "⚠️ DeepSeek API Key 未配置，无法生成 AI 分析。请设置 DEEPSEEK_API_KEY 环境变量。"

    user_prompt = _build_analysis_prompt(
        articles_by_domain, market_data, economic_data, recent_articles
    )

    # 截断 prompt 如果过长 (DeepSeek 有 token 限制)
    if len(user_prompt) > 60000:
        user_prompt = user_prompt[:60000] + "\n\n[内容过长已截断]"

    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            stream=False,
            reasoning_effort="high",
            extra_body={"thinking": {"type": "enabled"}},
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        return f"❌ DeepSeek API 调用失败: {e}"


def analyze_stock_impact(article: dict, stock_context: str = "") -> str:
    """单独分析单条新闻对特定股票的影响"""
    if not DEEPSEEK_API_KEY and not os.environ.get("DEEPSEEK_API_KEY"):
        return "⚠️ DeepSeek API Key 未配置。"

    ticker = article.get("_ticker", "Unknown")
    prompt = f"""请分析以下新闻对 {ticker} 股票的影响：

标题: {article.get('title', '')}
摘要: {article.get('summary', '')}
来源: {article.get('source', '')}
{stock_context}

请判断：
1. 利多/利空/中性？
2. 影响程度（1-5分）
3. 影响时间维度（短期/中期/长期）
4. 简要理由（50字以内）

输出格式: JSON {{"direction": "bullish|bearish|neutral", "impact_score": 1-5, "timeframe": "short|medium|long", "reason": "..."}}"""

    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {"role": "system", "content": "你是专业的股票分析师，回复简洁精准的JSON。"},
                {"role": "user", "content": prompt},
            ],
            stream=False,
            reasoning_effort="high",
            extra_body={"thinking": {"type": "enabled"}},
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        return json.dumps({"error": str(e)})


def analyze_opportunities(top_articles: list, tech_trends: list) -> str:
    """识别创业和投资机会"""
    if not DEEPSEEK_API_KEY and not os.environ.get("DEEPSEEK_API_KEY"):
        return "⚠️ DeepSeek API Key 未配置。"

    articles_text = "\n".join([
        f"- [{a.get('source', '')}] {a.get('title', '')}"
        for a in top_articles[:30]
    ])
    trends_text = "\n".join([
        f"- {t[0]} (提及 {t[1]} 次)" for t in tech_trends[:20]
    ]) if tech_trends else "无趋势数据"

    prompt = f"""基于以下信息，识别投资和创业机会：

## 今日科技要闻
{articles_text}

## 技术趋势热度
{trends_text}

## 任务
1. 识别 1-3 个低资金门槛、超前的科技创业方向。每个方向说明:
   - 为什么现在是好时机
   - 需要什么技术能力
   - 市场规模潜力
2. 识别 1-3 个可能被市场低估的美股标的。每个标的说明:
   - 低估理由
   - 催化事件
   - 风险提示

输出用中文 Markdown。每条建议标注 ⚠️ 仅供参考。"""

    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {"role": "system", "content": "你是硅谷顶级VC合伙人兼对冲基金科技行业分析师，眼光独到，善于发现被忽视的机会。"},
                {"role": "user", "content": prompt},
            ],
            stream=False,
            reasoning_effort="high",
            extra_body={"thinking": {"type": "enabled"}},
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        return f"❌ DeepSeek API 调用失败: {e}"
