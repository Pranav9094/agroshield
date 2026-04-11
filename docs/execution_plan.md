# AgroShield Exhaustive Execution Master Plan

This plan contains **every single task** required for the project, broken down into granular checklists for M1 to M5, including the final cloud deployment. 

## ✅ 1. Completed Scaffold (Foundation)
*   **M5 (Lead):** GitHub Repo created, 5 branches created (`main`, `dev`, `feature/*`), `.gitignore` configured.
*   **M5 (Lead):** Written `integration_test.py` (5-stage tester).
*   **M2 (FE):** React + Vite project initialized (`agroshield-frontend`), basic dependencies installed.
*   **M3 (BE):** FastAPI initialized (`agroshield-backend/main.py`), basic `/health` endpoint, CORS configured, `requirements.txt` generated.
*   **M1 (AI):** YOLOv8 / Ultralytics dependencies added to `requirements.txt`.
*   **M4 (Docs):** Base `README.md` generated with tech stack and setup cmds.

---

## ⏳ 2. Pending Development Work (By Role)

### 🤖 M1: AI Model Engineer (Feature: `feature/ai-model`)
- [ ] **1. Download Dataset:** Write `download_dataset.py` using `roboflow` to fetch the 'WeedCrop' dataset in YOLOv8 format into `./datasets/weedcrop/`.
- [ ] **2. Model Training:** Write `train.py` using `ultralytics`. Specs: YOLOv8n, 80 epochs, size 640, batch 16. Output: `./models/best.pt`.
- [ ] **3. Inference Script:** Write `inference.py` (`detect_weeds()`) function that:
    - [ ] Loads `best.pt`.
    - [ ] Draws Red boxes for "weed", Green boxes for "crop".
    - [ ] Returns exact JSON structure (weed count, detections, spray points).
- [ ] **4. Evaluation Report:** Write `evaluate.py`. Output accuracy report (mAP50, precision, recall) + confusion matrix image for the PPT.
- [ ] **5. WOW Factor (Opt):** Write `live_detection.py` using OpenCV to run real-time webcam inference.

### 💻 M2: Frontend Engineer (Feature: `feature/frontend`)
- [ ] **1. Upload UI:** Build `ImageUpload.jsx`.
    - [ ] Drag & Drop upload zone.
    - [ ] 'Detect Weeds' button & Loading spinner state.
- [ ] **2. Result Bounding Box UI:** Build `ResultCanvas.jsx`.
    - [ ] Draw base image on Canvas format.
    - [ ] Overlay red/green boxes from API JSON payload.
    - [ ] Overlay confidence text (e.g. `Weed 91%`).
- [ ] **3. Dashboard UI:** Build `Dashboard.jsx`.
    - [ ] 2x2 grid visualizing: Weed Count, Crop Count, Area Affected %, High-Risk Zones.
    - [ ] Spray Recommendation coordinates table. 
- [ ] **4. App Wiring:** Wire `App.jsx` to manage state, send `multipart/form-data` via Axios, display Canvas.
- [ ] **5. WOW Factor:** Draw red circle dot markers for `spray_points` on Canvas. Add CSS grid for the 3x3 Heatmap overlay over the image showing density.

### ⚙️ M3: Backend Engineer (Feature: `feature/backend`)
- [ ] **1. Bridge Logic:** Write `detect.py` that hooks FastAPI to M1's `best.pt` file.
    - [ ] Create `compute_spray_zones(detections)` to calculate target centroids.
- [ ] **2. Density Mapping Math:** Add logic computing the 3x3 Grid `density_map` scoring weeds per zone (0.0 to 1.0) and identifying `high_risk_zones` (>0.5).
- [ ] **3. Finalize API Endpoint:** Update `main.py` -> `POST /detect`. 
    - [ ] Handle image stream in memory. 
    - [ ] Return Base64 encoded annotated image inside the JSON payload.
- [ ] **4. Test Scripts:** Write `test_api.py` specific to M3 folder and `run.sh` initialization file.

### 📝 M4: Docs & PPT (Feature: `feature/ppt-docs`)
- [ ] **1. Presentation Flow:** Build 8-slide PPT (Title, Problem, Arch, AI, Demo, Impact, Future).
- [ ] **2. Data Viz:** Create Architecture diagram detailing data flow.
- [ ] **3. QA & Scripts:** Write specific speaking scripts (who says what line). Generate "Judge Q&A" FAQ cheat sheet.
- [ ] **4. Release Tagging:** Take HD app Screenshots required for README. Finalize `README.md` polishing.

---

## ☁️ 3. Pending Deployment & Demo Prep (Lead - M5)

### Cloud Setup 
- [ ] **Vercel / Netlify (Frontend):** Link M2's React code block. Configure `npm run build` and `dist` distruibution. Provide public URL.
- [ ] **Render / AWS (Backend/AI):** Link M3 FastAPI. Deploy with Docker or configured VM ensuring `torch` and `best.pt` file are uploaded. Bind to `0.0.0.0:8000`. Wait for URL.
- [ ] **Environment Mapping:** Update Frontend `.env` API URL to point towards the cloud server instead of `localhost:8000`.

### QA & Demo Verification
- [ ] **E2E Cloud Check:** Point `integration_test.py` strictly at the LIVE deployment links to verify success.
- [ ] **Safe Inputs:** Collect and isolate 3 explicitly validated "Safe Images" for the live demo.
- [ ] **Backup Resilience:** Record a 2-minute 1080p screen-recording of the full pipeline functioning flawlessly as a failsafe presentation.
