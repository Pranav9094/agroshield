from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="AgroShield API")

# Enable CORS for React frontend (localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure temp directory exists
os.makedirs("temp", exist_ok=True)

@app.get("/health")
def health_check():
    """Test 1 - Health Check"""
    return {"status": "ok", "model": "YOLOv8n"}

@app.post("/detect")
async def extract_weeds(file: UploadFile = File(...)):
    """
    POST endpoint for M3 to implement YOLO processing.
    Currently returns dummy data to pass Initial Scaffold checking.
    """
    file_location = f"temp/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    # TODO: M3 to replace with actual `detect_weeds()` call from `detect.py`
    return {
        "weed_count": 0,
        "crop_count": 0,
        "detections": [],
        "spray_points": [],
        "density_map": {"zone_1": 0.0},
        "area_affected_pct": 0.0,
        "high_risk_zones": 0,
        "annotated_image": ""
    }
