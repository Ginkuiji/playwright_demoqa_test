import asyncio
from playwright.async_api import async_playwright, expect


async def run():
    async with async_playwright() as a:
        browser = await a.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://demoqa.com/text-box")

        await page.fill("#userName", "Nobody")
        await page.fill("#userEmail", "mail@mail.com")
        await page.fill("#currentAddress", "here")
        await page.fill("#permanentAddress", "nowhere")
        await page.click("#submit")

        await expect(page.locator("#output")).to_contain_text("Nobody")

        await page.screenshot(path="text_box.png", full_page=True)

asyncio.run(run())
