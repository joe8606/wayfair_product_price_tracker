import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from datetime import datetime
from pathlib import Path
import os

# --- Settings ---
USERNAME = os.getenv("OXYLAB_USERNAME")
PASSWORD = os.getenv("OXYLAB_PASSWORD")
CSV_INPUT_PATH = Path("dat/wayfair_bs4_products.csv")
OUTPUT_FOLDER = Path("dat")
MAX_RETRIES = 3
DELAY_BETWEEN_REQUESTS = (2, 5)

# --- Functions ---
def fetch_price_from_url(url):
    payload = {
        "source": "universal_ecommerce",
        "url": url,
        "user_agent_type": "desktop_safari",
        "geo_location": "United States",
        "render": "html"
    }
    try:
        response = requests.post(
            "https://realtime.oxylabs.io/v1/queries",
            auth=(USERNAME, PASSWORD),
            json=payload,
            timeout=180
        )
        if response.status_code == 200:
            result = response.json()
            html_content = result["results"][0]["content"]
            soup = BeautifulSoup(html_content, "html.parser")
            price_span = soup.find("span", {"data-test-id": "PriceDisplay"})
            if price_span:
                return price_span.get_text(strip=True)
            else:
                return None
        else:
            print(f"[ERROR] API Request failed. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")
        return None

# --- Main Execution ---
def main():
    df = pd.read_csv(CSV_INPUT_PATH)
    urls = df['url'].tolist()[:10]

    records = []
    success_count = 0
    total_time = 0

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    for url in urls:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        price = None
        start_time = time.time()

        for attempt in range(1, MAX_RETRIES + 1):
            print(f"[INFO] Attempt {attempt} for URL: {url}")
            price = fetch_price_from_url(url)
            if price is not None:
                print(f"[SUCCESS] Found price: {price}")
                break
            else:
                print("[WARN] Price not found, retrying...")
                time.sleep(random.uniform(*DELAY_BETWEEN_REQUESTS))

        end_time = time.time()
        elapsed_time = end_time - start_time
        total_time += elapsed_time

        if price is not None:
            success_count += 1

        records.append({
            "timestamp": timestamp,
            "url": url,
            "price": price,
            "time_spent_sec": round(elapsed_time, 2)
        })

    result_df = pd.DataFrame(records)

    # Save output
    output_time = datetime.now().strftime("%Y%m%d_%H%M")
    output_filename = f"wayfair_price_tracking_{output_time}.csv"
    output_path = OUTPUT_FOLDER / output_filename
    result_df.to_csv(output_path, index=False)

    # Save log
    log_filename = "wayfair_scrape_log.txt"
    log_path = OUTPUT_FOLDER / log_filename
    with log_path.open("a") as log_file:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"\n[{now}] New Run\n")
        log_file.write(f"Total URLs: {len(urls)}\n")
        log_file.write(f"Successful fetches: {success_count}\n")
        log_file.write(f"Failed fetches: {len(urls) - success_count}\n")
        log_file.write(f"Success rate: {success_count/len(urls)*100:.2f}%\n")
        log_file.write(f"Average time per URL: {total_time/len(urls):.2f} seconds\n")
        log_file.write("="*40 + "\n")

    print(f"[DONE] Saved {len(result_df)} records to {output_path}")
    print(f"[DONE] Log saved to {log_path}")

if __name__ == "__main__":
    main()
