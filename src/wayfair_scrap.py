from playwright.sync_api import sync_playwright
import pandas as pd
import re
import os
from datetime import datetime

def extract_float(text):
    """Extract a float number from price/rating strings"""
    if not text:
        return None
    try:
        return float(re.sub(r"[^\d.]", "", text))
    except:
        return None

def extract_int(text):
    """Extract an integer from review count strings"""
    if not text:
        return None
    try:
        return int(re.sub(r"[^\d]", "", text))
    except:
        return None

def scrape_wayfair(keyword="desk", max_pages=2):
    product_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for page_num in range(1, max_pages + 1):
            url = f"https://www.wayfair.com/keyword.php?keyword={keyword}&curpage={page_num}"
            print(f"📄 Scraping page {page_num}...")
            page.goto(url)
            page.wait_for_load_state("networkidle")

            cards = page.query_selector_all("div[class*='ProductCard']")
            for card in cards:
                try:
                    # Product title and URL
                    title_elem = card.query_selector("a[data-enzyme-id='product-title']")
                    title = title_elem.inner_text().strip() if title_elem else None
                    href = title_elem.get_attribute("href") if title_elem else None
                    full_url = f"https://www.wayfair.com{href}" if href else None

                    # Price
                    price_elem = card.query_selector("div[class*='BasePrice']")
                    price_text = price_elem.inner_text().strip() if price_elem else None
                    price = extract_float(price_text)

                    # Brand
                    brand_elem = card.query_selector("span[class*='ProductCard-brand']")
                    brand = brand_elem.inner_text().strip().replace("by ", "") if brand_elem else None

                    # Rating
                    rating_elem = card.query_selector("span[class*='AverageRating']")
                    rating = extract_float(rating_elem.inner_text()) if rating_elem else None

                    # Review count
                    review_elem = card.query_selector("span[class*='RatingCount']")
                    review_count = extract_int(review_elem.inner_text()) if review_elem else None

                    product_data.append({
                        "name": title,
                        "brand": brand,
                        "price": price,
                        "rating": rating,
                        "review_count": review_count,
                        "url": full_url,
                        "category": keyword,
                        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                except Exception as e:
                    print("❌ Error parsing a product:", e)

        browser.close()

    return pd.DataFrame(product_data)

# Run the scraper and save to CSV
if __name__ == "__main__":
    df = scrape_wayfair(keyword="desk", max_pages=2)
    os.makedirs("dat", exist_ok=True)
    output_path = f"dat/wayfair_desk_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(output_path, index=False)
    print(f"✅ Done! {len(df)} products saved to {output_path}")