import scrapy
from scrapy.crawler import CrawlerProcess
import html2text
import os
import argparse
from urllib.parse import urlparse, urljoin
import logging
import time

class WebsiteSpider(scrapy.Spider):
    name = 'website_spider'

    def __init__(self, start_url=None, output_dir=None, *args, **kwargs):
        super(WebsiteSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.allowed_domains = [urlparse(start_url).netloc]
        self.output_dir = output_dir
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False
        self.sitemap = []
        self.last_request_time = time.time()
        self.request_delay = 1  # Delay between requests in seconds

    def parse(self, response):
        current_time = time.time()
        if current_time - self.last_request_time < self.request_delay:
            time.sleep(self.request_delay - (current_time - self.last_request_time))
        self.last_request_time = time.time()

        try:
            # Extract main content (adjust selectors based on the website structure)
            main_content = response.css('main').get()
            if not main_content:
                main_content = response.css('article').get()
            if not main_content:
                main_content = response.css('body').get()

            # Convert HTML to Markdown
            markdown_content = self.h2t.handle(main_content)

            # Create file path
            url_path = urlparse(response.url).path
            if url_path.endswith('/'):
                url_path += 'index'
            file_path = os.path.join(self.output_dir, url_path.lstrip('/') + '.md')

            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Write content to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            self.sitemap.append((response.url, file_path))
            logging.info(f"Scraped: {response.url}")

            # Follow links within the allowed domain
            for href in response.css('a::attr(href)').getall():
                url = urljoin(response.url, href)
                if urlparse(url).netloc in self.allowed_domains:
                    yield scrapy.Request(url, callback=self.parse)

        except Exception as e:
            logging.error(f"Error scraping {response.url}: {str(e)}")

    def closed(self, reason):
        self.create_sitemap()

    def create_sitemap(self):
        sitemap_content = "# Site Map\n\n"
        for url, file_path in self.sitemap:
            relative_path = os.path.relpath(file_path, self.output_dir)
            sitemap_content += f"- [{url}]({relative_path})\n"

        with open(os.path.join(self.output_dir, 'sitemap.md'), 'w', encoding='utf-8') as f:
            f.write(sitemap_content)

def main():
    parser = argparse.ArgumentParser(description='Scrape a website and convert to Markdown.')
    parser.add_argument('url', help='The URL to scrape')
    parser.add_argument('output_dir', help='The directory to save the Markdown files')
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'LOG_LEVEL': 'ERROR'  # Only log errors from Scrapy
    })

    process.crawl(WebsiteSpider, start_url=args.url, output_dir=args.output_dir)
    process.start()

if __name__ == "__main__":
    main()
