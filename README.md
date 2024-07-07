# scrapeNcrawlDeluxe
---


# Steps to run spider crawl and scrapes with Scrapfly


## Prerequisites

1. Python 3.x installed
2. Required Python packages installed:
   - `requests`
   - `scrapy`

## Steps

### 1. Set Up the Scrapy Project and Spider

1. **Install Scrapy**:
   ```bash
   pip install scrapy
   ```

2. **Create a Scrapy Project**:
   ```bash
   scrapy startproject myproject
   ```

3. **Navigate to the Project Directory**:
   ```bash
   cd myproject
   ```

4. **Create the Spider**:
   - Navigate to the `spiders` directory:
     ```bash
     cd myproject/spiders
     ```
   - Create a new file for the spider, e.g., `link_spider.py`, and add the spider code provided in spider.py

5. **Return to the Project Root Directory**:
   ```bash
   cd ../..
   ```

6. **Run the Spider**:
   ```bash
   scrapy crawl link_spider
   ```

7. **Ensure the Spider Output**:
   - Confirm that `found_paths.txt` is created in the project directory with the list of URLs.

### 2. Set Up and Run the Scrapfly Script

1. **Install Required Packages**:
   ```bash
   pip install requests
   ```

2. **Create the Scrapfly Script**:
   - Create a new file in the project directory, e.g., `scrapfly_scraper.py`, and add the provided script code from scrape.py

3. **Configure Your Scrapfly API Key**:
   - Replace the placeholder in the script with your Scrapfly API key:
     ```python
     api_key = "your_scrapfly_api_key_here"
     ```

4. **Run the Scrapfly Script**:
   ```bash
   python scrapfly_scraper.py
   ```

5. **Check the Results**:
   - Confirm that `scrapfly_results.json` is created with the scraping results.
   - Verify that downloaded files are saved in the project directory.

## Additional Notes

- Ensure your API key has sufficient permissions and budget for the number of requests you plan to make.
- Handle sensitive information like API keys securely and avoid hardcoding them in public repositories.

For further customization and troubleshooting, refer to the official documentation of the libraries and APIs used.
```
