# AgroShield 🌾

```
   _____                  _____ _     _      _     _
  / ____|                / ____| |   (_)    | |   | |
 | |     __ _ _ __ ___  | (___ | |__  _  ___| | __| |
 | |    / _` | '__/ _ \  \___ \| '_ \| |/ _ \ |/ _` |
 | |___| (_| | | | (_) | ____) | | | | |  __/ | (_| |
  \_____\__,_|_|  \___/ |_____/|_| |_|_|\___|_|\__,_|

         AI-Powered Precision Weed Detection System
```

> **Upload a farm image → AI detects weeds → Get exact spray coordinates. Stop wasting chemicals.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-61DAFB?logo=react&logoColor=black)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-FF6F00)](https://ultralytics.com)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Team](https://img.shields.io/badge/Team-THE%20ELITES-gold)](https://github.com/Pranav9094/agroshield)

---

## 🚩 The Problem

Indian farmers spray pesticides across **entire fields** — 60–80% of chemicals land on healthy crops and soil, not weeds. This causes **Rs 7,000 crore in annual losses** nationwide and contributes to serious environmental damage. Manual scouting is slow, inconsistent, and unscalable.

**AgroShield fixes this with AI.**

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| 🐍 **AI Model** | YOLOv8n (Ultralytics) | Real-time weed object detection |
| ⚡ **Backend** | FastAPI (Python) | High-performance REST API server |
| ⚛️ **Frontend** | React + Vite | Fast, responsive user interface |
| 🗄️ **Dataset** | WeedCrop Dataset (Roboflow) | Annotated farm weed images |
| 📦 **Runtime** | Python 3.10+, Node 18+ | Core runtimes |

---

## ✨ Features

### 🟢 Level 1 — MVP (Working Now)
- Upload farm image via browser
- YOLOv8 detects weed locations with bounding boxes
- Returns weed count, confidence scores, and spray coordinates
- Clean React UI with detection overlay

### 🔵 Level 2 — Strong
- Dashboard with detection history and stats
- Per-field pesticide reduction estimates
- Downloadable spray coordinate reports (CSV/JSON)
- Multi-image batch processing

### 🟣 Level 3 — WOW (Roadmap)
- Mobile app with real-time camera detection
- Drone integration for aerial weed mapping
- Smart autonomous sprayer command output
- Offline model inference on edge devices

---

## 📁 Repository Structure

```
agroshield/
├── agroshield-frontend/      # React + Vite app
├── agroshield-backend/       # FastAPI server
├── agroshield-model/         # YOLOv8 model + training
├── docs/                     # PPT, README, speaking script
└── README.md
```

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- Git

---

### 1. Clone the Repository

```bash
git clone https://github.com/Pranav9094/agroshield.git
cd agroshield
```

---

### 2. Setup AI Model (`agroshield-model/`)

```bash
cd agroshield-model

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate       # Linux/Mac
# venv\Scripts\activate        # Windows

# Install dependencies
pip install ultralytics opencv-python

# Download pre-trained weights (or use best.pt from model/weights/)
# Place your trained best.pt in: agroshield-model/weights/best.pt

# Verify model loads correctly
python -c "from ultralytics import YOLO; m = YOLO('weights/best.pt'); print('Model OK')"
```

---

### 3. Setup Backend (`agroshield-backend/`)

```bash
cd ../agroshield-backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate       # Linux/Mac
# venv\Scripts\activate        # Windows

# Install dependencies
pip install -r requirements.txt
# Key packages: fastapi, uvicorn, ultralytics, pillow, python-multipart

# Configure model path in config.py (if needed)
# MODEL_PATH = "../agroshield-model/weights/best.pt"

# Start the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be live at: `http://localhost:8000`
API docs (Swagger UI): `http://localhost:8000/docs`

---

### 4. Setup Frontend (`agroshield-frontend/`)

```bash
cd ../agroshield-frontend

# Install Node dependencies
npm install

# Start the development server
npm run dev
```

Frontend will be live at: `http://localhost:5173`

---

### 5. Run All 3 Together

Open **three separate terminal windows**:

```bash
# Terminal 1 — Backend
cd agroshield-backend && source venv/bin/activate && uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd agroshield-frontend && npm run dev

# Terminal 3 — (Optional) Model training / testing
cd agroshield-model && source venv/bin/activate && python test_model.py
```

Then open `http://localhost:5173` in your browser. Upload a farm image and watch AgroShield detect weeds in real time.

---

## 📡 API Documentation

### `POST /detect`

Detects weeds in an uploaded farm image.

**Request:**
```
Content-Type: multipart/form-data
```

| Field | Type | Required | Description |
|---|---|---|---|
| `file` | Image file | ✅ Yes | Farm photo (.jpg, .png, .webp) |
| `confidence` | float | ❌ Optional | Confidence threshold (default: 0.5) |

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/detect" \
  -F "file=@farm_field.jpg" \
  -F "confidence=0.5"
```

**Response (200 OK):**
```json
{
  "status": "success",
  "weed_count": 4,
  "processing_time_ms": 312,
  "image_dimensions": {
    "width": 1280,
    "height": 720
  },
  "detections": [
    {
      "weed_id": 1,
      "class": "broadleaf_weed",
      "confidence": 0.87,
      "bounding_box": {
        "x_min": 142,
        "y_min": 230,
        "x_max": 310,
        "y_max": 415
      },
      "spray_coordinate": {
        "center_x": 226,
        "center_y": 322
      },
      "area_px": 30940
    },
    {
      "weed_id": 2,
      "class": "grass_weed",
      "confidence": 0.74,
      "bounding_box": {
        "x_min": 540,
        "y_min": 390,
        "x_max": 670,
        "y_max": 510
      },
      "spray_coordinate": {
        "center_x": 605,
        "center_y": 450
      },
      "area_px": 16900
    }
  ],
  "pesticide_savings_estimate": "~73% reduction vs blanket spray",
  "annotated_image_base64": "<base64-encoded-png-with-bounding-boxes>"
}
```

**Error Response (400):**
```json
{
  "status": "error",
  "message": "Invalid file type. Please upload a JPG, PNG, or WEBP image.",
  "weed_count": 0,
  "detections": []
}
```

---

## 👥 Team — THE ELITES

| Name | Role | GitHub Branch | Key Contribution |
|---|---|---|---|
| **Pranav** | Team Lead / Backend | `feature/backend-api` | FastAPI server, YOLOv8 integration, system architecture |
| **Shrutika** | AI / ML Engineer | `feature/ai-model` | YOLOv8 training, WeedCrop dataset, model evaluation |
| **Arjun** | Frontend Developer | `feature/frontend-ui` | React UI, image upload, bounding box overlay |
| **Krishna** | Backend Developer | `feature/backend-db` | API endpoints, data pipeline, deployment |
| **Kangna Thakur** | PPT + Documentation | `feature/ppt-docs` | README, presentation, speaking script |

**Institution:** Parul University 


---

## 📸 Screenshots

> _Screenshots will be added after live demo capture (Day 4 – 10 Apr)._

| Screen | Description |
|---|---|
| 📤 Upload Screen | Drag & drop farm image interface |
| 🔍 Detection Result | Bounding boxes on detected weeds |
| 📊 Dashboard | Weed count, savings estimate, spray map |

---

## 📈 Impact

| Metric | Value |
|---|---|
| Pesticide reduction | **40–60%** per field |
| Cost savings | **Rs 18,000 per farmer / year** |
| Detection speed | **< 500ms** per image |
| Coverage | Works on any farm photo |
| Target users | 120M+ Indian farmers |

---

## 🔭 Future Scope

### Phase 1 — 📱 Mobile App (3 months)
- React Native app with on-device YOLOv8 inference
- Real-time camera detection in the field
- GPS-tagged weed reports

### Phase 2 — 🚁 Drone Integration (6 months)
- Aerial field mapping with drone cameras
- Large-scale weed heatmap generation
- Integration with drone flight controllers (DJI SDK)

### Phase 3 — 🤖 Smart Autonomous Sprayer (12 months)
- AI-commanded precision sprayer robots
- Fully automated detect → target → spray pipeline
- Compatible with existing tractor-mounted equipment

---

## 📄 License

```
MIT License

Copyright (c) 2025 THE ELITES — Parul University

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
provided to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

<div align="center">

**Built with 💚 by THE ELITES | Parul University × MIT-ADT**

[🔗 GitHub](https://github.com/Pranav9094/agroshield) • [📊 Live Demo](#) • [📄 Docs](docs/)

</div>
