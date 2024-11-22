from fastapi import APIRouter
from src.utils.scraper import scrape_matches

router = APIRouter()

@router.get("/scrape-matches")
def get_matches(league: str, season: str, gameweek: int):
    data = scrape_matches(league, season, gameweek)
    return {"matches": data}