"""Screenshot the NCN snippet figure."""

from pathlib import Path
import shutil
from playwright.sync_api import sync_playwright

HTML_PATH = Path(__file__).parent / "ncn_snippet.html"
OUT_PATH  = Path(__file__).parent / "ncn_snippet.png"
FIGURES   = Path(__file__).parent.parent / "latex_template" / "figures" / "ncn_snippet.png"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 900, "height": 400},
            device_scale_factor=2,
        )
        page.goto(f"file:///{HTML_PATH.as_posix()}")
        page.wait_for_timeout(400)

        card = page.query_selector(".ncn-fig")
        if card is None:
            raise RuntimeError("Could not find .ncn-fig element")

        img_bytes = card.screenshot()
        OUT_PATH.write_bytes(img_bytes)
        shutil.copy2(OUT_PATH, FIGURES)
        print(f"Saved {OUT_PATH}  ({len(img_bytes)//1024} KB)")
        print(f"Copied to {FIGURES}")
        browser.close()

if __name__ == "__main__":
    main()
