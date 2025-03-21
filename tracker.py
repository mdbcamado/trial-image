from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
import logging
import datetime
import os

app = FastAPI()

# Enable logging to track impressions
logging.basicConfig(filename="impressions.log", level=logging.INFO, format="%(asctime)s - %(message)s")

IMAGE_PATH = "static/Applynow.png"  # Adjusted path

@app.get("/track-apply.png")
async def track_apply(request: Request):
    """Serve the Apply Now button image and log impressions."""
    ip = request.client.host  # Get visitor's IP
    timestamp = datetime.datetime.now().isoformat()  # Timestamp

    # Log impression details
    logging.info(f"Impression: {timestamp}, IP: {ip}")

    # Ensure file exists before serving
    if not os.path.exists(IMAGE_PATH):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(IMAGE_PATH)
