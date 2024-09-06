import asyncio
import nodriver as driver

async def main(url, output_path):
    browser = await driver.start()
    await asyncio.sleep(1)
    tab = await browser.get(url)
    await tab.set_window_size(left=0, top=0, width=3840, height=2160)
    await asyncio.sleep(10)
    await tab.save_screenshot(format="png", full_page=True, filename=output_path)

# Example usage
url = "https://resume-review-lake.vercel.app"
output_path = "screenshot.png"

if __name__ == "__main__":
    driver.loop().run_until_complete(main(url, output_path))