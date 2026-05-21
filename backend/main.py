from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models, schemas, database, scheduler
from database import engine, get_db
from scheduler import run_scrapers

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LinkedIn Job Alerts API")

# CORS - Restrict to local frontend for security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    scheduler.start_scheduler()

@app.get("/alerts", response_model=List[schemas.Alert])
def get_alerts(db: Session = Depends(get_db)):
    return db.query(models.Alert).all()

@app.post("/alerts", response_model=schemas.Alert)
def create_alert(alert: schemas.AlertCreate, db: Session = Depends(get_db)):
    db_alert = models.Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

@app.delete("/alerts/{alert_id}")
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    db_alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    db.delete(db_alert)
    db.commit()
    return {"message": "Alert deleted"}

@app.get("/jobs", response_model=List[schemas.Job])
def get_jobs(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(models.Job).order_by(models.Job.discovered_at.desc()).offset(skip).limit(limit).all()

@app.post("/trigger-scrape")
async def trigger_scrape(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_scrapers)
    return {"message": "Scraping task triggered in background"}

@app.get("/")
def read_root():
    return {"status": "ok", "message": "LinkedIn Job Alerts API is running"}
