#!/usr/bin/env python3
"""
Minimal Playwright scraper for documentation snapshots.
"""
import argparse
import asyncio
from pathlib import Path


async def scrape(url: str, output_path: Path) -> None:
    try:
        from playwright.async_api import async_playwright
    except Exception as exc:
        raise RuntimeError("Playwright not installed. Run: python -m playwright install") from exc

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        content = await page.content()
        await browser.close()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Playwright doc scraper")
    parser.add_argument("--url", required=True, help="URL to capture")
    parser.add_argument("--output", required=True, help="Output HTML path")
    args = parser.parse_args()

    output_path = Path(args.output)
    asyncio.run(scrape(args.url, output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
