"""
每日报告生成模块
支持: Markdown 文件输出 + 控制台 Rich 输出
"""

import json
from datetime import datetime
from pathlib import Path

from config import OUTPUT_DIR


def generate_markdown_report(
    ai_analysis: str,
    articles_by_domain: dict,
    market_summary: str,
    date_str: str | None = None,
) -> str:
    """生成 Markdown 格式的每日报告"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    total_articles = sum(len(v) for v in articles_by_domain.values())
    domains = {
        "tech": "互联网/科技",
        "crypto": "加密货币",
        "energy": "能源科技",
        "semiconductor": "半导体",
        "investing": "美股/投资",
    }

    md = f"""# 📊 每日科技与投资资讯分析

**日期**: {date_str}
**采集文章数**: {total_articles} 篇
**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 📈 数据概览

| 领域 | 文章数 |
|------|--------|
"""
    for domain, label in domains.items():
        count = len(articles_by_domain.get(domain, []))
        md += f"| {label} | {count} |\n"

    md += f"\n{market_summary}\n"

    md += f"\n---\n\n## 🤖 AI 深度分析\n\n{ai_analysis}\n\n"

    md += "\n---\n\n## ⚠️ 免责声明\n\n"
    md += "本报告由 AI 自动生成，所有分析和建议仅供参考，不构成投资建议。"
    md += "投资有风险，决策需谨慎。信息来源包括多个公开 API，AI 分析可能存在错误或遗漏。\n"

    return md


def save_report(content: str, date_str: str | None = None, format: str = "md") -> Path:
    """保存报告到文件"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    filename = f"daily_report_{date_str}.{format}"
    filepath = OUTPUT_DIR / filename
    filepath.write_text(content, encoding="utf-8")
    print(f"[Report] 报告已保存: {filepath}")
    return filepath


def generate_market_summary(market_data: list, economic_data: list) -> str:
    """生成市场概览"""
    lines = ["### 核心市场数据\n"]

    # 关键股票
    key_tickers = ["NVDA", "AMD", "TSLA", "AAPL", "MSFT", "QQQ", "SPY"]
    stock_data = [d for d in market_data if d.get("ticker") in key_tickers]
    if stock_data:
        lines.append("| Ticker | 价格 | 日期 |")
        lines.append("|--------|------|------|")
        for d in stock_data[:10]:
            close_val = d.get("close", "N/A")
            if close_val and close_val != "N/A":
                lines.append(f"| {d['ticker']} | ${float(close_val):.2f} | {d.get('date', '')} |")

    # 经济指标
    if economic_data:
        lines.append("\n### 宏观经济指标\n")
        lines.append("| 指标 | 数值 | 日期 |")
        lines.append("|------|------|------|")
        for d in economic_data[:10]:
            ticker = d.get("ticker", "").replace("ECON:", "")
            val = d.get("close", "N/A")
            lines.append(f"| {ticker} | {val} | {d.get('date', '')} |")

    return "\n".join(lines)


def print_console_summary(
    articles_by_domain: dict,
    total_fetched: int,
    total_saved: int,
    ai_chars: int = 0,
):
    """控制台彩色输出（使用 Rich）"""
    try:
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel

        console = Console()

        domains = {
            "tech": ("互联网/科技", "cyan"),
            "crypto": ("加密货币", "orange1"),
            "energy": ("能源科技", "green"),
            "semiconductor": ("半导体", "blue"),
            "investing": ("美股/投资", "yellow"),
        }

        # 概览面板
        console.print(Panel.fit(
            f"[bold]NewsTracker 每日采集执行完成[/bold]\n\n"
            f"📥 拉取总数: {total_fetched} 篇\n"
            f"💾 入库: {total_saved} 篇 (去重后)\n"
            f"🤖 AI 分析: {ai_chars} 字符生成\n"
            f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            title="执行摘要",
            border_style="bold white",
        ))

        # 领域分布表
        table = Table(title="各领域文章分布")
        table.add_column("领域", style="bold")
        table.add_column("数量", justify="right")
        table.add_column("占比", justify="right")

        total = sum(len(v) for v in articles_by_domain.values()) or 1
        for domain, (label, color) in domains.items():
            count = len(articles_by_domain.get(domain, []))
            pct = f"{count / total * 100:.1f}%"
            table.add_row(f"[{color}]{label}[/{color}]", str(count), pct)

        console.print(table)

    except ImportError:
        print(f"\n{'='*60}")
        print(f"NewsTracker 每日采集完成")
        print(f"拉取: {total_fetched} 篇 | 入库: {total_saved} 篇 | AI分析: {ai_chars} 字符")
        print(f"{'='*60}")
