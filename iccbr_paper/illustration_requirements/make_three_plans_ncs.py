"""
Screenshot the three-pane NormCode snippet card (NC Compilations + PPT Generation
+ Code Assistant) from three_plans_ncs.html and save as three_plans_ncs.png.
Also copies the result into the latex_template/figures directory.
"""

from pathlib import Path
import shutil
from playwright.sync_api import sync_playwright

HTML_PATH = Path(__file__).parent / "three_plans_ncs.html"
OUT_PATH  = Path(__file__).parent / "three_plans_ncs.png"
FIGURES   = Path(__file__).parent.parent / "latex_template" / "figures" / "three_plans_ncs.png"

VIEWPORT_W = 1200
VIEWPORT_H = 1000

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": VIEWPORT_W, "height": VIEWPORT_H},
            device_scale_factor=2,
        )
        page.goto(f"file:///{HTML_PATH.as_posix()}")
        page.wait_for_timeout(400)

        card = page.query_selector(".nc-trio")
        if card is None:
            raise RuntimeError("Could not find .nc-trio element in the HTML")

        img_bytes = card.screenshot()
        OUT_PATH.write_bytes(img_bytes)
        shutil.copy2(OUT_PATH, FIGURES)
        print(f"Saved {OUT_PATH}  ({len(img_bytes)//1024} KB)")
        print(f"Copied to {FIGURES}")
        browser.close()

if __name__ == "__main__":
    main()
