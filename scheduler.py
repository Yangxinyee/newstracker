"""
定时调度模块
使用 APScheduler 实现每日定时采集和分析
"""

from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from main import run_full_pipeline
from config import MORNING_RUN_HOUR, EVENING_RUN_HOUR


def create_scheduler() -> BackgroundScheduler:
    """创建定时调度器"""
    scheduler = BackgroundScheduler()

    # 北京时间早上 7 点 = 前一日美股收盘后
    scheduler.add_job(
        run_full_pipeline,
        trigger=CronTrigger(hour=MORNING_RUN_HOUR, minute=0),
        id="morning_run",
        name="早间采集+分析",
        replace_existing=True,
    )

    # 北京时间晚上 6 点 = 美股盘前
    scheduler.add_job(
        run_full_pipeline,
        trigger=CronTrigger(hour=EVENING_RUN_HOUR, minute=0),
        id="evening_run",
        name="晚间采集+分析",
        replace_existing=True,
    )

    print(f"[Scheduler] 定时任务已配置:")
    print(f"  早间 (北京时间 {MORNING_RUN_HOUR}:00) — 采集 + AI 分析")
    print(f"  晚间 (北京时间 {EVENING_RUN_HOUR}:00) — 采集 + AI 分析")
    return scheduler


def start_scheduler():
    """启动定时调度器"""
    scheduler = create_scheduler()
    scheduler.start()
    print(f"[Scheduler] 调度器已启动. {datetime.now().isoformat()}")

    try:
        # 保持主线程运行
        import time
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        print("\n[Scheduler] 收到退出信号，关闭...")
        scheduler.shutdown()
        print("[Scheduler] 已安全关闭")
