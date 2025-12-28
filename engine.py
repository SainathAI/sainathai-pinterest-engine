import os
import csv
import textwrap
import gc  # Garbage Collection for 4GB RAM efficiency
from PIL import Image, ImageDraw, ImageFont

# ================= CONFIG =================
IMAGE_WIDTH = 1000
IMAGE_HEIGHT = 1500
TEMPLATE_PATH = "healthcare_template_clean.png"
INPUT_CSV = "pinterest_input.csv"
OUTPUT_DIR = r"D:\GITHUB\sainathai-site\pins"
BULK_CSV_OUT = "pinterest_final_bulk.csv"
FONT_PATH = "fonts/DejaVuSans-Bold.ttf"
LANDING_PAGE = "https://sainathai.github.io/SainathAI/healthcare-automation.html"
BASE_IMAGE_URL = "https://sainathai.github.io/SainathAI/pins"

# PRO UI COLORS
ACCENT_COLOR = (56, 189, 248)
TEXT_COLOR = (255, 255, 255)
OVERLAY_COLOR = (2, 6, 23, 220) # Slightly darker for better readability

def draw_pixel_wrapped_text(draw, text, font, max_width):
    """Wraps text based on pixel width instead of character count."""
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        if draw.textlength(test_line, font=font) <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))
    return lines

def generate_factory():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    try:
        base_template = Image.open(TEMPLATE_PATH).convert("RGBA").resize((IMAGE_WIDTH, IMAGE_HEIGHT))
    except:
        print("Template error."); return

    bulk_data = []

    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            img = base_template.copy()
            draw = ImageDraw.Draw(img)
            
            headline_text = row.get('headline', row.get('title', 'NO TITLE')).upper()
            subtitle_text = row.get('subhead', row.get('description', ''))

            # Fonts
            h_font = ImageFont.truetype(FONT_PATH, 68 if len(headline_text) < 30 else 60)
            s_font = ImageFont.truetype(FONT_PATH, 40)
            c_font = ImageFont.truetype(FONT_PATH, 38)

            # 1. PIXEL WRAPPING (Fixes bleeding)
            max_px = 850 
            wrapped_h = draw_pixel_wrapped_text(draw, headline_text, h_font, max_px)
            wrapped_s = draw_pixel_wrapped_text(draw, subtitle_text, s_font, max_px - 50)

            # 2. CALCULATE OVERLAY HEIGHT
            start_y = 500
            curr_y = start_y
            h_heights = []
            for line in wrapped_h:
                bbox = draw.textbbox((500, curr_y), line, font=h_font, anchor="mt")
                h_heights.append(bbox[3] - bbox[1])
                curr_y += (bbox[3] - bbox[1]) + 15
            
            curr_y += 30 # Space
            s_heights = []
            for line in wrapped_s:
                bbox = draw.textbbox((500, curr_y), line, font=s_font, anchor="mt")
                s_heights.append(bbox[3] - bbox[1])
                curr_y += (bbox[3] - bbox[1]) + 10

            # 3. DYNAMIC OVERLAY (Glassmorphism)
            overlay = Image.new("RGBA", img.size, (0,0,0,0))
            o_draw = ImageDraw.Draw(overlay)
            # Add padding for CTA at bottom
            o_draw.rectangle([0, start_y - 60, 1000, curr_y + 180], fill=OVERLAY_COLOR)
            img = Image.alpha_composite(img, overlay)
            draw = ImageDraw.Draw(img)

            # 4. DRAW CONTENT
            y = start_y
            for i, line in enumerate(wrapped_h):
                draw.text((500, y), line, font=h_font, anchor="mt", fill=TEXT_COLOR)
                y += h_heights[i] + 15
            y += 30
            for i, line in enumerate(wrapped_s):
                draw.text((500, y), line, font=s_font, anchor="mt", fill=ACCENT_COLOR)
                y += s_heights[i] + 10

            # 5. CTA
            y += 70
            cta = "GET INTELLIGENCE REPORT"
            cw = draw.textlength(cta, font=c_font)
            draw.rectangle([(500-cw/2)-30, y-15, (500+cw/2)+30, y+60], outline=ACCENT_COLOR, width=4)
            draw.text((500, y), cta, font=c_font, anchor="mt", fill=TEXT_COLOR)

            # 6. SAVE & CLEANUP (Crucial for 4GB RAM)
            fname = f"pin_{idx}.png"
            img.convert("RGB").save(os.path.join(OUTPUT_DIR, fname), quality=90)
            
            # Memory Management
            del img, draw, overlay, o_draw
            gc.collect() 

            bulk_data.append({"Title": headline_text, "Link": LANDING_PAGE, "Image URL": f"{BASE_IMAGE_URL}/{fname}"})

    print(f"Done! {len(bulk_data)} pins created.")

if __name__ == "__main__":
    generate_factory()