"""
Web Scraper Script

This script is designed to scrape a website and convert its content to Markdown format.
It uses Scrapy for web crawling and html2text for HTML to Markdown conversion.

The script performs the following main tasks:
1. Crawls a specified website, starting from the provided URL
2. Converts HTML content to Markdown
3. Saves each page as a separate Markdown file, maintaining the original site structure
4. Creates a table of contents for the scraped content
5. Adds the output directory to .gitignore in the Git root directory to prevent version control of scraped content

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
import subprocess

def find_git_root(path):
    """
    Find the root directory of the Git repository.
    
    Args:
        path (str): The starting path to search from

    Returns:
        str: The path to the Git root directory, or None if not found
    """
    try:
        git_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], 
                                           cwd=path, 
                                           stderr=subprocess.STDOUT).decode().strip()
        return git_root
    except subprocess.CalledProcessError:
        return None

def update_gitignore(output_dir):
    """
    Update .gitignore file in the Git root directory to include the output directory.
    
    Args:
        output_dir (str): The directory where scraped content is saved
    """
    current_dir = os.path.abspath(os.getcwd())
    git_root = find_git_root(current_dir)

    if git_root is None:
        print("Not a Git repository. Skipping .gitignore update.")
        return

    gitignore_path = os.path.join(git_root, '.gitignore')
    relative_output_dir = os.path.relpath(output_dir, git_root)
    gitignore_entry = f"{relative_output_dir}/"

    # Check if .gitignore exists, if not create it
    if not os.path.exists(gitignore_path):
        open(gitignore_path, 'a').close()

    # Read existing .gitignore content
    with open(gitignore_path, 'r') as file:
        content = file.read()

    # Check if the output directory is already in .gitignore
    if gitignore_entry not in content:
        # Append the output directory to .gitignore
        with open(gitignore_path, 'a') as file:
            file.write(f"\n# Scraped content\n{gitignore_entry}\n")
        print(f"Added {gitignore_entry} to .gitignore in {git_root}")
    else:
        print(f"{gitignore_entry} already in .gitignore")

class WebsiteSpider(scrapy.Spider):
    name = 'website_spider'

    def __init__(self, start_url=None, output_dir=None, *args, **kwargs):
        super(WebsiteSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.allowed_domains = [urlparse(start_url).netloc]
        self.output_dir = os.path.abspath(output_dir)
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False
        self.sitemap = []

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    def parse(self, response):
        try:
            # Extract main content
            main_content = response.css('main').get() or response.css('article').get() or response.css('body').get()

            # Convert HTML to Markdown
            markdown_content = self.h2t.handle(main_content)

            # Add original page link as documentation
            markdown_content = f"Original page: {response.url}\n\n{markdown_content}"

            # Create file path that mirrors the source site directory structure
            url_path = urlparse(response.url).path
            if url_path.endswith('/') or url_path == '':
                url_path += 'index'
            
            file_path = os.path.join(self.output_dir, url_path.lstrip('/').replace('.html', '.md'))

            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Write content to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            # Extract title from the page
            title = response.css('title::text').get() or os.path.basename(file_path)

            self.sitemap.append((title, response.url, file_path))
            self.logger.info(f"Scraped: {response.url} -> {file_path}")

            # Follow links within the same domain
            for href in response.css('a::attr(href)').getall():
                url = urljoin(response.url, href)
                if urlparse(url).netloc == self.allowed_domains[0]:
                    yield scrapy.Request(url, callback=self.parse)

        except Exception as e:
            self.logger.error(f"Error scraping {response.url}: {str(e)}")

    def closed(self, reason):
        self.create_table_of_contents()

    def create_table_of_contents(self):
        toc_content = """# Table of Contents

This table of contents provides an overview of all the pages scraped from the website. It is organized hierarchically to reflect the structure of the original site. You can use this table of contents to:

1. Navigate through the scraped content easily
2. Understand the overall structure of the website
3. Quickly find specific pages or topics of interest

Each entry in the table of contents is a link to the corresponding Markdown file in the output directory. The indentation indicates the hierarchy of pages within the site structure.

---

"""

        # Sort the sitemap by file path to group related pages together
        sorted_sitemap = sorted(self.sitemap, key=lambda x: x[2])

        for title, url, file_path in sorted_sitemap:
            relative_path = os.path.relpath(file_path, self.output_dir)
            parts = relative_path.split(os.sep)
            depth = len(parts) - 1
            indent = '  ' * depth
            toc_content += f"{indent}- [{title}]({relative_path})\n"

        toc_file_path = os.path.join(self.output_dir, 'table_of_contents.md')
        with open(toc_file_path, 'w', encoding='utf-8') as f:
            f.write(toc_content)

def main():
    parser = argparse.ArgumentParser(description='Scrape a website and convert to Markdown.')
    parser.add_argument('url', help='The URL to scrape')
    parser.add_argument('output_dir', help='The directory to save the Markdown files')
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Ensure output directory exists
    output_dir = os.path.abspath(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Update .gitignore
    update_gitignore(output_dir)

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'LOG_LEVEL': 'INFO'
    })

    process.crawl(WebsiteSpider, start_url=args.url, output_dir=output_dir)
    process.start()

if __name__ == "__main__":
    main()
