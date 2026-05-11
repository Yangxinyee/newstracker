"""
数据模型定义 — 使用 Pydantic 进行数据验证
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class NewsArticle(BaseModel):
    """统一新闻文章模型"""
    source: str
    source_topic: Optional[str] = None
    url: str
    title: str
    summary: Optional[str] = None
    content_preview: Optional[str] = Field(default=None, max_length=2000)
    published_at: Optional[str] = None
    fetched_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    category: str  # tech, crypto, energy, semiconductor, investing
    language: str = "en"
    score: Optional[float] = None  # 来源平台的热度评分
    num_comments: Optional[int] = None
    author: Optional[str] = None
    # 去重和唯一标识
    unique_hash: Optional[str] = None

    class Config:
        extra = "allow"


class MarketData(BaseModel):
    """市场行情数据"""
    ticker: str
    date: str
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[int] = None
    source: str
    fetched_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class EntityMention(BaseModel):
    """新闻中的实体提及"""
    article_url: str
    entity_name: str
    entity_type: str  # COMPANY, TICKER, PERSON, TECHNOLOGY, PRODUCT
    ticker: Optional[str] = None
    sector: Optional[str] = None
    relevance_score: float = 1.0


class DailyBrief(BaseModel):
    """AI 生成的每日摘要"""
    date: str
    domain: str
    top_stories: list = Field(default_factory=list)
    summary: str = ""
    market_impact: list = Field(default_factory=list)
    opportunities: list = Field(default_factory=list)
    raw_ai_response: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class WatchedStock(BaseModel):
    """追踪标的"""
    ticker: str
    company_name: str
    sector: str
    subsector: Optional[str] = None
    watch_reason: Optional[str] = None
    added_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class AInsight(BaseModel):
    """AI 分析洞察"""
    date: str
    insight_type: str  # daily_summary, stock_impact, opportunity, risk_alert
    content: str
    related_tickers: list = Field(default_factory=list)
    related_news_urls: list = Field(default_factory=list)
    confidence_score: Optional[float] = None
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
