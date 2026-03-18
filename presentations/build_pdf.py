#!/usr/bin/env python3
"""
build_pdf.py — Convert HTML slides to a multi-page PDF preview.

Usage:
    python presentations/build_pdf.py

Requirements:
    pip install playwright pillow
    playwright install chromium
"""

import sys
from pathlib import Path


def main() -> None:
    # ------------------------------------------------------------------ #
    # Resolve paths relative to this script's location                    #
    # ------------------------------------------------------------------ #
    script_dir = Path(__file__).parent
    slides_dir = script_dir / "slides"
    output_pdf = script_dir / "problem_slides_preview.pdf"

    # ------------------------------------------------------------------ #
    # Pre-flight checks                                                    #
    # ------------------------------------------------------------------ #
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "ERROR: playwright is not installed.\n"
            "       Run:  pip install playwright && playwright install chromium",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        from PIL import Image
    except ImportError:
        print(
            "ERROR: Pillow is not installed.\n"
            "       Run:  pip install pillow",
            file=sys.stderr,
        )
        sys.exit(1)

    if not slides_dir.exists():
        print(
            f"ERROR: Slides directory not found: {slides_dir}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Section order: P slides (problem + solution mechanics) then E slides (UAV examples)
    def _slide_sort_key(p: Path) -> tuple:
        import re
        prefix = p.stem[0]       # 'P' or 'E'
        match = re.match(r'\d+', p.stem[1:])
        number = int(match.group()) if match else 0
        section = 0 if prefix == "P" else 1
        return (section, number)

    slide_files = sorted(
        list(slides_dir.glob("P*.html")) + list(slides_dir.glob("E*.html")),
        key=_slide_sort_key,
    )

    if not slide_files:
        print(
            f"ERROR: No slides matching P*.html or E*.html found in {slides_dir}",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Found {len(slide_files)} slide(s):")
    for f in slide_files:
        print(f"  {f.name}")

    # ------------------------------------------------------------------ #
    # Capture screenshots with Playwright                                  #
    # ------------------------------------------------------------------ #
    screenshots: list[Path] = []
    tmp_dir = script_dir / ".slide_screenshots"
    tmp_dir.mkdir(exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            device_scale_factor=1,
        )

        for idx, slide_path in enumerate(slide_files, start=1):
            page = context.new_page()
            file_url = slide_path.as_uri()

            print(f"  [{idx}/{len(slide_files)}] Rendering {slide_path.name} …", end="", flush=True)
            page.goto(file_url, wait_until="networkidle", timeout=15_000)

            screenshot_path = tmp_dir / f"slide_{idx:03d}.png"
            page.screenshot(
                path=str(screenshot_path),
                clip={"x": 0, "y": 0, "width": 1280, "height": 720},
            )
            screenshots.append(screenshot_path)
            page.close()
            print(" done")

        context.close()
        browser.close()

    # ------------------------------------------------------------------ #
    # Combine screenshots into a single PDF with Pillow                   #
    # ------------------------------------------------------------------ #
    print(f"\nBuilding PDF -> {output_pdf.name} ...", end="", flush=True)

    images = [Image.open(str(p)).convert("RGB") for p in screenshots]

    if not images:
        print("\nERROR: No screenshots were captured.", file=sys.stderr)
        sys.exit(1)

    first_image = images[0]
    rest_images = images[1:]

    first_image.save(
        str(output_pdf),
        format="PDF",
        save_all=True,
        append_images=rest_images,
        resolution=96,
    )
    print(" done")

    # ------------------------------------------------------------------ #
    # Clean up temp screenshots                                            #
    # ------------------------------------------------------------------ #
    for p in screenshots:
        p.unlink(missing_ok=True)
    try:
        tmp_dir.rmdir()
    except OSError:
        pass  # non-empty dir — leave it

    print(f"\nSaved: {output_pdf}")
    print(f"Pages: {len(slide_files)}")


if __name__ == "__main__":
    main()
