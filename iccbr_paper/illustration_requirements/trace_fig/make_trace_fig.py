"""
Screenshot the composite trace figure from compose_trace_fig.html.
Copies result into latex_template/figures/.
"""

from pathlib import Path
import shutil
from playwright.sync_api import sync_playwright

HTML_PATH = Path(__file__).parent / "compose_trace_fig.html"
OUT_PATH  = Path(__file__).parent / "trace_composite.png"
FIGURES   = Path(__file__).parent.parent.parent / "latex_template" / "figures" / "trace_composite.png"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1200, "height": 2400},
            device_scale_factor=2,
        )
        page.goto(f"file:///{HTML_PATH.as_posix()}")
        page.wait_for_timeout(600)

        card = page.query_selector(".trace-composite")
        if card is None:
            raise RuntimeError("Could not find .trace-composite element")

        img_bytes = card.screenshot()
        OUT_PATH.write_bytes(img_bytes)
        shutil.copy2(OUT_PATH, FIGURES)
        print(f"Saved {OUT_PATH}  ({len(img_bytes)//1024} KB)")
        print(f"Copied to {FIGURES}")
        browser.close()

if __name__ == "__main__":
    main()
