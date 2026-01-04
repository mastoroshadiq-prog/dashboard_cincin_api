#!/usr/bin/env python3
"""
Script untuk mengkonversi HTML Report ke PDF
Menggunakan playwright (headless Chromium)
"""

import asyncio
import argparse
from pathlib import Path
import sys

async def convert_html_to_pdf(html_path: Path, pdf_path: Path = None):
    """
    Konversi file HTML ke PDF menggunakan playwright
    
    Args:
        html_path: Path ke file HTML
        pdf_path: Path output PDF (opsional, default sama dengan HTML tapi .pdf)
    """
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("❌ Error: playwright tidak terinstall. Jalankan:")
        print("   pip install playwright")
        print("   playwright install chromium")
        return False
    
    if not html_path.exists():
        print(f"❌ Error: File tidak ditemukan: {html_path}")
        return False
    
    if pdf_path is None:
        pdf_path = html_path.with_suffix('.pdf')
    
    print(f"📄 Mengkonversi: {html_path.name}")
    print(f"   → {pdf_path.name}")
    
    try:
        async with async_playwright() as p:
            # Launch headless browser
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Load HTML file
            await page.goto(f'file:///{html_path.resolve()}', wait_until='networkidle')
            
            # Generate PDF
            await page.pdf(
                path=str(pdf_path),
                format='A4',
                print_background=True,
                margin={
                    'top': '20mm',
                    'bottom': '20mm',
                    'left': '15mm',
                    'right': '15mm'
                }
            )
            
            await browser.close()
        
        print(f"   ✅ Berhasil: {pdf_path}")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

async def convert_all_reports(output_base_dir: Path):
    """
    Konversi semua report.html di folder output
    """
    # Cari semua folder dengan report.html
    report_files = list(output_base_dir.glob("*/report.html"))
    
    if not report_files:
        print("⚠️ Tidak ditemukan file report.html di folder output")
        return
    
    print(f"\n📊 Ditemukan {len(report_files)} file report.html")
    print("=" * 60)
    
    success_count = 0
    for html_file in sorted(report_files):
        folder_name = html_file.parent.name
        print(f"\n📁 Folder: {folder_name}")
        
        if await convert_html_to_pdf(html_file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Selesai: {success_count}/{len(report_files)} file berhasil dikonversi")

def main():
    parser = argparse.ArgumentParser(
        description="Konversi HTML Report ke PDF"
    )
    parser.add_argument(
        "--file", "-f",
        type=str,
        help="Path ke file HTML spesifik (opsional)"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Konversi semua report.html di folder output"
    )
    
    args = parser.parse_args()
    
    # Default output directory
    output_dir = Path(__file__).parent / "data" / "output" / "cincin_api"
    
    if args.file:
        # Konversi file spesifik
        html_path = Path(args.file)
        asyncio.run(convert_html_to_pdf(html_path))
    elif args.all:
        # Konversi semua
        asyncio.run(convert_all_reports(output_dir))
    else:
        # Default: konversi semua
        print("\n🔄 Mengkonversi semua report.html ke PDF...")
        asyncio.run(convert_all_reports(output_dir))

if __name__ == "__main__":
    main()
