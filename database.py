"""
数据库操作层 — SQLite (MVP)，后续可切换到 PostgreSQL
"""

import sqlite3
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from config import DATABASE_PATH


def get_conn() -> sqlite3.Connection:
    Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """初始化数据库表"""
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS news_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            source_topic TEXT,
            url TEXT NOT NULL,
            title TEXT NOT NULL,
            summary TEXT,
            content_preview TEXT,
            published_at TEXT,
            fetched_at TEXT NOT NULL,
            category TEXT NOT NULL,
            language TEXT DEFAULT 'en',
            score REAL,
            num_comments INTEGER,
            author TEXT,
            unique_hash TEXT UNIQUE,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_news_category ON news_articles(category);
        CREATE INDEX IF NOT EXISTS idx_news_fetched ON news_articles(fetched_at);
        CREATE INDEX IF NOT EXISTS idx_news_source ON news_articles(source);
        CREATE INDEX IF NOT EXISTS idx_news_hash ON news_articles(unique_hash);
        CREATE INDEX IF NOT EXISTS idx_news_published ON news_articles(published_at);

        CREATE TABLE IF NOT EXISTS entity_mentions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_url TEXT NOT NULL,
            entity_name TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            ticker TEXT,
            sector TEXT,
            relevance_score REAL DEFAULT 1.0,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_entity_ticker ON entity_mentions(ticker);
        CREATE INDEX IF NOT EXISTS idx_entity_type ON entity_mentions(entity_type);

        CREATE TABLE IF NOT EXISTS market_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            date TEXT NOT NULL,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            source TEXT NOT NULL,
            fetched_at TEXT NOT NULL,
            UNIQUE(ticker, date, source)
        );

        CREATE INDEX IF NOT EXISTS idx_market_ticker ON market_data(ticker);
        CREATE INDEX IF NOT EXISTS idx_market_date ON market_data(date);

        CREATE TABLE IF NOT EXISTS daily_briefs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            domain TEXT NOT NULL,
            top_stories TEXT DEFAULT '[]',
            summary TEXT DEFAULT '',
            market_impact TEXT DEFAULT '[]',
            opportunities TEXT DEFAULT '[]',
            raw_ai_response TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_briefs_date ON daily_briefs(date);
        CREATE INDEX IF NOT EXISTS idx_briefs_domain ON daily_briefs(domain);

        CREATE TABLE IF NOT EXISTS watched_stocks (
            ticker TEXT PRIMARY KEY,
            company_name TEXT NOT NULL,
            sector TEXT NOT NULL,
            subsector TEXT,
            watch_reason TEXT,
            added_at TEXT DEFAULT (datetime('now')),
            last_reviewed_at TEXT
        );

        CREATE TABLE IF NOT EXISTS ai_insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            insight_type TEXT NOT NULL,
            content TEXT NOT NULL,
            related_tickers TEXT DEFAULT '[]',
            related_news_urls TEXT DEFAULT '[]',
            confidence_score REAL,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_insights_date ON ai_insights(date);
        CREATE INDEX IF NOT EXISTS idx_insights_type ON ai_insights(insight_type);
    """)
    conn.commit()
    conn.close()


# ── 新闻文章 CRUD ──

def hash_article(url: str, title: str) -> str:
    """生成文章唯一哈希"""
    return hashlib.md5(f"{url}|{title[:100]}".encode()).hexdigest()


def insert_article(article: dict) -> Optional[int]:
    """插入单篇新闻，返回 id；如已存在（哈希冲突）则跳过"""
    article["unique_hash"] = hash_article(article.get("url", ""), article.get("title", ""))
    conn = get_conn()
    try:
        cursor = conn.execute("""
            INSERT OR IGNORE INTO news_articles
                (source, source_topic, url, title, summary, content_preview,
                 published_at, fetched_at, category, language, score, num_comments, author, unique_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            article.get("source", ""),
            article.get("source_topic", ""),
            article.get("url", ""),
            article.get("title", ""),
            article.get("summary", ""),
            article.get("content_preview", ""),
            article.get("published_at", ""),
            article.get("fetched_at", datetime.now().isoformat()),
            article.get("category", "tech"),
            article.get("language", "en"),
            article.get("score"),
            article.get("num_comments"),
            article.get("author"),
            article["unique_hash"],
        ))
        conn.commit()
        return cursor.lastrowid if cursor.lastrowid else None
    finally:
        conn.close()


