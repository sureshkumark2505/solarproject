const express = require("express");
const fs = require("fs");
const path = require("path");
const cors = require("cors");

const app = express();
app.use(cors());

// Path to EDGE folder
const EDGE_PATH = path.join(__dirname, "../EdgeAI");

// Route: Get summary.json
app.get("/api/summary", (req, res) => {
  const filePath = path.join(EDGE_PATH, "summary.json");

  try {
    const data = fs.readFileSync(filePath, "utf-8");
    res.json(JSON.parse(data));
  } catch (err) {
    res.status(500).json({
      error: "Edge summary not found. Run edge_run.py first."
    });
  }
});

// Health check
app.get("/", (req, res) => {
  res.send("Solar API is running");
});

// Start server
app.listen(5000, () => {
  console.log("API running at http://localhost:5000");
});
