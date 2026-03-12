"""
Screenshot the side-by-side NormCode snippet card (Example 2) from
normcode_snippet_template.html and save as ppt_and_code_ncs.png.
"""

from pathlib import Path
from playwright.sync_api import sync_playwright

HTML_PATH = Path(__file__).parent / "normcode_snippet_template.html"
OUT_PATH  = Path(__file__).parent / "ppt_and_code_ncs.png"

# The side-by-side card is 780px wide; give the viewport extra room
VIEWPORT_W = 900
VIEWPORT_H = 1200

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": VIEWPORT_W, "height": VIEWPORT_H},
            device_scale_factor=2,   # 2× for crisp PNG at print resolution
        )
        page.goto(f"file:///{HTML_PATH.as_posix()}")
        page.wait_for_timeout(400)

        # The side-by-side pair is the second .nc-pair element
        card = page.query_selector(".nc-pair")
        if card is None:
            raise RuntimeError("Could not find .nc-pair element in the HTML")

        img_bytes = card.screenshot()
        OUT_PATH.write_bytes(img_bytes)
        print(f"Saved {OUT_PATH}  ({len(img_bytes)//1024} KB)")
        browser.close()

if __name__ == "__main__":
    main()
