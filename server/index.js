const express = require("express");
const pinterestAPI = require("./pinterest-api");

const app = express();

app.get("/healthz", (req, res) => res.send("OK"));

app.use("/api", pinterestAPI);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log("SainathAI Pinterest Engine running on", PORT));
