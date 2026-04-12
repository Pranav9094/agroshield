from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
from detect import detect_weeds

app = FastAPI(title="AgroShield API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)
INPUT_PATH = TEMP_DIR / "input.jpg"

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "model": "YOLOv8n"}

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid image format")

    try:
        with INPUT_PATH.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = detect_weeds(str(INPUT_PATH))
        return result

    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=f"Model file missing: {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

    finally:
        if INPUT_PATH.exists():
            INPUT_PATH.unlink()
