# Build ICCBR paper PDF from LaTeX
# Requires: pdflatex and bibtex on PATH (install MiKTeX or TeX Live if needed)
# Run from: iccbr_paper/latex_template (or pass -ProjectRoot)

param(
    [string]$ProjectRoot = $PSScriptRoot
)

Set-Location $ProjectRoot

$main = "main.tex"
if (-not (Test-Path $main)) {
    Write-Error "main.tex not found in $ProjectRoot"
    exit 1
}

# Check for pdflatex
$pdflatex = Get-Command pdflatex -ErrorAction SilentlyContinue
if (-not $pdflatex) {
    Write-Host "pdflatex not found. Install MiKTeX (https://miktex.org) or TeX Live, and ensure pdflatex is on PATH."
    exit 1
}

Write-Host "Pass 1: pdflatex..."
& pdflatex -enable-installer -interaction=nonstopmode -file-line-error $main
if ($LASTEXITCODE -ne 0) { Write-Warning "First pass had errors; continuing." }

Write-Host "BibTeX..."
& bibtex main
if ($LASTEXITCODE -ne 0) { Write-Warning "BibTeX had warnings (normal if no citations yet)." }

Write-Host "Pass 2: pdflatex..."
& pdflatex -enable-installer -interaction=nonstopmode -file-line-error $main
Write-Host "Pass 3: pdflatex..."
& pdflatex -enable-installer -interaction=nonstopmode -file-line-error $main

if (Test-Path "main.pdf") {
    Write-Host "Done. Output: $ProjectRoot\main.pdf"
} else {
    Write-Error "main.pdf was not produced. Check LaTeX errors above."
    exit 1
}
