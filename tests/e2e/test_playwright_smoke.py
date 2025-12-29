import os

import pytest


@pytest.mark.asyncio
async def test_playwright_basic_navigation():
    if os.getenv("PLAYWRIGHT_E2E") != "1":
        pytest.skip("Set PLAYWRIGHT_E2E=1 to run Playwright smoke tests.")

    try:
        from playwright.async_api import async_playwright
    except Exception:
        pytest.skip("Playwright not installed.")

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://example.com")
        title = await page.title()
        await browser.close()

    assert "Example" in title
