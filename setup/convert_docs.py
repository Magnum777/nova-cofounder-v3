#!/usr/bin/env python3
"""Convert .md files to HTML and PDF via Playwright (clean headers/footers)."""

import markdown
import os
from pathlib import Path

BASE = Path(__file__).parent.parent / "docs"
STYLE = BASE / "nova-style.css"

def md_to_html(md_path, html_path, title="Nova AI Cofounder V3"):
    """Convert markdown to styled HTML."""
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()
    
    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc"])
    html_body = md.convert(md_text)
    
    css = ""
    if STYLE.exists():
        with open(STYLE, "r", encoding="utf-8") as f:
            css = f.read()
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
{css}
</style>
</head>
<body>
{html_body}
</body>
</html>"""
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  HTML: {md_path.name}")

def html_to_pdf(html_path, pdf_path):
    """Convert HTML to PDF via Playwright (no headers/footers)."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(f"  PDF skipped: Install playwright (`pip install playwright; playwright install chromium`)")
        return False
    
    file_url = "file:///" + str(html_path).replace("\\", "/")
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(file_url, wait_until="networkidle")
        
        page.pdf(
            path=str(pdf_path),
            format="A4",
            margin={"top": "20mm", "right": "15mm", "bottom": "20mm", "left": "15mm"},
            display_header_footer=False
        )
        browser.close()
    
    if pdf_path.exists():
        print(f"  PDF:  {pdf_path.name}")
        return True
    else:
        print(f"  PDF failed: {pdf_path.name}")
        return False

def main():
    print("=== Converting Markdown to HTML + PDF ===")
    
    # PDF docs
    pdf_dir = BASE / "PDF"
    if pdf_dir.exists():
        print("\nPDF Docs:")
        for md_file in sorted(pdf_dir.glob("*.md")):
            base = md_file.stem
            html_path = pdf_dir / f"{base}.html"
            pdf_path = pdf_dir / f"{base}.pdf"
            
            md_to_html(md_file, html_path)
            html_to_pdf(html_path, pdf_path)
    
    # Video scripts
    video_dir = BASE / "video-scripts"
    if video_dir.exists():
        print("\nVideo Scripts:")
        for md_file in sorted(video_dir.glob("*.md")):
            base = md_file.stem
            html_path = video_dir / f"{base}.html"
            md_to_html(md_file, html_path, title="Nova V3 Video Script")
    
    print("\nDone.")

if __name__ == "__main__":
    main()
