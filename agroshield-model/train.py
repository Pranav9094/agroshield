"""
AgroShield — YOLOv8 Model Trainer
Trains YOLOv8n on crop-weed dataset and saves best model.
Usage: python train.py
"""

import os
import sys
import shutil
from pathlib import Path


def train():
    # ── Imports ────────────────────────────────────────────────────────────
    try:
        import torch
        from ultralytics import YOLO
    except ImportError as e:
        print(f"[ERROR] Missing package: {e}")
        print("        Run: pip install ultralytics torch")
        sys.exit(1)

    # ── Config ─────────────────────────────────────────────────────────────
    DATASET_YAML = "./datasets/weedcrop/data.yaml"
    MODEL_DIR    = "./models"
    BEST_MODEL   = "./models/best.pt"
    EPOCHS       = 80
    IMG_SIZE     = 640
    BATCH        = 16
    PROJECT      = "./runs/train"
    RUN_NAME     = "agroshield_v1"

    # ── Device check ───────────────────────────────────────────────────────
    print("=" * 55)
    print("  AgroShield — YOLOv8 Trainer")
    print("=" * 55)

    if torch.cuda.is_available():
        device = 0
        gpu_name = torch.cuda.get_device_name(0)
        print(f"  Device    : GPU — {gpu_name}")
    else:
        device = "cpu"
        print("  [WARN] CUDA not available — using CPU (slow!)")
        print("  [WARN] Consider using Google Colab for faster training.")

    print(f"  Model     : YOLOv8n (nano)")
    print(f"  Epochs    : {EPOCHS}")
    print(f"  Image size: {IMG_SIZE}")
    print(f"  Batch     : {BATCH}")
    print(f"  Dataset   : {DATASET_YAML}")
    print("=" * 55)

    # ── Dataset check ──────────────────────────────────────────────────────
    if not Path(DATASET_YAML).exists():
        print(f"\n[ERROR] data.yaml not found at: {DATASET_YAML}")
        print("        Run download_dataset.py first!")
        sys.exit(1)

    # ── Create models dir ──────────────────────────────────────────────────
    Path(MODEL_DIR).mkdir(parents=True, exist_ok=True)

    # ── Load model ─────────────────────────────────────────────────────────
    print("\n[1/3] Loading YOLOv8n model...")
    model = YOLO("yolov8n.pt")

    # ── Train ──────────────────────────────────────────────────────────────
    print("[2/3] Starting training...\n")
    results = model.train(
        data=DATASET_YAML,
        epochs=EPOCHS,
        imgsz=IMG_SIZE,
        batch=BATCH,
        device=device,
        project=PROJECT,
        name=RUN_NAME,
        exist_ok=True,
        patience=20,
        save=True,
        plots=True,
        verbose=True,
    )

    # ── Save best model ────────────────────────────────────────────────────
    print("\n[3/3] Saving best model...")

    best_src = Path(PROJECT) / RUN_NAME / "weights" / "best.pt"

    if best_src.exists():
        shutil.copy(str(best_src), BEST_MODEL)
        print(f"[✓] Best model saved to: {BEST_MODEL}")
    else:
        print(f"[WARN] best.pt not found at expected path: {best_src}")
        print("       Check runs/train/agroshield_v1/weights/ manually.")

    # ── Print final mAP50 ──────────────────────────────────────────────────
    print("\n" + "=" * 55)
    print("  TRAINING COMPLETE!")
    print("=" * 55)

    try:
        metrics = results.results_dict
        map50   = metrics.get("metrics/mAP50(B)", None)
        map5095 = metrics.get("metrics/mAP50-95(B)", None)
        prec    = metrics.get("metrics/precision(B)", None)
        rec     = metrics.get("metrics/recall(B)", None)

        if map50 is not None:
            print(f"  mAP50      : {map50:.4f} ({map50*100:.2f}%)")
        if map5095 is not None:
            print(f"  mAP50-95   : {map5095:.4f} ({map5095*100:.2f}%)")
        if prec is not None:
            print(f"  Precision  : {prec:.4f} ({prec*100:.2f}%)")
        if rec is not None:
            print(f"  Recall     : {rec:.4f} ({rec*100:.2f}%)")
    except Exception as e:
        print(f"  [WARN] Could not extract metrics: {e}")
        print("         Check runs/train/agroshield_v1/results.csv for details.")

    print("=" * 55)
    print(f"  Best model : {BEST_MODEL}")
    print("=" * 55)


if __name__ == "__main__":
    train()