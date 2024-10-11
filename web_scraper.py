"""
Web Scraper Script

This script is designed to scrape websites and convert their content to Markdown format.
It uses Scrapy for web crawling and html2text for HTML to Markdown conversion.

Main features:
1. Crawls specified websites (single URL or multiple URLs from a file)
2. Converts HTML content to Markdown
3. Saves each page as a separate Markdown file, maintaining the original site structure
4. Creates a table of contents for the scraped content
5. Adds the output directory to .gitignore in the Git root directory
6. Implements secure coding practices, including input validation and sanitization

Usage:
    python web_scraper.py -u <url> -o <output_dir> [options]
    python web_scraper.py -f <url_file> -o <output_dir> [options]

Options:
    -u, --url URL             The URL to scrape
    -f, --file FILE           File containing URLs to scrape (one per line)
    -o, --output OUTPUT_DIR   The directory to save the Markdown files
    -i, --ignore-links        Ignore links in the HTML when converting to Markdown
    -a, --user-agent AGENT    Set a custom user agent string
    -v, --verbose             Increase output verbosity
    -s, --subdir SUBDIR       Limit scraping to a specific subdirectory
    --data-download-limit LIMIT Limit the amount of data to download (e.g., 4GB)
                              Note: This is a beta feature and may not work as expected

Dependencies:
    - scrapy
    - html2text
    - validators

This script is designed to be flexible and can be used for various web scraping tasks,
including documentation retrieval, content archiving, and offline reading preparation.
"""

import scrapy
from scrapy.crawler import CrawlerProcess
import html2text
import os
import argparse
from urllib.parse import urlparse, urljoin
import logging
import subprocess
import re
import sys
import hashlib
import validators

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

def escape_gitignore_pattern(pattern):
    """
    Escape special characters in a gitignore pattern.

    Args:
        pattern (str): The gitignore pattern to escape

    Returns:
        str: The escaped gitignore pattern
    """
    return re.sub(r'([#!\[\]])', r'\\\1', pattern)

def update_gitignore(output_dir, negate=False):
    """
    Update .gitignore file in the Git root directory to include the output directory.
    
    Args:
        output_dir (str): The directory where scraped content is saved
        negate (bool): Whether to negate the pattern (default: False)
    """
    current_dir = os.path.abspath(os.getcwd())
    git_root = find_git_root(current_dir)

    if git_root is None:
        print("Not a Git repository. Skipping .gitignore update.")
        return

    gitignore_path = os.path.join(git_root, '.gitignore')
    relative_output_dir = os.path.relpath(output_dir, git_root)
    gitignore_entry = escape_gitignore_pattern(f"{relative_output_dir}/")
    
    if negate:
        gitignore_entry = f"!{gitignore_entry}"

    if not os.path.exists(gitignore_path):
        open(gitignore_path, 'a').close()

    with open(gitignore_path, 'r+') as file:
        content = file.read()
        if gitignore_entry not in content:
            file.seek(0, 2)
            file.write(f"\n# Scraped content\n{gitignore_entry}\n")
            print(f"Added {gitignore_entry} to .gitignore in {git_root}")
        else:
            print(f"{gitignore_entry} already in .gitignore")

def read_urls_from_file(file_path):
    """
    Read URLs from a file, one URL per line.

    Args:
        file_path (str): Path to the file containing URLs

    Returns:
        list: List of valid URLs read from the file
    """
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    return [url for url in urls if validators.url(url)]

def parse_size(size):
    """
    Parse a human-readable size string (e.g., '4GB') to bytes.

    Args:
        size (str): A string representing a file size (e.g., '4GB', '100MB')

    Returns:
        int: The size in bytes

    Raises:
        ValueError: If the input string format is invalid
    """
    units = {
        'B': 1,
        'KB': 1024,
        'MB': 1024 ** 2,
        'GB': 1024 ** 3,
        'TB': 1024 ** 4
    }
    size = size.upper()
    match = re.match(r'^(\d+(\.\d+)?)\s*([B|KB|MB|GB|TB])$', size)
    if not match:
        raise ValueError("Invalid size format. Use something like '4GB' or '100MB'.")
    
    number = float(match.group(1))
    unit = match.group(3)
    return int(number * units[unit])

