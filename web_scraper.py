"""
Web Scraper Script

This script is designed to scrape a website and convert its content to Markdown format.
It uses Scrapy for web crawling and html2text for HTML to Markdown conversion.

The script performs the following main tasks:
1. Crawls a specified website, focusing on the /docs directory
2. Converts HTML content to Markdown
3. Saves each page as a separate Markdown file, maintaining the original site structure
4. Creates a table of contents for the scraped content

Usage:
    python web_scraper.py <url> <output_dir>

    <url>: The URL of the website to scrape
    <output_dir>: The directory where the Markdown files will be saved

Dependencies:
    - scrapy
    - html2text
"""

import scrapy
from scrapy.crawler import CrawlerProcess
import html2text
import os
import argparse
from urllib.parse import urlparse, urljoin
import logging
import time

class WebsiteSpider(scrapy.Spider):
    """
    Spider class for crawling a website and converting its content to Markdown.

    This spider crawls a specified website, converts HTML content to Markdown,
    and saves each page as a separate file while maintaining the original site structure.
    """

    name = 'website_spider'

    def __init__(self, start_url=None, output_dir=None, *args, **kwargs):
        """
        Initialize the WebsiteSpider.

        Args:
            start_url (str): The URL to start crawling from
            output_dir (str): The directory to save the Markdown files
        """
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
        """
        Parse the response from each crawled page.

        This method handles the conversion of HTML to Markdown, saves the content,
        and follows links within the allowed domain and /docs directory.

        Args:
            response (scrapy.http.Response): The response object from the crawled page
        """
        current_time = time.time()
        if current_time - self.last_request_time < self.request_delay:
            time.sleep(self.request_delay - (current_time - self.last_request_time))
        self.last_request_time = time.time()

        # Only process pages within the /docs directory
        if not response.url.startswith(self.start_urls[0]):
            return

        try:
            # Extract main content (adjust selectors based on the website structure)
            main_content = response.css('main').get()
            if not main_content:
                main_content = response.css('article').get()
            if not main_content:
                main_content = response.css('body').get()

            # Convert HTML to Markdown
            markdown_content = self.h2t.handle(main_content)

            # Add original page link as documentation
            markdown_content = f"Original page: {response.url}\n\n{markdown_content}"

            # Create file path that mirrors the source site directory structure
            url_path = urlparse(response.url).path
            if url_path.endswith('/'):
                url_path += 'index'
            
            # Remove the '/docs' prefix from the path
            relative_path = url_path.replace('/docs/', '', 1)
            
            # Construct the full file path
            file_path = os.path.join(self.output_dir, relative_path + '.md')

            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Write content to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            # Extract title from the page
            title = response.css('title::text').get() or os.path.basename(file_path)

            self.sitemap.append((title, response.url, file_path))
            logging.info(f"Scraped: {response.url}")

            # Follow links within the allowed domain and /docs directory
            for href in response.css('a::attr(href)').getall():
                url = urljoin(response.url, href)
                if url.startswith(self.start_urls[0]):
                    yield scrapy.Request(url, callback=self.parse)

        except Exception as e:
            logging.error(f"Error scraping {response.url}: {str(e)}")

    def closed(self, reason):
        """
        Method called when the spider is closed.

        This method is responsible for creating the table of contents after all pages have been scraped.

        Args:
            reason (str): The reason for closing the spider
        """
        self.create_table_of_contents()

    def create_table_of_contents(self):
        """
        Create a table of contents for the scraped content.

        This method generates a Markdown file containing a hierarchical table of contents
        based on the scraped pages and their file structure.
        """
        toc_content = "# Table of Contents\n\n"

        # Sort the sitemap by file path to group related pages together
        sorted_sitemap = sorted(self.sitemap, key=lambda x: x[2])

        current_path = []
        for title, url, file_path in sorted_sitemap:
            relative_path = os.path.relpath(file_path, self.output_dir)
            parts = relative_path.split(os.sep)

            # Determine the depth of the current item
            depth = len(parts) - 1

            # Update the current path
            current_path = current_path[:depth]
            while len(current_path) < depth:
                current_path.append('')

            current_path.append(parts[-1])

            # Create the indentation
            indent = '  ' * depth

            # Add the item to the table of contents
            toc_content += f"{indent}- [{title}]({relative_path})\n"

        with open(os.path.join(self.output_dir, 'table_of_contents.md'), 'w', encoding='utf-8') as f:
            f.write(toc_content)

def main():
    """
    Main function to set up and run the web scraper.

    This function parses command-line arguments, sets up logging,
    and initializes the Scrapy crawler process.
    """
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
