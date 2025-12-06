// engine/pinterest/post-pin.js
const axios = require("axios");

async function postPin({ board_id, title, description, alt_text, image_url }) {
  const token = process.env.PINTEREST_ACCESS_TOKEN;
  if (!token) throw new Error("Missing PINTEREST_ACCESS_TOKEN env var");

  const payload = {
    title,
    description,
    board_id,
    alt_text,
    media_source: {
      source_type: "image_url",
      url: image_url
    }
  };

  try {
    const res = await axios.post(
      "https://api.pinterest.com/v5/pins",
      payload,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      }
    );

    return {
      ok: true,
      pin_id: res.data.id,
      link: res.data.link || null
    };

  } catch (err) {
    console.error("Pinterest error:", err.response?.data || err.message);
    return {
      ok: false,
      error: err.response?.data || err.message
    };
  }
}

module.exports = { postPin };
