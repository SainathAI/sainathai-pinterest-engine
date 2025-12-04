import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import postPin from "../pinterest/api/postPin.js";

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json({ limit: "10mb" }));

// Health check
app.get("/healthz", (req, res) => {
  res.status(200).send("OK");
});

// Generate Content (LLM)
app.post("/generate-content", async (req, res) => {
  try {
    const { niche } = req.body;
    if (!niche) return res.status(400).json({ error: "Missing niche" });

    const title = `Pinterest Pin for ${niche}`;
    const description = `This is an auto-generated pin description for ${niche}.`;

    res.json({ title, description });
  } catch (err) {
    console.error("Content generation error:", err);
    res.status(500).json({ error: "Failed to generate content" });
  }
});

// Create Pinterest Pin
app.post("/post-pin", async (req, res) => {
  try {
    const result = await postPin(req.body);
    res.json(result);
  } catch (err) {
    console.error("Post pin error:", err);
    res.status(500).json({ error: "Failed to post pin" });
  }
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () =>
  console.log(`Pinterest Engine running on port ${PORT}`)
);
