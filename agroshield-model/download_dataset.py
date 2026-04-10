"""
AgroShield — Dataset Downloader
Downloads WeedCrop dataset from Roboflow in YOLOv8 format.
Usage: python download_dataset.py --api-key YOUR_API_KEY
"""

import os
import sys
import argparse
from pathlib import Path


def count_images(split_dir: Path) -> int:
    """Count images in a dataset split directory."""
    images_dir = split_dir / "images"
    if not images_dir.exists():
        return 0
    extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    return sum(1 for f in images_dir.iterdir() if f.suffix.lower() in extensions)


def download_dataset(api_key: str, save_dir: str = "./datasets/weedcrop") -> bool:
    try:
        from roboflow import Roboflow
    except ImportError:
        print("[ERROR] 'roboflow' package not found.")
        print("        Install it with:  pip install roboflow")
        return False

    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    print("=" * 55)
    print("  AgroShield — Roboflow Dataset Downloader")
    print("=" * 55)
    print(f"  Workspace : srec-dthh0")
    print(f"  Project   : crop-weed-poxtn")
    print(f"  Version   : 2")
    print(f"  Format    : YOLOv8")
    print(f"  Save dir  : {save_path.resolve()}")
    print("=" * 55)

    try:
        print("\n[1/3] Authenticating with Roboflow...")
        rf = Roboflow(api_key=api_key)

        print("[2/3] Accessing project...")
        project = rf.workspace("srec-dthh0").project("crop-weed-poxtn")
        version = project.version(2)

        print("[3/3] Downloading dataset (YOLOv8 format)...")
        dataset = version.download("yolov8", location=str(save_path), overwrite=True)

        print("\n[✓] Download complete!\n")

    except Exception as e:
        print(f"\n[ERROR] Download failed: {e}")
        print("\nPossible causes:")
        print("  • Invalid API key")
        print("  • Wrong workspace / project name")
        print("  • No internet connection")
        print("  • Roboflow rate limit reached")
        return False

    splits = {
        "train": save_path / "train",
        "valid": save_path / "valid",
        "test":  save_path / "test",
    }

    print("-" * 35)
    print("  Dataset image counts:")
    print("-" * 35)
    total = 0
    for split_name, split_path in splits.items():
        count = count_images(split_path)
        total += count
        status = f"{count:>5} images" if count > 0 else "  not found"
        print(f"  {split_name:<8}: {status}")
    print("-" * 35)
    print(f"  {'TOTAL':<8}: {total:>5} images")
    print("-" * 35)

    yaml_path = save_path / "data.yaml"
    if yaml_path.exists():
        print(f"\n[✓] data.yaml found at: {yaml_path.resolve()}")
    else:
        print("\n[WARN] data.yaml not found — check the download folder manually.")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Download crop-weed dataset from Roboflow for AgroShield"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=os.environ.get("ROBOFLOW_API_KEY", ""),
        help="Roboflow API key (or set ROBOFLOW_API_KEY env var)",
    )
    parser.add_argument(
        "--save-dir",
        type=str,
        default="./datasets/weedcrop",
        help="Directory to save the dataset (default: ./datasets/weedcrop)",
    )
    args = parser.parse_args()

    if not args.api_key:
        print("[ERROR] No API key provided.")
        print("        Pass it with:  --api-key YOUR_KEY")
        print("        Or export:     export ROBOFLOW_API_KEY=YOUR_KEY")
        sys.exit(1)

    success = download_dataset(api_key=args.api_key, save_dir=args.save_dir)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
