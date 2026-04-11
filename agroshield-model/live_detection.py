"""
AgroShield — Live Weed Detection
Real-time weed/crop detection using webcam feed.
Usage: python live_detection.py
Press 'Q' to quit | 'S' to save screenshot | 'P' to pause
"""

import sys
import time
from pathlib import Path
from datetime import datetime


# ── Colour constants ────────────────────────────────────────────────────────
WEED_COLOR = (51, 51, 255)    # #FF3333 in BGR
CROP_COLOR = (51, 204, 51)    # #33CC33 in BGR
BLACK      = (0, 0, 0)
WHITE      = (255, 255, 255)
YELLOW     = (0, 255, 255)


WEED_KEYWORDS = {"weed", "wild", "broadleaf", "narrowleaf", "morningglory"}
CROP_KEYWORDS = {"crop", "maize", "corn", "wheat", "soybean", "rice"}


def classify_label(name: str) -> str:
    name_lower = name.lower()
    for kw in WEED_KEYWORDS:
        if kw in name_lower:
            return "weed"
    for kw in CROP_KEYWORDS:
        if kw in name_lower:
            return "crop"
    return "weed"


def draw_overlay(frame, weed_count, crop_count, fps, paused=False):
    """Draw HUD overlay on frame."""
    import cv2
    h, w = frame.shape[:2]

    # Top bar background
    cv2.rectangle(frame, (0, 0), (w, 50), (20, 20, 20), -1)

    # Title
    cv2.putText(frame, "AgroShield Live Detection",
                (10, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.8, YELLOW, 2, cv2.LINE_AA)

    # FPS
    fps_text = f"FPS: {fps:.1f}"
    cv2.putText(frame, fps_text,
                (w - 120, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.7, WHITE, 2, cv2.LINE_AA)

    # Bottom bar background
    cv2.rectangle(frame, (0, h - 50), (w, h), (20, 20, 20), -1)

    # Weed count
    cv2.putText(frame, f"Weeds: {weed_count}",
                (10, h - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.75, WEED_COLOR, 2, cv2.LINE_AA)

    # Crop count
    cv2.putText(frame, f"Crops: {crop_count}",
                (160, h - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.75, CROP_COLOR, 2, cv2.LINE_AA)

    # Controls hint
    cv2.putText(frame, "Q: Quit | S: Screenshot | P: Pause",
                (w - 360, h - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1, cv2.LINE_AA)

    # Paused indicator
    if paused:
        cv2.rectangle(frame, (w//2 - 80, h//2 - 30), (w//2 + 80, h//2 + 30), BLACK, -1)
        cv2.putText(frame, "PAUSED", (w//2 - 55, h//2 + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, YELLOW, 2, cv2.LINE_AA)

    return frame


def live_detection():
    try:
        import cv2
        import torch
        from ultralytics import YOLO
    except ImportError as e:
        print(f"[ERROR] Missing package: {e}")
        sys.exit(1)

    # ── Config ─────────────────────────────────────────────────────────────
    MODEL_PATH     = "./models/best.pt"
    SCREENSHOT_DIR = "./outputs/live_screenshots"
    CAMERA_INDEX   = 0       # 0 = default webcam
    CONF_THRESH    = 0.30
    FRAME_SKIP     = 2       # Process every Nth frame (1 = every frame)
    DISPLAY_WIDTH  = 960
    DISPLAY_HEIGHT = 540

    # ── Validate model ──────────────────────────────────────────────────────
    if not Path(MODEL_PATH).exists():
        print(f"[ERROR] Model not found: {MODEL_PATH}")
        print("        Run train.py first!")
        sys.exit(1)

    Path(SCREENSHOT_DIR).mkdir(parents=True, exist_ok=True)

    print("=" * 55)
    print("  AgroShield — Live Weed Detection")
    print("=" * 55)
    print(f"  Model   : {MODEL_PATH}")
    print(f"  Camera  : index {CAMERA_INDEX}")
    print(f"  Conf    : {CONF_THRESH}")
    if torch.cuda.is_available():
        print(f"  Device  : GPU — {torch.cuda.get_device_name(0)}")
        device = 0
    else:
        print(f"  Device  : CPU")
        device = "cpu"
    print("=" * 55)
    print("\nControls:")
    print("  Q — Quit")
    print("  S — Save screenshot")
    print("  P — Pause/Resume")
    print("\nStarting...\n")

    # ── Load model ──────────────────────────────────────────────────────────
    model = YOLO(MODEL_PATH)
    class_names = model.names

    # ── Open webcam ─────────────────────────────────────────────────────────
    cap = cv2.VideoCapture(CAMERA_INDEX)

    if not cap.isOpened():
        print(f"[ERROR] Could not open camera index {CAMERA_INDEX}")
        print("        Try changing CAMERA_INDEX to 1 or 2")
        sys.exit(1)

    # Set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, DISPLAY_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, DISPLAY_HEIGHT)

    print("[✓] Camera opened successfully!")
    print("[✓] Live detection running — press Q to quit\n")

    # ── State variables ─────────────────────────────────────────────────────
    frame_count   = 0
    fps           = 0.0
    fps_timer     = time.time()
    fps_frames    = 0
    paused        = False
    last_results  = []
    last_weed_cnt = 0
    last_crop_cnt = 0
    screenshot_no = 1

    # ── Main loop ───────────────────────────────────────────────────────────
    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                print("[WARN] Frame capture failed — retrying...")
                time.sleep(0.1)
                continue

            frame_count += 1
            fps_frames  += 1

            # FPS calculation every second
            elapsed = time.time() - fps_timer
            if elapsed >= 1.0:
                fps       = fps_frames / elapsed
                fps_timer = time.time()
                fps_frames = 0

            # Run inference every FRAME_SKIP frames
            if frame_count % FRAME_SKIP == 0:
                results = model.predict(
                    source=frame,
                    conf=CONF_THRESH,
                    iou=0.45,
                    verbose=False,
                    device=device,
                )

                last_results  = []
                last_weed_cnt = 0
                last_crop_cnt = 0

                if results and results[0].boxes is not None:
                    for box in results[0].boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                        conf     = round(float(box.conf[0]), 2)
                        cls_id   = int(box.cls[0])
                        raw_name = class_names.get(cls_id, f"class_{cls_id}")
                        label    = classify_label(raw_name)
                        color    = WEED_COLOR if label == "weed" else CROP_COLOR

                        if label == "weed":
                            last_weed_cnt += 1
                        else:
                            last_crop_cnt += 1

                        last_results.append((x1, y1, x2, y2, conf, label, color))

            # Draw cached results on current frame
            for (x1, y1, x2, y2, conf, label, color) in last_results:
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                text = f"{label} {conf:.2f}"
                (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
                cv2.rectangle(frame, (x1, y1 - th - 8), (x1 + tw + 4, y1), color, -1)
                cv2.putText(frame, text, (x1 + 2, y1 - 4),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, WHITE, 1, cv2.LINE_AA)

                # Spray point for weeds
                if label == "weed":
                    cx = x1 + (x2 - x1) // 2
                    cy = y1 + (y2 - y1) // 2
                    cv2.circle(frame, (cx, cy), 5, WEED_COLOR, -1)
                    cv2.circle(frame, (cx, cy), 8, WHITE, 1)

            # Draw HUD overlay
            frame = draw_overlay(frame, last_weed_cnt, last_crop_cnt, fps, paused)

        # ── Show frame ───────────────────────────────────────────────────────
        cv2.imshow("AgroShield — Live Detection", frame)

        # ── Key handling ─────────────────────────────────────────────────────
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q') or key == ord('Q'):
            print("\n[✓] Quit — closing live detection.")
            break

        elif key == ord('s') or key == ord('S'):
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fname = f"{SCREENSHOT_DIR}/live_{screenshot_no:03d}_{ts}.jpg"
            cv2.imwrite(fname, frame)
            print(f"[📸] Screenshot saved: {fname}")
            screenshot_no += 1

        elif key == ord('p') or key == ord('P'):
            paused = not paused
            status = "PAUSED" if paused else "RESUMED"
            print(f"[{status}]")

    # ── Cleanup ──────────────────────────────────────────────────────────────
    cap.release()
    cv2.destroyAllWindows()
    print(f"\n[✓] Live detection ended.")
    print(f"    Screenshots saved: {SCREENSHOT_DIR}")


if __name__ == "__main__":
    live_detection()