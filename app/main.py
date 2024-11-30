from fastapi import FastAPI
from app.routes.scrape import router as scrape_router
from mangum import Mangum

app = FastAPI(title="Season Match Data Scraper")
app.include_router(scrape_router)
handler = Mangum(app)