write_status('START','script_started')

import pathlib, time
def write_status(code, msg):
    ts = time.strftime('%Y-%m-%d %H:%M:%S')
    p = pathlib.Path('logs/last_status.txt')
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"[{ts} IST] {code}:{msg}\n", encoding='utf-8')
    except Exception:
        pass
\nimport os, time, json, zipfile, sys, logging
from PIL import Image, ImageDraw, ImageFont

# Accept either HF_TOKEN or HF_ACCESS_TOKEN env var
HF_TOKEN = os.getenv('HF_ACCESS_TOKEN') or os.getenv('HF_TOKEN') or ''

logging.basicConfig(level=os.getenv('LOG_LEVEL','INFO'))
log = logging.getLogger("pinterest-engine")

def generate_title(keyword: str):
    return f"Top {keyword} ideas to boost engagement"

def generate_description(keyword: str):
    return f"High-converting pin ideas for {keyword}. Optimized for Pinterest SEO and CTR."

def generate_image(keyword: str, output_dir='outputs', filename=None):
    os.makedirs(output_dir, exist_ok=True)
    if not filename:
        filename = f"pin_{int(time.time())}.png"
    path = os.path.join(output_dir, filename)
    img = Image.new('RGB', (1000,1500), color=(255,255,255))
    d = ImageDraw.Draw(img)
    text = keyword[:40]
    # basic text placement
    try:
        d.text((50,50), text, fill=(0,0,0))
    except Exception:
        pass
    img.save(path)
    return path

def package_assets(image_paths, title, description, out_dir='outputs', basename=None):
    os.makedirs(out_dir, exist_ok=True)
    if not basename:
        basename = f"pinpack_{int(time.time())}"
    zip_path = os.path.join(out_dir, f"{basename}.zip")
    with zipfile.ZipFile(zip_path, 'w') as z:
        meta = {'title': title, 'description': description}
        z.writestr('meta.json', json.dumps(meta))
        for p in image_paths:
            z.write(p, arcname=os.path.basename(p))
    return zip_path

def read_first_keyword(path='keywords.txt'):
    if not os.path.exists(path):
        return 'home decor'
    with open(path,'r',encoding='utf-8') as f:
        for line in f:
            s = line.strip()
            if s:
                return s
    return 'home decor'

def run_pinterest_mode():
    log.info("Starting pinterest mode")
    keyword = read_first_keyword()
    log.info(f"Using keyword: {keyword}")
    title = generate_title(keyword)
    desc = generate_description(keyword)
    img = generate_image(keyword)
    log.info(f"Generated image: {img}")
    zipf = package_assets([img], title, desc)
    log.info(f"Packaged assets: {zipf}")
    # Minimal output for automation checks
    print(json.dumps({"status":"ok","keyword":keyword,"image":img,"zip":zipf}))

if __name__ == '__main__':
    mode = None
    if '--mode' in sys.argv:
        try:
            mode = sys.argv[sys.argv.index('--mode')+1]
        except Exception:
            mode = None
    # fallback: positional
    if not mode and len(sys.argv) > 1:
        mode = sys.argv[1]
    if mode == 'pinterest':
        run_pinterest_mode()
    else:
        log.info("No mode or unknown mode provided. Available: pinterest")
        print("usage: python engine.py --mode pinterest")
