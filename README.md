# LinkedIn Job Alerts

A free, local tool to monitor LinkedIn job postings and receive email alerts.

## Project Structure
- `backend/`: FastAPI server with Playwright scraper and SQLite database.
- `frontend/`: React + TypeScript + Tailwind CSS dashboard.

## Setup Instructions

### 1. Backend Setup
1. Navigate to `backend/`.
2. Activate the virtual environment: `source venv/bin/activate`.
3. Update the `.env` file with your email credentials:
   - `SMTP_USER`: Your Gmail address.
   - `SMTP_PASSWORD`: Your Gmail App Password (NOT your regular password).
   - `ALERT_EMAIL_RECIPIENT`: Where you want to receive alerts.
4. Run the server: `uvicorn main:app --reload`.

### 2. Frontend Setup
1. Navigate to `frontend/`.
2. Install dependencies: `npm install`.
3. Run the development server: `npm run dev`.
4. Open `http://localhost:5173` in your browser.

## Features
- **Local Scraping:** Uses Playwright to scrape public LinkedIn data without an account or paid API.
- **Anti-Detection:** Implements stealth techniques to avoid being blocked.
- **Email Alerts:** Automatically sends an email when new jobs are found matching your alerts.
- **Dashboard:** Manage your job keywords and locations easily.

## Notes
- The scraper runs every 6 hours by default (configurable in `.env`).
- You can manually trigger a refresh from the dashboard.
- This tool is subject to LinkedIn's website layout; if they change their site, the scraper may need updates.
