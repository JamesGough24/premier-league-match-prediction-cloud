# from typing import List
from fastapi import FastAPI
from src.routes.scrape import router as scrape_router

app = FastAPI(title="Season Match Data Scraper")

app.include_router(scrape_router)