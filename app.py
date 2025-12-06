from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os, io, zipfile, time
from engine import generate_title, generate_description, generate_image, package_assets

app = FastAPI()
if not os.path.exists("outputs"):
    os.makedirs("outputs")

@app.get('/', response_class=HTMLResponse)
def homepage():
    return """<html><head><title>Pinterest Engine</title></head>
    <body>
    <h2>Pinterest Engine - Quick UI</h2>
    <form action="/generate" method="post">
    Keyword: <input name="keyword" />
    <button type="submit">Generate</button>
    </form>
    </body></html>"""

@app.post('/generate')
async def generate(keyword: str = Form(...)):
    ts = int(time.time())
    title = generate_title(keyword)
    desc = generate_description(keyword)
    img_path = generate_image(keyword, output_dir="outputs", filename=f"pin_{ts}.png")
    zip_path = package_assets([img_path], title, desc, out_dir="outputs", basename=f"pinpack_{ts}")
    return FileResponse(zip_path, media_type='application/zip', filename=os.path.basename(zip_path))