class WebsiteSpider(scrapy.Spider):
    name = 'website_spider'

    def __init__(self, start_urls, output_dir, ignore_links=False, subdir=None, data_limit=None, *args, **kwargs):
        super(WebsiteSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.allowed_domains = [urlparse(url).netloc for url in start_urls]
        self.output_dir = os.path.abspath(output_dir)
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = ignore_links
        self.sitemap = []
        self.subdir = subdir
        self.original_url_path = urlparse(start_urls[0]).path
        self.data_limit = data_limit
        self.total_data_downloaded = 0

    def parse(self, response):
        if self.data_limit and self.total_data_downloaded >= self.data_limit:
            self.logger.info(f"Data download limit reached. Stopping crawl.")
            return

        try:
            if not self.is_valid_url(response.url):
                return

            self.total_data_downloaded += len(response.body)

            markdown_content = self.extract_and_convert_content(response)
            file_path = self.create_file_path(response.url)
            self.save_markdown_file(file_path, markdown_content)

            title = self.extract_title(response)
            self.update_sitemap(response.url, title, file_path)

            if not self.h2t.ignore_links and (not self.data_limit or self.total_data_downloaded < self.data_limit):
                yield from self.follow_links(response)

        except Exception as e:
            self.logger.error(f"Error scraping {response.url}: {str(e)}")

    def is_valid_url(self, url):
        """Check if the URL is valid and within the allowed scope."""
        current_path = urlparse(url).path
        return (current_path.startswith(self.original_url_path) and
                (not self.subdir or current_path.startswith(self.subdir)))

    def extract_and_convert_content(self, response):
        """Extract main content and convert to Markdown."""
        main_content = response.css('main').get() or response.css('article').get() or response.css('body').get()
        markdown_content = self.h2t.handle(main_content)
        return f"Original page: {response.url}\n\n{markdown_content}"

    def create_file_path(self, url):
        """Create a file path for the Markdown file."""
        domain = urlparse(url).netloc
        url_path = urlparse(url).path
        if url_path.endswith('/') or url_path == '':
            url_path += 'index'
        
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        file_name = f"{os.path.basename(url_path)}_{url_hash}.md"
        return os.path.join(self.output_dir, domain, os.path.dirname(url_path.lstrip('/')), file_name)

    def save_markdown_file(self, file_path, content):
        """Save the Markdown content to a file."""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def extract_title(self, response):
        """Extract the title from the page."""
        return response.css('title::text').get() or os.path.basename(response.url)

    def update_sitemap(self, url, title, file_path):
        """Update the sitemap with the scraped page information."""
        domain = urlparse(url).netloc
        self.sitemap.append((domain, title, url, file_path))
        self.logger.info(f"Scraped: {url} -> {file_path}")

    def follow_links(self, response):
        """Follow links within the same domain and original URL path."""
        domain = urlparse(response.url).netloc
        for href in response.css('a::attr(href)').getall():
            url = urljoin(response.url, href)
            parsed_url = urlparse(url)
            if parsed_url.netloc == domain and parsed_url.path.startswith(self.original_url_path):
                yield scrapy.Request(url, callback=self.parse)

    def closed(self, reason):
        self.create_table_of_contents()

    def create_table_of_contents(self):
        """Create a table of contents for the scraped content."""
        toc_content = self.generate_toc_header()
        sorted_sitemap = sorted(self.sitemap, key=lambda x: (x[0], x[3]))
        toc_content += self.generate_toc_entries(sorted_sitemap)
        self.save_toc_file(toc_content)

    def generate_toc_header(self):
        """Generate the header for the table of contents."""
        return """# Table of Contents

This table of contents provides an overview of all the pages scraped from the website(s). It is organized hierarchically to reflect the structure of the original site(s). You can use this table of contents to:

1. Navigate through the scraped content easily
2. Understand the overall structure of the website(s)
3. Quickly find specific pages or topics of interest

Each entry in the table of contents is a link to the corresponding Markdown file in the output directory. The indentation indicates the hierarchy of pages within the site structure.

---

"""

    def generate_toc_entries(self, sorted_sitemap):
        """Generate the entries for the table of contents."""
        toc_content = ""
        current_domain = None
        for domain, title, url, file_path in sorted_sitemap:
            if domain != current_domain:
                toc_content += f"\n## {domain}\n\n"
                current_domain = domain

            relative_path = os.path.relpath(file_path, self.output_dir)
            depth = len(relative_path.split(os.sep)) - 2
            indent = '  ' * depth
            toc_content += f"{indent}- [{title}]({relative_path})\n"
        return toc_content

    def save_toc_file(self, toc_content):
        """Save the table of contents to a file."""
        toc_file_path = os.path.join(self.output_dir, 'table_of_contents.md')
        os.makedirs(os.path.dirname(toc_file_path), exist_ok=True)
        with open(toc_file_path, 'w', encoding='utf-8') as f:
            f.write(toc_content)

def main():
    parser = argparse.ArgumentParser(description='Scrape website(s) and convert to Markdown.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--url', help='The URL to scrape')
    group.add_argument('-f', '--file', help='File containing URLs to scrape (one per line)')
    parser.add_argument('-o', '--output', required=True, help='The directory to save the Markdown files')
    parser.add_argument('-i', '--ignore-links', action='store_true', help='Ignore links in the HTML when converting to Markdown')
    parser.add_argument('-a', '--user-agent', default='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', help='Set a custom user agent string')
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity')
    parser.add_argument('-s', '--subdir', help='Limit scraping to a specific subdirectory')
    parser.add_argument('--data-download-limit', help='Limit the amount of data to download (e.g., 4GB). Note: This is a beta feature.')
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

    output_dir = os.path.abspath(args.output)
    os.makedirs(output_dir, exist_ok=True)

    update_gitignore(output_dir)

    if args.file:
        start_urls = read_urls_from_file(args.file)
    else:
        start_urls = [args.url] if validators.url(args.url) else []

    if not start_urls:
        print("Error: No valid URLs provided.", file=sys.stderr)
        sys.exit(1)

    data_limit = None
    if args.data_download_limit:
        try:
            data_limit = parse_size(args.data_download_limit)
        except ValueError as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            sys.exit(1)

    process = CrawlerProcess({
        'USER_AGENT': args.user_agent,
        'LOG_LEVEL': 'DEBUG' if args.verbose else 'INFO'
    })

    process.crawl(WebsiteSpider, start_urls=start_urls, output_dir=output_dir, ignore_links=args.ignore_links, subdir=args.subdir, data_limit=data_limit)
    process.start()

if __name__ == "__main__":
    main()
