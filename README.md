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

### 1. Clone
```bash
git clone https://github.com/Pranav9094/agroshield.git
cd agroshield
```

### 2. Backend
```bash
cd agroshield-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
> API: `http://localhost:8000` | Docs: `http://localhost:8000/docs`

### 3. Frontend
```bash
cd agroshield-frontend
npm install
npm run dev
```
> App: `http://localhost:5173`

---

## 📡 API

### `POST /detect`
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

| | |
|---|---|
| **Pranav Chaudhari** | AI Model, Training, Architecture, Project Lead |
| **Arjun Kawale** | Frontend, Backend, API Integration |

---

## 📄 License
MIT License © 2026