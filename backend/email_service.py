import smtplib
import html as html_lib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def send_job_alerts(self, jobs):
        if not jobs:
            return

        if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
            logger.warning("SMTP credentials not configured. Skipping email.")
            return

        recipient = settings.ALERT_EMAIL_RECIPIENT or settings.SMTP_USER
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"LinkedIn Job Alert: {len(jobs)} New Matches"
        msg["From"] = settings.SMTP_USER
        msg["To"] = recipient

        # Build HTML content with escaping for safety

        html = "<h2>New LinkedIn Job Matches</h2><ul>"
        for job in jobs:
            safe_title = html_lib.escape(job.title)
            safe_company = html_lib.escape(job.company)
            safe_location = html_lib.escape(job.location)
            # Link is cleaned in scraper but we escape for the template
            safe_link = html_lib.escape(job.link)
            
            html += f"""
            <li>
                <strong>{safe_title}</strong> at {safe_company}<br>
                {safe_location}<br>
                <a href="{safe_link}">View Job</a>
            </li><br>
            """
        html += "</ul>"

        msg.attach(MIMEText(html, "html"))

        try:
            with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            logger.info(f"Alert email sent to {recipient}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
