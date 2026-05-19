import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./jobs.db"
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    ALERT_EMAIL_RECIPIENT: str = ""
    SCRAPE_INTERVAL_HOURS: int = 6
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
