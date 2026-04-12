const Dashboard = ({ result }) => {
  if (!result) {
    return (
      <div style={styles.empty}>
        <p style={styles.emptyText}>Detection results will appear here</p>
      </div>
    );
  }

  const {
    weed_count = 0,
    crop_count = 0,
    area_affected_pct = 0,
    high_risk_zones = 0,
    detections = [],
    spray_points = [],
    density_map = {},
  } = result;

  const getZoneColor = (val) => {
    if (val >= 0.71) return { bg: "#ffecec", color: "#cc0000", label: "HIGH" };
    if (val >= 0.31) return { bg: "#fff8e1", color: "#e65c00", label: "MED" };
    return { bg: "#eafaf1", color: "#1a7a4a", label: "LOW" };
  };

  return (
    <div style={styles.wrapper}>

      {/* 4 Stat Cards */}
      <div style={styles.grid4}>
        <div style={styles.card}>
          <span style={styles.num("#e53935")}>{weed_count}</span>
          <span style={styles.label}>Weed Count</span>
        </div>
        <div style={styles.card}>
          <span style={styles.num("#2e7d32")}>{crop_count}</span>
          <span style={styles.label}>Crop Count</span>
        </div>
        <div style={styles.card}>
          <span style={styles.num("#e65c00")}>{area_affected_pct.toFixed(1)}%</span>
          <span style={styles.label}>Area Affected</span>
        </div>
        <div style={styles.card}>
          <span style={styles.num("#1565c0")}>{high_risk_zones}/9</span>
          <span style={styles.label}>High Risk Zones</span>
        </div>
      </div>

      {/* Detection Table */}
      <div style={styles.section}>
        <h3 style={styles.heading}>Detection Results</h3>
        {detections.length === 0 ? (
          <p style={styles.noData}>No detections</p>
        ) : (
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>#</th>
                <th style={styles.th}>Label</th>
                <th style={styles.th}>Confidence</th>
              </tr>
            </thead>
            <tbody>
              {detections.map((d, i) => (
                <tr key={i}>
                  <td style={styles.td}>{i + 1}</td>
                  <td style={styles.td}>
                    <span style={{
                      ...styles.badge,
                      background: d.label === "weed" ? "#ffecec" : "#eafaf1",
                      color: d.label === "weed" ? "#cc0000" : "#1a7a4a",
                    }}>
                      {d.label === "weed" ? "🌿 Weed" : "🌱 Crop"}
                    </span>
                  </td>
                  <td style={styles.td}>{Math.round(d.confidence * 100)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Spray Points */}
      <div style={styles.section}>
        <h3 style={styles.heading}>Spray Coordinates</h3>
        {spray_points.length === 0 ? (
          <p style={styles.noData}>No spray points</p>
        ) : (
          <div style={styles.sprayList}>
            {spray_points.map(([x, y], i) => (
              <span key={i} style={styles.sprayTag}>
                🎯 ({x}, {y})
              </span>
            ))}
          </div>
        )}
      </div>

      {/* 3x3 Heatmap */}
      <div style={styles.section}>
        <h3 style={styles.heading}>Field Density Heatmap</h3>
        <div style={styles.heatmap}>
          {Array.from({ length: 9 }, (_, i) => {
            const key = `zone_${i + 1}`;
            const val = density_map[key] ?? 0;
            const { bg, color, label } = getZoneColor(val);
            return (
              <div key={i} style={{ ...styles.zone, background: bg }}>
                <span style={{ fontSize: 13, fontWeight: 700, color }}>{label}</span>
                <span style={{ fontSize: 11, color }}>{(val * 100).toFixed(0)}%</span>
              </div>
            );
          })}
        </div>
        <div style={styles.heatLegend}>
          <span style={styles.legendItem("#eafaf1", "#1a7a4a")}>Low (0-30%)</span>
          <span style={styles.legendItem("#fff8e1", "#e65c00")}>Medium (31-70%)</span>
          <span style={styles.legendItem("#ffecec", "#cc0000")}>High (71-100%)</span>
        </div>
      </div>

    </div>
  );
};

const styles = {
  wrapper: { width: "100%", fontFamily: "'Segoe UI', sans-serif", marginTop: 24 },
  empty: { padding: 32, textAlign: "center" },
  emptyText: { color: "#888", fontSize: 14 },
  grid4: { display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12, marginBottom: 24 },
  card: {
    background: "#fff", border: "1.5px solid #d0e8da", borderRadius: 10,
    padding: "16px 12px", textAlign: "center", display: "flex",
    flexDirection: "column", gap: 6,
  },
  num: (color) => ({ fontSize: 28, fontWeight: 700, color }),
  label: { fontSize: 11, color: "#888", textTransform: "uppercase", letterSpacing: 0.5 },
  section: { marginBottom: 24 },
  heading: { fontSize: 15, fontWeight: 600, color: "#2D6A4F", marginBottom: 12 },
  noData: { color: "#aaa", fontSize: 13 },
  table: { width: "100%", borderCollapse: "collapse" },
  th: { background: "#f0f4f1", padding: "8px 12px", fontSize: 12, color: "#555", textAlign: "left", borderBottom: "1px solid #ddd" },
  td: { padding: "8px 12px", fontSize: 13, borderBottom: "1px solid #f0f0f0" },
  badge: { padding: "3px 10px", borderRadius: 20, fontSize: 12, fontWeight: 600 },
  sprayList: { display: "flex", flexWrap: "wrap", gap: 8 },
  sprayTag: { background: "#fff0f0", color: "#cc0000", border: "1px solid #ffcccc", borderRadius: 20, padding: "4px 12px", fontSize: 12 },
  heatmap: { display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 6 },
  zone: { borderRadius: 8, padding: "12px 8px", textAlign: "center", display: "flex", flexDirection: "column", gap: 2 },
  heatLegend: { display: "flex", gap: 12, marginTop: 10, flexWrap: "wrap" },
  legendItem: (bg, color) => ({ background: bg, color, padding: "3px 10px", borderRadius: 20, fontSize: 11, fontWeight: 600 }),
};

export default Dashboard;