from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import logging
import datetime

app = FastAPI()

# Enable logging to track impressions
logging.basicConfig(filename="impressions.log", level=logging.INFO)

@app.get("/track-apply.png")
async def track_apply(request: Request):
    """Serve the Apply Now button image and log impressions."""
    ip = request.client.host  # Get visitor's IP
    timestamp = datetime.datetime.now().isoformat()  # Timestamp

    # Log impression details
    logging.info(f"Impression: {timestamp}, IP: {ip}")

    # Serve the image
    return FileResponse("Applynow.png")

