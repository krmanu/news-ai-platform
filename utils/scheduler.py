from apscheduler.schedulers.background import BackgroundScheduler
from services.news_service import fetch_all_news

scheduler = BackgroundScheduler()

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            fetch_all_news,
            'interval',
            minutes=30,
            id='news_fetch_job'
        )
        scheduler.start()
        print("Scheduler started — fetching news every 30 mins")