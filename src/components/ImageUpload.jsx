import { useState, useRef } from "react";

const ImageUpload = ({ onDetect, loading }) => {
  const [preview, setPreview] = useState(null);
  const [fileName, setFileName] = useState("");
  const [fileSize, setFileSize] = useState("");
  const [dragOver, setDragOver] = useState(false);
  const inputRef = useRef(null);

  const handleFile = (file) => {
    if (!file) return;
    setFileName(file.name);
    setFileSize((file.size / 1024).toFixed(1) + " KB");
    const reader = new FileReader();
    reader.onloadend = () => setPreview(reader.result);
    reader.readAsDataURL(file);
  };

  const handleChange = (e) => handleFile(e.target.files[0]);

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    handleFile(e.dataTransfer.files[0]);
  };

  const handleDetect = () => {
    const file = inputRef.current.files[0];
    if (file) onDetect(file);
  };

  const styles = {
    wrapper: { width: "100%", fontFamily: "'Segoe UI', sans-serif" },
    dropzone: {
      border: dragOver ? "2px solid #2D6A4F" : "2px dashed #52B788",
      borderRadius: 12,
      padding: "32px 24px",
      textAlign: "center",
      background: dragOver ? "#f0faf4" : "#fff",
      cursor: "pointer",
      transition: "all 0.2s",
    },
    icon: { fontSize: 48, marginBottom: 12 },
    text: { fontSize: 16, fontWeight: 600, color: "#2D6A4F", margin: "0 0 4px" },
    hint: { fontSize: 13, color: "#888", margin: 0 },
    preview: {
      marginTop: 16,
      width: "100%",
      maxHeight: 300,
      objectFit: "contain",
      borderRadius: 8,
      border: "1px solid #d0e8da",
    },
    fileInfo: { marginTop: 8, fontSize: 13, color: "#555" },
    btn: {
      marginTop: 16,
      width: "100%",
      padding: "12px",
      background: loading ? "#888" : "#2D6A4F",
      color: "#fff",
      border: "none",
      borderRadius: 8,
      fontSize: 15,
      fontWeight: 700,
      cursor: loading ? "not-allowed" : "pointer",
      letterSpacing: 0.5,
    },
    spinner: { marginRight: 8 },
  };

  return (
    <div style={styles.wrapper}>
      <div
        style={styles.dropzone}
        onClick={() => inputRef.current.click()}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
      >
        <div style={styles.icon}>📷</div>
        <p style={styles.text}>Drag & drop a farm image here</p>
        <p style={styles.hint}>or click to browse</p>

        <input
          ref={inputRef}
          type="file"
          accept="image/*"
          style={{ display: "none" }}
          onChange={handleChange}
        />

        {preview && (
          <img src={preview} alt="preview" style={styles.preview} />
        )}
      </div>

      {fileName && (
        <p style={styles.fileInfo}>
          📁 {fileName} — {fileSize}
        </p>
      )}

      {preview && (
        <button
          style={styles.btn}
          onClick={handleDetect}
          disabled={loading}
        >
          {loading ? "⏳ Detecting..." : "🔍 Detect Weeds"}
        </button>
      )}
    </div>
  );
};

export default ImageUpload;