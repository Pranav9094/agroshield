import { useState } from "react";
import "./App.css";
import ImageUpload from "./components/ImageUpload";
import ResultCanvas from "./components/ResultCanvas";
import Dashboard from "./components/Dashboard";

function App() {
  const [imageFile, setImageFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleDetect = (file) => {
    setImageFile(file);
    setLoading(true);
    setError(null);

    // Dummy data — Day 4 mein real API se aayega
    setTimeout(() => {
      setResult({
        weed_count: 3,
        crop_count: 5,
        area_affected_pct: 38.5,
        high_risk_zones: 2,
        detections: [
          { label: "weed", confidence: 0.91, bbox: [120, 80, 85, 60], center: [162, 110] },
          { label: "crop", confidence: 0.87, bbox: [250, 150, 90, 70], center: [295, 185] },
          { label: "weed", confidence: 0.78, bbox: [400, 200, 75, 55], center: [437, 227] },
          { label: "crop", confidence: 0.82, bbox: [550, 120, 80, 65], center: [590, 152] },
          { label: "weed", confidence: 0.69, bbox: [300, 300, 70, 50], center: [335, 325] },
        ],
        spray_points: [[162, 110], [437, 227], [335, 325]],
        density_map: {
          zone_1: 0.85, zone_2: 0.12, zone_3: 0.67,
          zone_4: 0.45, zone_5: 0.92, zone_6: 0.23,
          zone_7: 0.78, zone_8: 0.34, zone_9: 0.56,
        },
      });
      setLoading(false);
    }, 2000);
  };

  const handleReset = () => {
    setImageFile(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-inner">
          <span className="logo">🌿 AgroShield</span>
          <span className="subtitle">AI Weed Detection for Precision Agriculture</span>
        </div>
      </header>

      <main className="main">
        <section className="upload-section">
          <ImageUpload onDetect={handleDetect} loading={loading} />
          {error && <p style={{ color: "red", marginTop: 8 }}>{error}</p>}
          {result && (
            <button onClick={handleReset} style={{
              marginTop: 12, padding: "8px 20px", background: "#fff",
              border: "1.5px solid #2D6A4F", color: "#2D6A4F",
              borderRadius: 7, cursor: "pointer", fontSize: 13, fontWeight: 600,
            }}>
              🔄 Reset / Try Another Image
            </button>
          )}
        </section>

        {result && (
          <section className="result-section" style={{ display: "flex", gap: 24, flexWrap: "wrap" }}>
            <div style={{ flex: 1, minWidth: 300 }}>
              <ResultCanvas
                imageFile={imageFile}
                detections={result.detections}
                spray_points={result.spray_points}
                density_map={result.density_map}
              />

            </div>
            <div style={{ flex: 1, minWidth: 300 }}>
              <Dashboard result={result} />
            </div>
          </section>
        )}

        {!result && (
          <section className="result-section">
            <div className="result-placeholder">
              <div className="result-icon">🔍</div>
              <p className="result-text">Detection results will appear here</p>
              <p className="result-hint">Upload an image and click Detect Weeds</p>
            </div>
          </section>
        )}
      </main>

      <footer className="footer">
        <p>Precision Agriculture Through AI 🌿</p>
      </footer>
    </div>
  );
}

export default App;