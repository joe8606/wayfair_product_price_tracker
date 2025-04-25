import asyncio
from playwright.async_api import async_playwright

async def test_wayfair_sponsored_products():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # 顯示瀏覽器畫面
        page = await browser.new_page()
        url = "https://www.wayfair.com/furniture/sb0/desks-c1780384.html?redir=desk&rtype=9"
        await page.goto(url)
        await page.wait_for_selector("section._1hwhogy1", timeout=15000)

        print("🔃 Starting lazy scroll...")

        # 滾動 + lazy loading 等待
        prev_count = 0
        for i in range(25):
            await page.mouse.wheel(0, 600)  # 小幅滾動
            await page.evaluate("window.scrollBy(0, 800)")  # 強制向下滾動一點
            await asyncio.sleep(2.5)  # 給 JS 載入商品時間

            section = await page.query_selector("section._1hwhogy1")
            cards = await section.query_selector_all('div[data-node-id="SponsoredListingCollectionItem"]')

            print(f"🌀 Scroll #{i+1} → {len(cards)} product blocks")

            if len(cards) > prev_count:
                prev_count = len(cards)
            else:
                print("🛑 No new cards loaded, stopping.")
                break

        print(f"\n📦 Total: {prev_count} sponsored product blocks.\n")

        # 輸出商品名稱
        for i, card in enumerate(cards, start=1):
            title_tag = await card.query_selector("h2")
            title = await title_tag.inner_text() if title_tag else "❓ Unknown Title"
            print(f"{i}. {title}")

        # 等你手動關閉視窗
        input("\n🛑 Press Enter to close the browser...")
        await browser.close()

# ▶️ Run it
if __name__ == "__main__":
    asyncio.run(test_wayfair_sponsored_products())
