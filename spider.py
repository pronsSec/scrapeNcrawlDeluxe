import scrapy
import cloudscraper
from scrapy.crawler import CrawlerProcess

class LinkSpider(scrapy.Spider):
    name = 'link_spider'
    start_urls = ['https://example.org']  # replace with your target website
    allowed_domains = ['example.org']

    def __init__(self, *args, **kwargs):
        super(LinkSpider, self).__init__(*args, **kwargs)
        self.scraper = cloudscraper.create_scraper()  # use cloudscraper to bypass Cloudflare
        self.visited_urls = set()
        self.found_paths = set()

    def parse(self, response):
        # Extract all links on the page
        links = response.css('a::attr(href)').getall()
        for link in links:
            # Ensure the link has a scheme (http/https)
            if link.startswith('//'):
                link = response.urljoin('http:' + link)
            elif link.startswith('/'):
                link = response.urljoin(link)
            elif not link.startswith('http'):
                link = response.urljoin('/' + link)
                
            if link not in self.visited_urls and self.is_allowed_domain(link):
                self.visited_urls.add(link)
                yield scrapy.Request(url=link, callback=self.parse)

        # Check if the response is blocked by Cloudflare
        if b'Attention Required! | Cloudflare' in response.body:
            self.found_paths.add(response.url)
            self.log(f'Blocked by Cloudflare: {response.url}')
        elif response.status != 404:
            self.found_paths.add(response.url)
            self.log(f'Found path: {response.url}')

    def is_allowed_domain(self, url):
        return any(domain in url for domain in self.allowed_domains)

    def closed(self, reason):
        # Write found paths to a text file
        with open('found_paths.txt', 'w') as f:
            for path in sorted(self.found_paths):
                f.write(path + '\n')

if __name__ == '__main__':
    process = CrawlerProcess(settings={
        'LOG_LEVEL': 'INFO',
    })
    process.crawl(LinkSpider)
    process.start()
