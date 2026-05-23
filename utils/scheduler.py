from apscheduler.schedulers.background import BackgroundScheduler
from services.news_service import fetch_all_news, COUNTRY_MAP

scheduler = BackgroundScheduler()

def fetch_all_countries():
    
    for country_name in COUNTRY_MAP.keys():
        try:
            fetch_all_news(country_name)
            print(f"Fetched: {country_name}")
        except Exception as e:
            print(f"Failed {country_name}: {e}")

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(fetch_all_countries,'interval',minutes=30,id='news_fetch_job')
        scheduler.start()
        print("Scheduler started")
        