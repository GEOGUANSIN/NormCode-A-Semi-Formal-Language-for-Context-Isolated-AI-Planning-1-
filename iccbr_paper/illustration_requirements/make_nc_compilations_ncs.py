from pathlib import Path
from playwright.sync_api import sync_playwright

HTML_PATH = Path(__file__).parent / "nc_compilations_ncs.html"
OUT_PATH  = Path(__file__).parent / "nc_compilations_ncs.png"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 600, "height": 800},
            device_scale_factor=2,
        )
        page.goto(f"file:///{HTML_PATH.as_posix()}")
        page.wait_for_timeout(400)

        card = page.query_selector(".nc-card")
        if card is None:
            raise RuntimeError("Could not find .nc-card element")

        img_bytes = card.screenshot()
        OUT_PATH.write_bytes(img_bytes)
        print(f"Saved {OUT_PATH}  ({len(img_bytes)//1024} KB)")
        browser.close()

if __name__ == "__main__":
    main()
