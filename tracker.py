from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
import logging
import datetime
import os

app = FastAPI()

# Use the correct Render-mounted log directory
LOG_DIR = "/opt/render/logs"
LOG_FILE = os.path.join(LOG_DIR, "impressions.log")

# Ensure the log directory exists (Render should already have this)
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logger = logging.getLogger("impressions_tracker")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(LOG_FILE)
handler.setFormatter(logging.Formatter("%(asctime)s - IP: %(message)s"))
logger.addHandler(handler)

# Define the image path
IMAGE_PATH = "static/Applynow.png"

@app.get("/track-apply.png")
async def track_apply(request: Request):
    """Serve the Apply Now button image and log impressions."""
    ip = request.client.host  # Get visitor's IP address
    timestamp = datetime.datetime.now().isoformat()  # Current timestamp

    # Log impression details
    logger.info(f"{timestamp}, {ip}")

    # Check if the image exists before serving
    if not os.path.exists(IMAGE_PATH):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(IMAGE_PATH)
