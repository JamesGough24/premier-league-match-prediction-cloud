from fastapi import APIRouter
from app.utils.scraper import scrape_matches
from app.utils.file_operations import save_data_to_csv

router = APIRouter()

@router.get("/scrape/")
async def scrape(league: str, season: str, gameweek: int):
    data = scrape_matches(league, season, gameweek)

    save_data_to_csv(data, filename=f"{league}_gw_{gameweek}_{season}_match_data.csv")
    return {"status": "Data scraped and saved successfully", "file": f"{league}_gw_{gameweek}_{season}_match_data.csv"}