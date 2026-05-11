"""
NewsTracker 全局配置
复制此文件为 .env 并填入实际的 API Keys
"""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# ── 数据库 ──
DATABASE_PATH = os.environ.get("DATABASE_PATH", str(BASE_DIR / "data" / "newstracker.db"))

# ── DeepSeek AI ──
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-v4-pro"

# ── NewsAPI ──
NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY", "")

# ── Reddit ──
REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT = os.environ.get("REDDIT_USER_AGENT", "NewsTracker/1.0")

# ── Alpha Vantage ──
ALPHA_VANTAGE_KEY = os.environ.get("ALPHA_VANTAGE_KEY", "")

# ── Finnhub ──
FINNHUB_KEY = os.environ.get("FINNHUB_KEY", "")

# ── FRED ──
FRED_API_KEY = os.environ.get("FRED_API_KEY", "")

# ── EIA ──
EIA_API_KEY = os.environ.get("EIA_API_KEY", "")

# ── CryptoCompare ──
CRYPTOCOMPARE_KEY = os.environ.get("CRYPTOCOMPARE_KEY", "")

# ── 调度配置 ──
MORNING_RUN_HOUR = int(os.environ.get("MORNING_RUN_HOUR", "7"))  # 北京时间早上 7 点
EVENING_RUN_HOUR = int(os.environ.get("EVENING_RUN_HOUR", "18"))  # 北京时间晚上 6 点

# ── 输出配置 ──
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", str(BASE_DIR / "data" / "reports")))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── 日志 ──
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
