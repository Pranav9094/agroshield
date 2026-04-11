"""
AgroShield — Weed Detection Inference
Loads trained YOLOv8 model and detects weeds/crops in images.
Usage: python inference.py --image path/to/image.jpg
"""

import sys
import argparse
from pathlib import Path


# ── Colour constants ────────────────────────────────────────────────────────
WEED_COLOR = (51, 51, 255)    # #FF3333 in BGR
CROP_COLOR = (51, 204, 51)    # #33CC33 in BGR


def detect_weeds(image_path: str) -> dict:
    """
    Detect weeds and crops in an image using trained YOLOv8 model.

    Args:
        image_path: Path to input image

    Returns:
        {
            'weed_count': int,
            'crop_count': int,
            'detections': [
                {
                    'label': 'weed' or 'crop',
                    'confidence': float,
                    'bbox': [x, y, w, h],
                    'center': [cx, cy]
                }
            ],
            'spray_points': [[cx, cy], ...],
            'annotated_image_path': str
        }
    """
    try:
        import cv2
        import torch
        from ultralytics import YOLO
    except ImportError as e:
        print(f"[ERROR] Missing package: {e}")
        sys.exit(1)

    # ── Paths ───────────────────────────────────────────────────────────────
    MODEL_PATH  = "./models/best.pt"
    OUTPUT_DIR  = "./outputs"
    OUTPUT_PATH = f"{OUTPUT_DIR}/annotated.jpg"

    # ── Empty result template ───────────────────────────────────────────────
    empty_result = {
        "weed_count": 0,
        "crop_count": 0,
        "detections": [],
        "spray_points": [],
        "annotated_image_path": OUTPUT_PATH,
    }

    # ── Validate inputs ─────────────────────────────────────────────────────
    if not Path(MODEL_PATH).exists():
        print(f"[ERROR] Model not found: {MODEL_PATH}")
        print("        Run train.py first!")
        return empty_result

    if not Path(image_path).exists():
        print(f"[ERROR] Image not found: {image_path}")
        return empty_result

    # ── Create output dir ───────────────────────────────────────────────────
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # ── Load model ──────────────────────────────────────────────────────────
    print(f"[1/3] Loading model from {MODEL_PATH}...")
    model = YOLO(MODEL_PATH)

    # ── Run inference ───────────────────────────────────────────────────────
    print(f"[2/3] Running inference on {image_path}...")
    results = model.predict(
        source=image_path,
        conf=0.25,
        iou=0.45,
        verbose=False,
    )

    # ── Load image for annotation ───────────────────────────────────────────
    image = cv2.imread(image_path)
    if image is None:
        print(f"[ERROR] Could not read image: {image_path}")
        return empty_result

    # ── Parse detections ────────────────────────────────────────────────────
    print("[3/3] Parsing detections...")

    detections  = []
    spray_points = []
    weed_count  = 0
    crop_count  = 0

    # Get class names from model
    class_names = model.names  # {0: 'class1', 1: 'class2', ...}

    # Keywords to identify weed vs crop
    WEED_KEYWORDS = {"weed", "wild", "broadleaf", "narrowleaf", "morningglory"}
    CROP_KEYWORDS = {"crop", "maize", "corn", "wheat", "soybean", "rice"}

    def classify_label(name: str) -> str:
        """Map raw class name to 'weed' or 'crop'."""
        name_lower = name.lower()
        for kw in WEED_KEYWORDS:
            if kw in name_lower:
                return "weed"
        for kw in CROP_KEYWORDS:
            if kw in name_lower:
                return "crop"
        # Fallback: even class indices = crop, odd = weed
        return "weed"

    if results and results[0].boxes is not None:
        boxes = results[0].boxes

        for box in boxes:
            # Raw values
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            conf     = round(float(box.conf[0]), 4)
            cls_id   = int(box.cls[0])
            raw_name = class_names.get(cls_id, f"class_{cls_id}")
            label    = classify_label(raw_name)

            # BBox in [x, y, w, h] format
            bx = x1
            by = y1
            bw = x2 - x1
            bh = y2 - y1

            # Center point
            cx = x1 + bw // 2
            cy = y1 + bh // 2

            # Counts
            if label == "weed":
                weed_count += 1
                spray_points.append([cx, cy])
                color = WEED_COLOR
            else:
                crop_count += 1
                color = CROP_COLOR

            # Add to detections list
            detections.append({
                "label":      label,
                "confidence": conf,
                "bbox":       [bx, by, bw, bh],
                "center":     [cx, cy],
            })

            # ── Draw bounding box ──────────────────────────────────────────
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

            # ── Draw label ────────────────────────────────────────────────
            text = f"{label} {conf:.2f}"
            (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
            cv2.rectangle(image, (x1, y1 - th - 8), (x1 + tw + 4, y1), color, -1)
            cv2.putText(
                image, text,
                (x1 + 2, y1 - 4),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55, (255, 255, 255), 1, cv2.LINE_AA
            )

            # ── Draw spray point (weed only) ───────────────────────────────
            if label == "weed":
                cv2.circle(image, (cx, cy), 5, WEED_COLOR, -1)
                cv2.circle(image, (cx, cy), 8, (255, 255, 255), 1)

    # ── Save annotated image ─────────────────────────────────────────────────
    cv2.imwrite(OUTPUT_PATH, image)

    # ── Build result dict ────────────────────────────────────────────────────
    result = {
        "weed_count":           weed_count,
        "crop_count":           crop_count,
        "detections":           detections,
        "spray_points":         spray_points,
        "annotated_image_path": OUTPUT_PATH,
    }

    # ── Print summary ────────────────────────────────────────────────────────
    print("\n" + "=" * 50)
    print("  AgroShield Detection Results")
    print("=" * 50)
    print(f"  Weeds detected : {weed_count} 🌿")
    print(f"  Crops detected : {crop_count} 🌾")
    print(f"  Total          : {len(detections)}")
    print(f"  Spray points   : {len(spray_points)}")
    print(f"  Annotated image: {OUTPUT_PATH}")
    print("=" * 50)

    if detections:
        print("\n  Detections:")
        for i, d in enumerate(detections):
            print(f"  [{i+1}] {d['label']:<5} | conf: {d['confidence']:.2f} | "
                  f"center: {d['center']} | bbox: {d['bbox']}")

    return result


# ── CLI entry point ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="AgroShield — Detect weeds and crops in an image"
    )
    parser.add_argument(
        "--image",
        type=str,
        required=True,
        help="Path to input image (jpg/png)"
    )
    args = parser.parse_args()

    result = detect_weeds(args.image)

    if not result["detections"]:
        print("\n[INFO] No detections found in this image.")

    return result


if __name__ == "__main__":
    main()
