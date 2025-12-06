import os, time, json
from PIL import Image, ImageDraw, ImageFont

HF_TOKEN = os.getenv('HF_TOKEN','')

def generate_title(keyword: str):
    return f"Top {keyword} ideas to boost engagement"

def generate_description(keyword: str):
    return f"High-converting pin ideas for {keyword}. Optimized for Pinterest SEO and CTR."

def generate_image(keyword: str, output_dir='outputs', filename=None):
    # Simple placeholder image generator (replace with HF image API call)
    os.makedirs(output_dir, exist_ok=True)
    if not filename:
        filename = f"pin_{int(time.time())}.png"
    path = os.path.join(output_dir, filename)
    img = Image.new('RGB', (1000,1500), color=(255,255,255))
    d = ImageDraw.Draw(img)
    text = keyword[:40]
    d.text((50,50), text, fill=(0,0,0))
    img.save(path)
    return path

def package_assets(image_paths, title, description, out_dir='outputs', basename=None):
    if not basename:
        basename = f"pinpack_{int(time.time())}"
    zip_path = os.path.join(out_dir, f"{basename}.zip")
    with zipfile.ZipFile(zip_path, 'w') as z:
        meta = {'title': title, 'description': description}
        z.writestr('meta.json', json.dumps(meta))
        for p in image_paths:
            z.write(p, arcname=os.path.basename(p))
    return zip_path
