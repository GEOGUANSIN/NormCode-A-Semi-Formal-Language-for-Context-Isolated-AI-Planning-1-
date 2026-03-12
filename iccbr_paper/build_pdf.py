#!/usr/bin/env python3
"""
Build the ICCBR paper PDF from LaTeX.
Double-click this script or run: python build_pdf.py

Requires: MiKTeX or TeX Live (pdflatex, bibtex).
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# Project paths: script lives in iccbr_paper/, build runs in latex_template/
SCRIPT_DIR = Path(__file__).resolve().parent
LATEX_DIR = SCRIPT_DIR / "latex_template"
MAIN_TEX = "main.tex"
OUTPUT_PDF = "main.pdf"
COPY_PDF = "NormCode_Canvas_ICCBR_initial.pdf"

# MiKTeX common install locations (pdflatex not always on PATH when double-clicking)
MIKTEX_PATHS = [
    Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64",
    Path(os.environ.get("ProgramFiles", "")) / "MiKTeX" / "miktex" / "bin" / "x64",
    Path(os.environ.get("ProgramFiles", "")) / "MiKTeX" / "miktex" / "bin",
]


def find_pdflatex():
    """Return path to pdflatex.exe, or None."""
    exe = shutil.which("pdflatex")
    if exe:
        return Path(exe)
    for base in MIKTEX_PATHS:
        if not base:
            continue
        exe = base / "pdflatex.exe"
        if exe.is_file():
            return exe
    return None


def find_bibtex():
    """Return path to bibtex.exe, or None."""
    exe = shutil.which("bibtex")
    if exe:
        return Path(exe)
    for base in MIKTEX_PATHS:
        if not base:
            continue
        exe = base / "bibtex.exe"
        if exe.is_file():
            return exe
    return None


def run(cmd, cwd):
    """Run command; return True if returncode is 0."""
    print(f"  Running: {' '.join(str(x) for x in cmd)}")
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=False, text=True)
        return r.returncode == 0
    except FileNotFoundError:
        print(f"  Error: command not found: {cmd[0]}")
        return False


def main():
    print("ICCBR paper — LaTeX build")
    print("=" * 50)

    pdflatex = find_pdflatex()
    bibtex = find_bibtex()
    if not pdflatex:
        print("ERROR: pdflatex not found. Install MiKTeX (https://miktex.org) or TeX Live.")
        input("Press Enter to close...")
        sys.exit(1)
    if not bibtex:
        print("ERROR: bibtex not found. Install MiKTeX or TeX Live.")
        input("Press Enter to close...")
        sys.exit(1)

    print(f"  pdflatex: {pdflatex}")
    print(f"  bibtex:   {bibtex}")
    print()

    if not (LATEX_DIR / MAIN_TEX).is_file():
        print(f"ERROR: {MAIN_TEX} not found in {LATEX_DIR}")
        input("Press Enter to close...")
        sys.exit(1)

    cwd = str(LATEX_DIR)

    print("Pass 1: pdflatex...")
    run([str(pdflatex), "-enable-installer", "-interaction=nonstopmode", "-file-line-error", MAIN_TEX], cwd)
    print()

    print("BibTeX...")
    run([str(bibtex), "main"], cwd)
    print()

    print("Pass 2: pdflatex...")
    run([str(pdflatex), "-enable-installer", "-interaction=nonstopmode", "-file-line-error", MAIN_TEX], cwd)
    print("Pass 3: pdflatex...")
    run([str(pdflatex), "-enable-installer", "-interaction=nonstopmode", "-file-line-error", MAIN_TEX], cwd)
    print()

    pdf_path = LATEX_DIR / OUTPUT_PDF
    if not pdf_path.is_file():
        print("ERROR: main.pdf was not produced. Check LaTeX errors above.")
        input("Press Enter to close...")
        sys.exit(1)

    copy_path = SCRIPT_DIR / COPY_PDF
    shutil.copy2(pdf_path, copy_path)
    print("=" * 50)
    print("SUCCESS")
    print(f"  PDF: {pdf_path}")
    print(f"  Copy: {copy_path}")
    print()
    input("Press Enter to close...")
    sys.exit(0)


if __name__ == "__main__":
    main()
