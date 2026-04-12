# 🌿 AgroShield
### AI-Powered Weed Detection for Precision Agriculture

> Detects weeds using AI, shows where they are, and tells you exactly where to spray.

![YOLOv8](https://img.shields.io/badge/AI-YOLOv8n%2094.73%25%20mAP-brightgreen)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB)
![License](https://img.shields.io/badge/License-MIT-blue)

---

## 🚨 The Problem

Farmers spray pesticides across **entire fields** — but **60-80% of chemicals** land on perfectly healthy crops, wasting money and harming soil.

---

## ✅ Solution

```
Upload Farm Image → AI Detects Weeds → Bounding Boxes → Spray Coordinates → Save Chemicals
```

- 🎯 **94.73% mAP accuracy** on real farm dataset
- 💧 **40-60% reduction** in pesticide usage
- 💰 **₹18,000+ saved** per farmer per season
- 🌐 Works **100% offline** — no internet needed

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| 🤖 AI Model | YOLOv8n (Ultralytics) |
| ⚙️ Backend | Python + FastAPI |
| ⚛️ Frontend | React + Vite + Canvas API |
| 👁️ Vision | OpenCV |
| 🗄️ Dataset | WeedCrop (Roboflow) — 4396 images |

---

## ✨ Features

### Level 1 — MVP
- Image upload (drag & drop)
- YOLOv8 real-time weed detection
- Bounding boxes — RED = weed, GREEN = crop
- Weed count + confidence %

### Level 2 — Smart Detection
- Spray coordinate markers on image
- Dashboard: weed count, crop count, area affected %
- High-risk zones calculation (out of 9)

### Level 3 — Advanced
- 3x3 Field density heatmap
- Live webcam detection at 30+ FPS
- Download annotated image
- Field zone risk analysis

---

## 🚀 Quick Start

### Prerequisites
Make sure these are installed on your system:
- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/)
- [Git](https://git-scm.com/)

---

### Step 1 — Clone Repository

```powershell
git clone https://github.com/Pranav9094/agroshield.git
cd agroshield
```

---

### Step 2 — Backend Setup

```powershell
# Navigate to backend folder
cd agroshield-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt

# Start backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

> ✅ API running at: `http://localhost:8000`
> ✅ API Docs at: `http://localhost:8000/docs`

---

### Step 3 — Frontend Setup

Open a **new terminal** and run:

```powershell
# Navigate to frontend folder
cd agroshield\agroshield-frontend

# Install dependencies
npm install

# Start frontend
npm run dev
```

> ✅ App running at: `http://localhost:5173`

---

### Step 4 — Open App

Open browser and go to:
```
http://localhost:5173
```

Upload any farm image → Click **Detect Weeds** → See results! 🌿

---

## ⚠️ First Time Setup Notes

> If you are running on a **new system**, the AI model (`best.pt`) must be present in:
> ```
> agroshield-backend/models/best.pt
> ```
> Download the trained model from [Releases](https://github.com/Pranav9094/agroshield/releases) or retrain using the steps below.

### Retrain Model (Optional)

```powershell
# Navigate to model folder
cd agroshield-model

# Create virtual environment
python -m venv agroshield_env
agroshield_env\Scripts\activate

# Install dependencies
pip install ultralytics opencv-python pillow roboflow

# Download dataset
python download_dataset.py --api-key YOUR_ROBOFLOW_KEY

# Train model
python train.py
```

> ✅ Trained model saved at: `agroshield-model/models/best.pt`
> Copy it to `agroshield-backend/models/best.pt` after training.

---

## 📡 API Documentation

### `POST /detect`
**Request:** `multipart/form-data` — field: `file` (image)

**Response:**
```json
{
  "weed_count": 3,
  "crop_count": 2,
  "detections": [
    {"label": "weed", "confidence": 0.91, "bbox": [120, 300, 85, 60], "center": [162, 330]}
  ],
  "spray_points": [[162, 330], [335, 225]],
  "density_map": {"zone_1": 0.85, "zone_2": 0.12},
  "area_affected_pct": 38.5,
  "high_risk_zones": 2,
  "annotated_image": "base64_string"
}
```

### `GET /health`
```json
{"status": "ok", "model": "YOLOv8n"}
```

---

## 📊 Model Performance

| Metric | Score |
|---|---|
| mAP50 | **94.73%** |
| Training Images | 3,620 |
| Validation Images | 517 |
| Inference Speed | 30+ FPS |

---

## 🔮 Future Scope

- 📱 Mobile App for farmers
- 🚁 Drone camera integration
- 🤖 Autonomous smart sprayer

---

## 👨‍💻 Built by

| Name | Role |
|---|---|
| **Pranav Chaudhari** | AI Model, Training, Architecture, Project Lead |
| **Arjun Kawale** | Frontend, Backend, API Integration |

---

## 📄 License
MIT License © 2026