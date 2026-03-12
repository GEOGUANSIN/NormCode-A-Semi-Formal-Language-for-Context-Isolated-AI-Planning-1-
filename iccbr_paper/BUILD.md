# Building the ICCBR paper PDF

## Prerequisites

- **LaTeX:** Install [MiKTeX](https://miktex.org/download) or [TeX Live](https://www.tug.org/texlive/). Ensure `pdflatex` and `bibtex` are on your PATH.

## Build

From a terminal, run from the `latex_template` folder:

```powershell
cd iccbr_paper\latex_template
.\build.ps1
```

Or from the repo root:

```powershell
.\iccbr_paper\latex_template\build.ps1
```

Output: `iccbr_paper/latex_template/main.pdf`.

## One-off commands (if you prefer not to use the script)

```powershell
cd iccbr_paper\latex_template
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

## If pdflatex is not in PATH

- **MiKTeX:** Add `C:\Program Files\MiKTeX\miktex\bin\x64\` (or your install path) to System / User PATH.
- **TeX Live:** Add `C:\texlive\2024\bin\windows\` (or your year) to PATH.

After installing, close and reopen the terminal (or restart Cursor) so the new PATH is picked up, then run `.\build.ps1` again.
