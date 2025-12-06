// server/pinterest-api.js
const express = require("express");
const bodyParser = require("body-parser");
const { postPin } = require("../engine/pinterest/post-pin");

const router = express.Router();
router.use(bodyParser.json({ limit: "2mb" }));

router.post("/post-pin", async (req, res) => {
  try {
    const result = await postPin(req.body);
    res.json(result);
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message });
  }
});

module.exports = router;
