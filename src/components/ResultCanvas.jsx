import { useEffect, useRef } from "react";

const ResultCanvas = ({ imageFile, detections = [], spray_points = [] }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    if (!imageFile || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    const img = new Image();
    const url = URL.createObjectURL(imageFile);

    img.onload = () => {
      const maxWidth = canvas.parentElement.offsetWidth || 800;
      const scale = maxWidth / img.width;
      canvas.width = maxWidth;
      canvas.height = img.height * scale;

      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

      detections.forEach((det) => {
        const [x, y, w, h] = det.bbox.map((v) => v * scale);
        const isWeed = det.label === "weed";
        const color = isWeed ? "#FF3333" : "#33CC33";
        const label = `${isWeed ? "Weed" : "Crop"} ${Math.round(det.confidence * 100)}%`;

        ctx.strokeStyle = color;
        ctx.lineWidth = 2.5;
        ctx.strokeRect(x, y, w, h);

        const fontSize = 12;
        ctx.font = `bold ${fontSize}px sans-serif`;
        const textWidth = ctx.measureText(label).width;
        const padding = 4;
        const tagH = fontSize + padding * 2;
        const tagY = y - tagH < 0 ? y : y - tagH;

        ctx.fillStyle = color;
        ctx.fillRect(x, tagY, textWidth + padding * 2, tagH);
        ctx.fillStyle = "#ffffff";
        ctx.fillText(label, x + padding, tagY + fontSize + padding - 2);
      });

      spray_points.forEach(([cx, cy]) => {
        const sx = cx * scale;
        const sy = cy * scale;
        ctx.beginPath();
        ctx.arc(sx, sy, 6, 0, Math.PI * 2);
        ctx.fillStyle = "#FF3333";
        ctx.fill();
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 2;
        ctx.stroke();
      });

      URL.revokeObjectURL(url);
    };

    img.src = url;
  }, [imageFile, detections, spray_points]);

  const handleDownload = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const link = document.createElement("a");
    link.download = "agroshield_annotated.jpg";
    link.href = canvas.toDataURL("image/jpeg", 0.92);
    link.click();
  };

  const weedCount = detections.filter((d) => d.label === "weed").length;
  const cropCount = detections.filter((d) => d.label === "crop").length;

  const styles = {
    wrapper: { width: "100%", fontFamily: "'Segoe UI', sans-serif" },
    canvasWrap: {
      position: "relative", width: "100%",
      border: "1.5px solid #2D6A4F", borderRadius: 8,
      overflow: "hidden", background: "#0a0a0a",
    },
    canvas: { display: "block", width: "100%" },
    empty: {
      display: "flex", alignItems: "center", justifyContent: "center",
      height: 220, color: "#52B788", fontSize: 14,
    },
    statsRow: { display: "flex", gap: 10, marginTop: 10 },
    statCard: (accent) => ({
      flex: 1, background: "#f7faf8",
      border: `1.5px solid ${accent}`, borderRadius: 8,
      padding: "8px 14px", textAlign: "center",
    }),
    statNum: (color) => ({ fontSize: 22, fontWeight: 700, color, display: "block" }),
    statLabel: { fontSize: 11, color: "#888", textTransform: "uppercase" },
    legend: { display: "flex", gap: 20, marginTop: 10, fontSize: 13, color: "#444" },
    dot: (color) => ({
      display: "inline-block", width: 12, height: 12,
      borderRadius: 2, background: color, marginRight: 5, verticalAlign: "middle",
    }),
    btn: {
      marginTop: 12, display: "inline-flex", alignItems: "center", gap: 6,
      padding: "9px 20px", background: "#2D6A4F", color: "#fff",
      border: "none", borderRadius: 7, fontSize: 13, fontWeight: 600, cursor: "pointer",
    },
  };

  return (
    <div style={styles.wrapper}>
      <div style={styles.canvasWrap}>
        {imageFile ? (
          <canvas ref={canvasRef} style={styles.canvas} />
        ) : (
          <div style={styles.empty}>Upload an image to see detection results</div>
        )}
      </div>

      {imageFile && (
        <>
          <div style={styles.statsRow}>
            <div style={styles.statCard("#FF3333")}>
              <span style={styles.statNum("#FF3333")}>{weedCount}</span>
              <span style={styles.statLabel}>Weeds</span>
            </div>
            <div style={styles.statCard("#33CC33")}>
              <span style={styles.statNum("#33CC33")}>{cropCount}</span>
              <span style={styles.statLabel}>Crops</span>
            </div>
            <div style={styles.statCard("#FF8C00")}>
              <span style={styles.statNum("#FF8C00")}>{spray_points.length}</span>
              <span style={styles.statLabel}>Spray Points</span>
            </div>
          </div>

          <div style={styles.legend}>
            <span><span style={styles.dot("#FF3333")} />Weed</span>
            <span><span style={styles.dot("#33CC33")} />Crop</span>
          </div>

          <button style={styles.btn} onClick={handleDownload}>
            ↓ Download Annotated Image
          </button>
        </>
      )}
    </div>
  );
};

export default ResultCanvas;