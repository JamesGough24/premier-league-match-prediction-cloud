from fastapi import FastAPI, Query
import boto3
import json
from app.utils.scraper import scrape_matches
from app.utils.file_operations import save_data_to_csv
from mangum import Mangum

app = FastAPI(title="Season Match Data Scraper")

# S3 client
s3_client = boto3.client('s3')

@app.get("/scrape/")
async def scrape(league: str = Query("premier-league"), season: str = Query("2024-2025"), gameweek: str = Query(...)):
    season = season.replace("-", "/")
    
    # Scrape matches
    try:
        data = scrape_matches(league, season, gameweek)
    except Exception as e:
        return {
            "status-code": 500,
            "body": json.dumps({"error": str(e)})
        }
    
    try:
        match_data = save_data_to_csv(data, filename=f"{league}_gw_{gameweek}_{season}_match_data.csv")
    except Exception as e:
        return {
            "status-code": 500,
            "body": json.dumps({"error": str(e)})
        }

    print("Finished saving data to CSV")

    bucket_name = "match-prediction-data"
    object_name = f"{league}_gw_{gameweek}_{season}_match_data.csv"

    try:
        s3_client.put_object(Body=match_data, Bucket=bucket_name, Key=object_name)
        return {
            "status-code": 200,
            "body": json.dumps({"message": f"Saved successfully to https://{bucket_name}.s3.amazonaws.com/{object_name}"})
        }
    
    except Exception as e:
        return {
            "status-code": 500,
            "body": json.dumps({"error": str(e)})
        }

handler = Mangum(app)

def lambda_handler(event, context):
    return handler(event, context)