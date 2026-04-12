const HeatmapOverlay = ({ density_map = {}, visible = true }) => {
  if (!visible) return null;

  const getColor = (val) => {
    if (val >= 0.71) return "rgba(220, 38, 38, 0.45)";
    if (val >= 0.31) return "rgba(234, 179, 8, 0.35)";
    return "rgba(34, 197, 94, 0.30)";
  };

  return (
    <div style={{
      position: "absolute", top: 0, left: 0,
      width: "100%", height: "100%",
      display: "grid", gridTemplateColumns: "repeat(3, 1fr)",
      gridTemplateRows: "repeat(3, 1fr)",
      pointerEvents: "none",
    }}>
      {Array.from({ length: 9 }, (_, i) => {
        const key = `zone_${i + 1}`;
        const val = density_map[key] ?? 0;
        return (
          <div key={i} style={{
            background: getColor(val),
            border: "1px solid rgba(255,255,255,0.15)",
            display: "flex", alignItems: "center",
            justifyContent: "center",
          }}>
            <span style={{
              color: "#fff", fontSize: 11, fontWeight: 700,
              textShadow: "0 1px 3px rgba(0,0,0,0.8)",
            }}>
              {(val * 100).toFixed(0)}%
            </span>
          </div>
        );
      })}
    </div>
  );
};

export default HeatmapOverlay;