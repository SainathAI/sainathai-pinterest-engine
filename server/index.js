import express from "express";

const app = express();
app.use(express.json());

// Health check
app.get("/healthz", (req, res) => {
  res.status(200).send("OK");
});

// Basic test route
app.get("/api/test", (req, res) => {
  res.status(200).json({ status: "Pinterest Engine Running" });
});

// Default fallback
app.get("/", (req, res) => {
  res.send("Pinterest Engine Backend Active");
});

// Railway binds PORT automatically
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
