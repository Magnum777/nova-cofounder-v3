#!/usr/bin/env python3
"""Convert .md files to HTML (styled) and PDF (via Chrome headless)."""

import markdown
import os
import sys
import subprocess
from pathlib import Path

BASE = Path(__file__).parent.parent / "docs"
STYLE = BASE / "nova-style.css"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(EDGE):
    EDGE = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

def md_to_html(md_path, html_path, title="Nova AI Cofounder V3"):
    """Convert markdown to styled HTML."""
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()
    
    # Convert markdown to HTML body
    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc"])
    html_body = md.convert(md_text)
    
    # Read CSS
    css = ""
    if STYLE.exists():
        with open(STYLE, "r", encoding="utf-8") as f:
            css = f.read()
    
    # Build full HTML document
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
    """Convert HTML to PDF via Edge headless."""
    if not os.path.exists(EDGE):
        print(f"  PDF skipped (Edge not found)")
        return False
    
    file_url = "file:///" + str(html_path).replace("\\", "/")
    
    cmd = [
        EDGE,
        "--headless",
        f"--print-to-pdf={pdf_path}",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=10000",
        file_url
    ]
    
    result = subprocess.run(cmd, capture_output=True, timeout=30)
    
    if os.path.exists(pdf_path):
        print(f"  PDF:  {Path(pdf_path).name}")
        return True
    else:
        print(f"  PDF failed: {Path(pdf_path).name}")
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
    
    print("\nDone. Check:")
    print(f"  {pdf_dir} — HTML + PDF")
    print(f"  {video_dir} — HTML")

if __name__ == "__main__":
    main()
