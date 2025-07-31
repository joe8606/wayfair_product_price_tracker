# Wayfair Price Tracker

Automated price tracking system for Wayfair products using web scraping and GitHub Actions.

## Overview

This project automatically tracks price changes for Wayfair products by scraping product listings and monitoring price updates over time. It uses GitHub Actions for automated execution and stores historical data in CSV format.

## Features

- **Automated Scraping**: Daily product listing collection
- **Price Tracking**: Hourly price updates for tracked products
- **Historical Data**: Complete price history with timestamps
- **Multiple Methods**: Both Playwright and requests-based scrapers
- **Error Handling**: Retry mechanisms and logging
- **Git Integration**: Automatic commit and push of results

## How It Works

### GitHub Actions Workflows

1. **Daily Product Scraping** (`wayfair_scraper.yml`)
   - Runs daily at 00:00 UTC
   - Scrapes product listings from Wayfair
   - Output: `dat/wayfair_sofa_bs4_products.csv`

2. **Hourly Price Tracking** (`wayfair_price_tracking.yml`)
   - Runs every hour
   - Updates prices using Oxylabs API
   - Output: `dat/wayfair_price_tracking_YYYYMMDD_HHMM.csv`

## Setup

### Prerequisites
- GitHub account with repository
- Oxylabs API account

### Configuration
1. **Fork or clone this repository**

2. **Set GitHub Secrets**:
   - Go to Settings → Secrets and variables → Actions
   - Add: `OXYLAB_USERNAME` and `OXYLAB_PASSWORD`

3. **Enable Workflows**:
   - Go to Actions tab
   - Enable both workflows

## File Structure

```
├── src/
│   ├── wayfair_scrap.py              # Product scraping
│   ├── update_price.py               # Price tracking
│   └── *.ipynb                       # Analysis notebooks
├── dat/                              # Data storage
│   ├── wayfair_bs4_products.csv      # Product listings
│   └── wayfair_price_tracking_*.csv  # Price data
└── .github/workflows/                # GitHub Actions
```

## Data Output

### Product Listings
```csv
title,price,reviews,star_rating,url
"Product Name","$299.99","(150)",4.5,"https://wayfair.com/..."
```

### Price Tracking
```csv
timestamp,url,price,time_spent_sec
"2025-01-15 14:30:00","https://wayfair.com/...","$299.99",12.5
```

## Local Development

### Install Dependencies
```bash
pip install requests beautifulsoup4 pandas pytz playwright
playwright install
```

### Set Environment Variables
```bash
export OXYLAB_USERNAME="your_username"
export OXYLAB_PASSWORD="your_password"
```

### Run Scripts
```bash
python src/wayfair_scrap.py      # Scrape products
python src/update_price.py       # Track prices
```

## Customization

### Change Search Keywords
Edit `src/wayfair_scrap.py`:
```python
query = "desk"  # Change from "sofa"
pages = 50      # Adjust page count
```

### Track More Products
Edit `src/update_price.py`:
```python
urls = df['url'].tolist()[:20]  # Track 20 instead of 10
```

## Monitoring

- **GitHub Actions**: Check execution status in Actions tab
- **Data Files**: Review CSV files in `dat/` directory
- **Logs**: Check `dat/wayfair_scrape_log.txt`

## Troubleshooting

### Common Issues
1. **API Rate Limits**: Check Oxylabs quota
2. **Scraping Failures**: Verify website accessibility
3. **GitHub Actions Failures**: Check workflow logs

### Support
- Review GitHub Actions logs
- Check execution logs in `dat/` directory
- Verify API credentials

## License

MIT License 