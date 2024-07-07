import requests
import json
import os
import time

def read_visited_urls(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

def scrape_with_scrapfly(url, api_key):
    scrapfly_url = f"https://api.scrapfly.io/scrape?tags=player%2Cproject%3Atest&country=ru&asp=true&cost_budget=10&render_js=true&key={api_key}&url={url}"

    response = requests.request("GET", scrapfly_url)
    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    data = response.json()
    return data

def save_results(results, file_path):
    with open(file_path, 'w') as file:
        json.dump(results, file, indent=4)

def download_file(url, content):
    filename = url.split('/')[-1]
    with open(filename, 'wb') as file:
        file.write(content)

def download_file_with_retry(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            return response.content
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
    raise Exception(f"Failed to download file from {url} after {retries} attempts")

def main():
    api_key = ""  # Replace with your Scrapfly API key
    visited_urls = read_visited_urls('/myproject/spiders/found_paths.txt') # will need to change this to your proper path
    results = []

    for url in visited_urls:
        print(f"Scraping URL: {url}")
        try:
            data = scrape_with_scrapfly(url, api_key)
            if data:  # Ensure the response is not None
                results.append({
                    "url": url,
                    "result": data['result']
                })

                # Check if the content is a file
                if 'file' in data.get('tags', []):
                    file_url = data['result']['url']
                    file_content = download_file_with_retry(file_url)
                    download_file(file_url, file_content)
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    save_results(results, 'scrapfly_results.json') # may want to adjust path for saving

if __name__ == "__main__":
    main()
