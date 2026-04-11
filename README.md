<<<<<<< HEAD
# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
=======
# AgroShield

**AI-Powered Weed Detection for Precision Agriculture**

![AgroShield Theme](https://via.placeholder.com/1000x200/2D6A4F/FFFFFF?text=AgroShield)

AgroShield detects weeds using AI, shows where they are, and tells you exactly where to spray.

## 🛠️ Tech Stack
*   **Frontend**: React + Vite + Canvas API ⚛️
*   **Backend**: FastAPI + Python ⚡
*   **AI Model**: YOLOv8n (Ultralytics) 🤖

## ✨ Features (Sprint Goals)
*   **Level 1 (MVP)**: Image upload, YOLO weed detection, Bounding boxes on Canvas, Weed counting.
*   **Level 2 (Demo)**: Spray coordinate marks, Dashboard analytics, High-risk zones calculated.
*   **Level 3 (Wow)**: 3x3 Heatmap Grid, Auto-spray visual zones.

## 🚀 Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/Pranav9094/agroshield.git
cd agroshield
```

### 2. Setup AI Model (M1)
```bash
cd agroshield-model
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install ultralytics opencv-python pillow roboflow
```

### 3. Setup Backend (M3)
```bash
cd agroshield-backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
> API runs at: http://localhost:8000 | Docs: http://localhost:8000/docs

### 4. Setup Frontend (M2)
```bash
cd agroshield-frontend
npm install
npm run dev
```
> Frontend runs at: http://localhost:5173

---

## 📡 API Documentation
### `POST /detect`
**Request:** `multipart/form-data` with field `file` (Image)
**Response:**
```json
{
  "weed_count": 7,
  "crop_count": 12,
  "detections": [{"label": "weed", "confidence": 0.91, "bbox": [120, 300, 85, 60], "center": [162, 330]}],
  "spray_points": [[162, 330]],
  "density_map": {"zone_1": 0.85},
  "area_affected_pct": 38.5,
  "high_risk_zones": 2,
  "annotated_image": "base64_string"
}
```

## 👥 Team Members
| Name | Role | Contribution |
| :--- | :--- | :--- |
| **Member 1** | AI Model Engineer | YOLO training, `detect.py`, dataset prep |
| **Member 2** | Frontend Engineer | React upload, Canvas rendering, Dashboard |
| **Member 3** | Backend Engineer | FastAPI, Spray zone logic, API routing |
| **Member 4** | PPT & Docs | Architecture diagram, README, Design |
| **Member 5** | Team Lead | Integration tests, GitHub merging, Demos |

## 🔮 Future Scope
1.  **Mobile App:** Subscription for individual farmers.
2.  **Drone Integration:** Real-time scanning.
3.  **Smart Sprayer:** Autonomous hardware integration.

## 📄 License
MIT License
>>>>>>> f7c4e61e5c32fcc77e818ca709a199b3e7353451
