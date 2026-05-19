from apscheduler.schedulers.asyncio import AsyncIOScheduler
from scraper import LinkedInScraper
from email_service import EmailService
from database import SessionLocal
from models import Alert, Job
from config import settings
import logging

logger = logging.getLogger(__name__)

async def run_scrapers():
    logger.info("Starting scheduled scraping run...")
    db = SessionLocal()
    scraper = LinkedInScraper()
    email_service = EmailService()
    
    try:
        active_alerts = db.query(Alert).filter(Alert.is_active == True).all()
        new_jobs_to_alert = []

        for alert in active_alerts:
            found_jobs = await scraper.scrape_jobs(alert.keyword, alert.location)
            
            for job_data in found_jobs:
                # Check if job already exists
                existing_job = db.query(Job).filter(Job.linkedin_id == job_data["linkedin_id"]).first()
                if not existing_job:
                    new_job = Job(
                        linkedin_id=job_data["linkedin_id"],
                        title=job_data["title"],
                        company=job_data["company"],
                        location=job_data["location"],
                        link=job_data["link"],
                        alert_id=alert.id
                    )
                    db.add(new_job)
                    new_jobs_to_alert.append(new_job)
        
        db.commit()
        
        if new_jobs_to_alert:
            logger.info(f"Found {len(new_jobs_to_alert)} new jobs. Sending alert.")
            email_service.send_job_alerts(new_jobs_to_alert)
            # Mark as emailed
            for job in new_jobs_to_alert:
                job.emailed = True
            db.commit()
        else:
            logger.info("No new jobs found this run.")

    except Exception as e:
        logger.error(f"Error in scheduled run: {e}")
    finally:
        db.close()

scheduler = AsyncIOScheduler()

def start_scheduler():
    scheduler.add_job(run_scrapers, "interval", hours=settings.SCRAPE_INTERVAL_HOURS)
    scheduler.start()
    logger.info(f"Scheduler started. Will run every {settings.SCRAPE_INTERVAL_HOURS} hours.")
