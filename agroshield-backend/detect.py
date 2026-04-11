import os
import cv2
import numpy as np
import base64
from PIL import Image

def compute_spray_zones(detections, image_width, image_height):
    zone_counts = {f"zone_{i}": 0 for i in range(1, 10)}
    total_weed_area = 0
    
    for det in detections:
        if det['label'] == 'weed':
            cx, cy = det['center']
            bw, bh = det['bbox'][2], det['bbox'][3]
            total_weed_area += bw * bh
            
            col = min(int(cx / (image_width / 3)), 2)
            row = min(int(cy / (image_height / 3)), 2)
            zone_num = row * 3 + col + 1
            zone_counts[f"zone_{zone_num}"] += 1
    
    total_weeds = max(sum(zone_counts.values()), 1)
    density_map = {k: round(v / total_weeds, 2) for k, v in zone_counts.items()}
    high_risk_zones = sum(1 for v in density_map.values() if v > 0.5)
    image_area = image_width * image_height
    area_affected_pct = round((total_weed_area / image_area) * 100, 2)
    
    return density_map, high_risk_zones, area_affected_pct

def detect_weeds(image_path: str) -> dict:
    # Check if real model exists
    model_path = "../agroshield-model/models/best.pt"
    
    if os.path.exists(model_path):
        # Real model detection
        from ultralytics import YOLO
        model = YOLO(model_path)
        results = model(image_path)
        
        image = cv2.imread(image_path)
        h, w = image.shape[:2]
        
        detections = []
        spray_points = []
        
        for result in results:
            for box in result.boxes:
                label = result.names[int(box.cls)]
                confidence = round(float(box.conf), 2)
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                bw, bh = x2 - x1, y2 - y1
                cx, cy = x1 + bw // 2, y1 + bh // 2
                
                det = {
                    "label": label,
                    "confidence": confidence,
                    "bbox": [x1, y1, bw, bh],
                    "center": [cx, cy]
                }
                detections.append(det)
                
                color = (0, 0, 255) if label == "weed" else (0, 204, 0)
                cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
                cv2.putText(image, f"{label} {int(confidence*100)}%",
                           (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
                if label == "weed":
                    spray_points.append([cx, cy])
    else:
        # Dummy response when model not available
        image = cv2.imread(image_path)
        if image is None:
            image = np.zeros((640, 640, 3), dtype=np.uint8)
        h, w = image.shape[:2]
        
        detections = [
            {"label": "weed", "confidence": 0.91, "bbox": [120, 300, 85, 60], "center": [162, 330]},
            {"label": "weed", "confidence": 0.85, "bbox": [300, 200, 70, 50], "center": [335, 225]},
            {"label": "crop", "confidence": 0.87, "bbox": [200, 150, 90, 70], "center": [245, 185]},
            {"label": "crop", "confidence": 0.92, "bbox": [400, 350, 80, 60], "center": [440, 380]},
        ]
        spray_points = [[162, 330], [335, 225]]
        
        # Draw dummy boxes
        for det in detections:
            x, y, bw, bh = det['bbox']
            color = (0, 0, 255) if det['label'] == 'weed' else (0, 204, 0)
            cv2.rectangle(image, (x, y), (x+bw, y+bh), color, 2)
            cv2.putText(image, f"{det['label']} {int(det['confidence']*100)}%",
                       (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    # Save annotated image
    os.makedirs("./outputs", exist_ok=True)
    output_path = "./outputs/annotated.jpg"
    cv2.imwrite(output_path, image)
    
    # Convert to base64
    with open(output_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode("utf-8")
    
    weed_count = sum(1 for d in detections if d['label'] == 'weed')
    crop_count = sum(1 for d in detections if d['label'] == 'crop')
    density_map, high_risk_zones, area_affected_pct = compute_spray_zones(detections, w, h)
    
    return {
        "weed_count": weed_count,
        "crop_count": crop_count,
        "detections": detections,
        "spray_points": spray_points,
        "density_map": density_map,
        "area_affected_pct": area_affected_pct,
        "high_risk_zones": high_risk_zones,
        "annotated_image": img_base64
    }