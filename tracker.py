from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
import logging
import datetime
import os

app = FastAPI()

# Set log directory (match this to your Render disk mount path)
LOG_DIR = "/var/logs"  # Adjust this based on your Render disk path
LOG_FILE = os.path.join(LOG_DIR, "impressions.log")

# Ensure the directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - IP: %(message)s")

IMAGE_PATH = "static/Applynow.png"  # Adjusted path

@app.get("/track-apply.png")
async def track_apply(request: Request):
    """Serve the Apply Now button image and log impressions."""
    ip = request.client.host  # Get visitor's IP
    timestamp = datetime.datetime.now().isoformat()  # Timestamp

    # Log impression details
    logging.info(f"{timestamp}, {ip}")

    # Ensure file exists before serving
    if not os.path.exists(IMAGE_PATH):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(IMAGE_PATH)
