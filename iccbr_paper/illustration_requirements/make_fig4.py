"""
Generate fig4.png: a 2×3 collage of the 6 PPT slides from ppt_example_generated.html.
Each slide is screenshotted at 960×540 via playwright, then tiled into a
labelled grid and saved as fig4.png.
"""

import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

HTML_PATH = Path(__file__).parent / "ppt_example_generated.html"
OUT_PATH  = Path(__file__).parent / "fig4.png"
SLIDE_W, SLIDE_H = 960, 540   # native slide size in px
TOTAL_SLIDES = 6

# Collage layout
COLS, ROWS    = 3, 2
THUMB_W       = 480            # each thumb width
THUMB_H       = int(THUMB_W * SLIDE_H / SLIDE_W)   # 270
PAD           = 24             # gap between thumbs
MARGIN        = 40             # outer margin
LABEL_H       = 28             # height below each thumb for slide number
BG_COLOR      = (245, 247, 250)
BORDER_COLOR  = (180, 190, 205)
SHADOW_OFFSET = 4

def screenshot_slides():
    slides = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": SLIDE_W + 40, "height": SLIDE_H + 120})
        page.goto(f"file:///{HTML_PATH.as_posix()}")
        page.wait_for_timeout(800)   # let iframes settle

        for i in range(1, TOTAL_SLIDES + 1):
            # Click the i-th dot to navigate to that slide
            dots = page.query_selector_all(".dot")
            if dots and len(dots) >= i:
                dots[i - 1].click()
                page.wait_for_timeout(400)

            # Locate the .slide-container and screenshot it
            container = page.query_selector(".slide-container")
            if container:
                img_bytes = container.screenshot()
                from io import BytesIO
                img = Image.open(BytesIO(img_bytes)).convert("RGB")
            else:
                img = Image.new("RGB", (SLIDE_W, SLIDE_H), (200, 200, 200))
            slides.append(img)
            print(f"  captured slide {i}")

        browser.close()
    return slides


def build_collage(slides):
    canvas_w = MARGIN*2 + COLS*THUMB_W + (COLS-1)*PAD
    canvas_h = MARGIN*2 + ROWS*(THUMB_H + LABEL_H) + (ROWS-1)*PAD
    canvas = Image.new("RGB", (canvas_w, canvas_h), BG_COLOR)
    draw   = ImageDraw.Draw(canvas)

    # Try to load a font; fall back to default
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except Exception:
        font = ImageFont.load_default()

    for idx, img in enumerate(slides):
        col = idx % COLS
        row = idx // COLS
        x = MARGIN + col * (THUMB_W + PAD)
        y = MARGIN + row * (THUMB_H + LABEL_H + PAD)

        # Drop shadow
        shadow_box = [x + SHADOW_OFFSET, y + SHADOW_OFFSET,
                      x + THUMB_W + SHADOW_OFFSET, y + THUMB_H + SHADOW_OFFSET]
        draw.rectangle(shadow_box, fill=(200, 207, 218))

        # Resize and paste thumb
        thumb = img.resize((THUMB_W, THUMB_H), Image.LANCZOS)
        canvas.paste(thumb, (x, y))

        # Border
        draw.rectangle([x, y, x + THUMB_W, y + THUMB_H],
                       outline=BORDER_COLOR, width=1)

        # Slide number label below
        label = f"Slide {idx + 1}"
        bbox = font.getbbox(label)
        tw = bbox[2] - bbox[0]
        lx = x + (THUMB_W - tw) // 2
        ly = y + THUMB_H + 6
        draw.text((lx, ly), label, fill=(90, 100, 120), font=font)

    return canvas


def main():
    print("Launching browser to screenshot slides...")
    slides = screenshot_slides()
    print("Building collage...")
    collage = build_collage(slides)
    collage.save(OUT_PATH, dpi=(150, 150))
    print(f"Saved: {OUT_PATH}")


if __name__ == "__main__":
    main()
