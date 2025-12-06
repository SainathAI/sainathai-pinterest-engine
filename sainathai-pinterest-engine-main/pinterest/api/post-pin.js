import fetch from "node-fetch";

const PINTEREST_API = "https://api.pinterest.com/v5/pins";

export default async function postPin({ title, description, image_url, board_id }) {
  try {
    const token = process.env.PINTEREST_ACCESS_TOKEN;

    if (!token) throw new Error("Missing Pinterest token");
    if (!image_url) throw new Error("Missing image_url");

    const payload = {
      board_id,
      title,
      description,
      media_source: {
        source_type: "image_url",
        url: image_url
      }
    };

    const res = await fetch(PINTEREST_API, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (!res.ok) {
      console.error("Pinterest API Error:", data);
      throw new Error(data?.message || "Failed to create pin");
    }

    return { success: true, pin: data };
  } catch (err) {
    console.error("postPin error:", err);
    return { success: false, error: err.message };
  }
}
