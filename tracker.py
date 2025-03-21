from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
import logging
import datetime
import os
import requests
import gspread
from google.oauth2.service_account import Credentials

app = FastAPI()

# Set up logging directory
LOG_DIR = "/opt/render/logs"
LOG_FILE = os.path.join(LOG_DIR, "impressions.log")
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - IP: %(message)s")

# Load Google Sheets credentials from environment variables
SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_CREDENTIALS")
if not SERVICE_ACCOUNT_JSON:
    raise ValueError("GOOGLE_CREDENTIALS is not set in the environment.")

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds = Credentials.from_service_account_info(eval(SERVICE_ACCOUNT_JSON), scopes=SCOPES)
gc = gspread.authorize(creds)

# Set your Google Sheet name and worksheet
SHEET_NAME = "Craiglist Posting"
WORKSHEET_NAME = "Log"

# Open the Google Sheet
try:
    sheet = gc.open(SHEET_NAME)
    worksheet = sheet.worksheet(WORKSHEET_NAME)
except gspread.exceptions.SpreadsheetNotFound:
    raise ValueError(f"Spreadsheet '{SHEET_NAME}' not found.")
except gspread.exceptions.WorksheetNotFound:
    raise ValueError(f"Worksheet '{WORKSHEET_NAME}' not found.")

app = FastAPI()

# Set up logging directory
LOG_DIR = "/opt/render/logs"
LOG_FILE = os.path.join(LOG_DIR, "impressions.log")
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - IP: %(message)s")

# Load Google Sheets credentials from environment variables
SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_CREDENTIALS")
if not SERVICE_ACCOUNT_JSON:
    raise ValueError("GOOGLE_CREDENTIALS is not set in the environment.")


# Function to get geolocation from IP
def get_geolocation(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data["status"] == "fail":
            return "Unknown"
        return f"{data['city']}, {data['regionName']}, {data['country']}"
    except:
        return "Unknown"

# Serve the tracked images
@app.get("/track/{image_name}")
async def track_image(request: Request, image_name: str):
    """Serve tracked images and log impressions to Google Sheets."""
    ip = request.client.host
    timestamp = datetime.datetime.utcnow().isoformat()
    geolocation = get_geolocation(ip)

    # Log impression details locally
    log_entry = f"{timestamp}, {ip}, {geolocation}, {image_name}"
    logging.info(log_entry)

    # Append log entry to Google Sheet
    worksheet.append_row([timestamp, ip, geolocation, image_name])

    # Check if the image exists
    image_path = f"static/{image_name}"
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(image_path)