def insert_articles_batch(articles: list[dict]) -> int:
    """批量插入文章，返回成功插入的数量"""
    count = 0
    for article in articles:
        if insert_article(article):
            count += 1
    return count


def get_todays_articles(date_str: Optional[str] = None) -> list[dict]:
    """获取今日所有文章"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    conn = get_conn()
    try:
        rows = conn.execute("""
            SELECT * FROM news_articles
            WHERE fetched_at >= ? AND fetched_at < ?
            ORDER BY score DESC NULLS LAST
        """, (f"{date_str}T00:00:00", f"{date_str}T23:59:59"))
        return [dict(r) for r in rows.fetchall()]
    finally:
        conn.close()


def get_recent_articles(days: int = 7, category: Optional[str] = None) -> list[dict]:
    """获取最近 N 天的文章"""
    conn = get_conn()
    try:
        query = """
            SELECT * FROM news_articles
            WHERE fetched_at >= datetime('now', ?)
        """
        params = [f"-{days} days"]
        if category:
            query += " AND category = ?"
            params.append(category)
        query += " ORDER BY score DESC NULLS LAST"
        rows = conn.execute(query, params)
        return [dict(r) for r in rows.fetchall()]
    finally:
        conn.close()


# ── 市场数据 CRUD ──

def insert_market_data(data: dict):
    conn = get_conn()
    try:
        conn.execute("""
            INSERT OR REPLACE INTO market_data
                (ticker, date, open, high, low, close, volume, source, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["ticker"], data["date"],
            data.get("open"), data.get("high"), data.get("low"),
            data.get("close"), data.get("volume"),
            data.get("source", ""), datetime.now().isoformat(),
        ))
        conn.commit()
    finally:
        conn.close()


# ── 每日摘要 CRUD ──

def save_daily_brief(brief: dict):
    conn = get_conn()
    try:
        conn.execute("""
            INSERT OR REPLACE INTO daily_briefs
                (date, domain, top_stories, summary, market_impact, opportunities, raw_ai_response)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            brief["date"], brief["domain"],
            json.dumps(brief.get("top_stories", []), ensure_ascii=False),
            brief.get("summary", ""),
            json.dumps(brief.get("market_impact", []), ensure_ascii=False),
            json.dumps(brief.get("opportunities", []), ensure_ascii=False),
            brief.get("raw_ai_response", ""),
        ))
        conn.commit()
    finally:
        conn.close()


def get_daily_brief(date_str: str, domain: Optional[str] = None) -> list[dict]:
    conn = get_conn()
    try:
        if domain:
            rows = conn.execute(
                "SELECT * FROM daily_briefs WHERE date = ? AND domain = ?",
                (date_str, domain)
            )
        else:
            rows = conn.execute(
                "SELECT * FROM daily_briefs WHERE date = ?", (date_str,)
            )
        return [dict(r) for r in rows.fetchall()]
    finally:
        conn.close()


# ── AI 洞察 CRUD ──

def save_insight(insight: dict):
    conn = get_conn()
    try:
        conn.execute("""
            INSERT INTO ai_insights (date, insight_type, content, related_tickers, related_news_urls, confidence_score)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            insight["date"], insight["insight_type"], insight["content"],
            json.dumps(insight.get("related_tickers", [])),
            json.dumps(insight.get("related_news_urls", [])),
            insight.get("confidence_score"),
        ))
        conn.commit()
    finally:
        conn.close()
