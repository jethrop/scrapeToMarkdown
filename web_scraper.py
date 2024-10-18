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
6. Implements secure coding practices including input validation and sanitization
7. Option to combine markdown files per directory during scraping
8. Handles 404 errors by attempting to crawl deeper into the directory structure

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
    --combine-markdown        Combine markdown files per directory during scraping

Dependencies:
    - scrapy
    - html2text
    - validators
"""

import os
import sys
import re
import hashlib
import logging
import argparse
import subprocess
from typing import List, Tuple, Optional, Dict, Set
from urllib.parse import urlparse, urljoin

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import Response
import html2text
import validators


def find_git_root(path: str) -> Optional[str]:
    """Find the root directory of the Git repository."""
    try:
        return subprocess.check_output(['git', 'rev-parse', '--show-toplevel'],
                                       cwd=path,
                                       stderr=subprocess.STDOUT).decode().strip()
    except subprocess.CalledProcessError:
        return None


def escape_gitignore_pattern(pattern: str) -> str:
    """Escape special characters in a gitignore pattern."""
    return re.sub(r'([#!\[\]])', r'\\\1', pattern)


def update_gitignore(output_dir: str, negate: bool = False) -> None:
    """Update .gitignore file in the Git root directory to include the output directory."""
    current_dir = os.path.abspath(os.getcwd())
    git_root = find_git_root(current_dir)

    if git_root is None:
        logging.warning("Not a Git repository. Skipping .gitignore update.")
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
            logging.info(f"Added {gitignore_entry} to .gitignore in {git_root}")
        else:
            logging.info(f"{gitignore_entry} already in .gitignore")


def read_urls_from_file(file_path: str) -> List[str]:
    """Read URLs from a file, one URL per line."""
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    return [url for url in urls if validators.url(url)]


def parse_size(size: str) -> int:
    """Parse a human-readable size string (e.g., '4GB') to bytes."""
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
    handle_httpstatus_list = [404]  # Tell Scrapy to process 404 responses

    def __init__(self, start_urls: List[str], output_dir: str, ignore_links: bool = False,
                 subdir: Optional[str] = None, data_limit: Optional[int] = None,
                 combine_markdown: bool = False, *args, **kwargs):
        super(WebsiteSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.allowed_domains = [urlparse(url).netloc for url in start_urls]
        self.output_dir = os.path.abspath(output_dir)
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = ignore_links
        self.sitemap: List[Tuple[str, str, str, str]] = []
        self.subdir = subdir
        self.original_url_path = urlparse(start_urls[0]).path
        self.data_limit = data_limit
        self.total_data_downloaded = 0
        self.combine_markdown = combine_markdown
        self.combined_content: Dict[str, str] = {}
        self.visited_urls: Set[str] = set()
        self.max_subdirectory_depth = 3  # Maximum depth for subdirectory attempts

    def parse(self, response: Response):
        if self._check_data_limit():
            return

        try:
            if not self._is_valid_url(response.url):
                return

            self.total_data_downloaded += len(response.body)

            if response.status == 404:
                self.logger.info(f"Encountered 404 for {response.url}")
                yield from self._handle_404(response)
            else:
                yield from self._process_page(response)

        except Exception as e:
            self.logger.error(f"Error scraping {response.url}: {str(e)}")

    def _check_data_limit(self) -> bool:
        """Check if the data download limit has been reached."""
        if self.data_limit and self.total_data_downloaded >= self.data_limit:
            self.logger.info("Data download limit reached. Stopping crawl.")
            return True
        return False

    def _is_valid_url(self, url: str) -> bool:
        """Check if the URL is valid and within the allowed scope."""
        current_path = urlparse(url).path
        return (current_path.startswith(self.original_url_path) and
                (not self.subdir or current_path.startswith(self.subdir)))

    def _handle_404(self, response: Response):
        """Handle 404 errors by attempting to crawl subdirectories."""
        self.logger.info(f"Attempting to crawl subdirectories for: {response.url}")
        parsed_url = urlparse(response.url)
        path_parts = parsed_url.path.rstrip('/').split('/')
        
        for i in range(len(path_parts), 0, -1):
            new_path = '/'.join(path_parts[:i])
            new_url = parsed_url._replace(path=new_path).geturl()
            if new_url != response.url and new_url not in self.visited_urls:
                self.visited_urls.add(new_url)
                yield scrapy.Request(new_url, callback=self.parse, dont_filter=True,
                                     meta={'depth': response.meta.get('depth', 0) + 1})
            
            if response.meta.get('depth', 0) >= self.max_subdirectory_depth:
                self.logger.info(f"Reached maximum subdirectory depth for {response.url}")
                break

    def _process_page(self, response: Response):
        """Process a successfully scraped page."""
        markdown_content = self._extract_and_convert_content(response)
        file_path = self._create_file_path(response.url)
        
        if self.combine_markdown:
            self._add_to_combined_content(file_path, markdown_content)
        else:
            self._save_markdown_file(file_path, markdown_content)

        title = self._extract_title(response)
        self._update_sitemap(response.url, title, file_path)

        if not self.h2t.ignore_links:
            yield from self._follow_links(response)

    def _extract_and_convert_content(self, response: Response) -> str:
        """Extract main content and convert to Markdown."""
        main_content = response.css('main').get() or response.css('article').get() or response.css('body').get()
        markdown_content = self.h2t.handle(main_content)
        return f"Original page: {response.url}\n\n{markdown_content}"

    def _create_file_path(self, url: str) -> str:
        """Create a file path for the Markdown file."""
        domain = urlparse(url).netloc
        url_path = urlparse(url).path
        if url_path.endswith('/') or url_path == '':
            url_path += 'index'

        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        file_name = f"{os.path.basename(url_path)}_{url_hash}.md"
        return os.path.join(self.output_dir, domain, os.path.dirname(url_path.lstrip('/')), file_name)

    def _save_markdown_file(self, file_path: str, content: str) -> None:
        """Save the Markdown content to a file."""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _add_to_combined_content(self, file_path: str, content: str) -> None:
        """Add content to the combined markdown for the directory."""
        directory = os.path.dirname(file_path)
        if directory not in self.combined_content:
            self.combined_content[directory] = ""
        self.combined_content[directory] += f"\n\n# {os.path.basename(file_path)}\n\n{content}"

    def _extract_title(self, response: Response) -> str:
        """Extract the title from the page."""
        return response.css('title::text').get() or os.path.basename(response.url)

    def _update_sitemap(self, url: str, title: str, file_path: str) -> None:
        """Update the sitemap with the scraped page information."""
        domain = urlparse(url).netloc
        self.sitemap.append((domain, title, url, file_path))
        self.logger.info(f"Scraped: {url} -> {file_path}")

    def _follow_links(self, response: Response):
        """Follow links within the same domain and original URL path."""
        domain = urlparse(response.url).netloc
        for href in response.css('a::attr(href)').getall():
            url = urljoin(response.url, href)
            parsed_url = urlparse(url)
            if parsed_url.netloc == domain and parsed_url.path.startswith(self.original_url_path):
                if url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse)

    def closed(self, reason):
        if self.combine_markdown:
            self._save_combined_markdown_files()
        self._create_table_of_contents()

    def _save_combined_markdown_files(self) -> None:
        """Save the combined markdown content for each directory."""
        for directory, content in self.combined_content.items():
            combined_file_path = os.path.join(directory, 'combined.md')
            os.makedirs(os.path.dirname(combined_file_path), exist_ok=True)
            with open(combined_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.logger.info(f"Saved combined markdown file: {combined_file_path}")

    def _create_table_of_contents(self) -> None:
        """Create a table of contents for the scraped content."""
        toc_content = self._generate_toc_header()
        sorted_sitemap = sorted(self.sitemap, key=lambda x: (x[0], x[3]))
        toc_content += self._generate_toc_entries(sorted_sitemap)
        self._save_toc_file(toc_content)

    def _generate_toc_header(self) -> str:
        """Generate the header for the table of contents."""
        return """# Table of Contents

This table of contents provides an overview of all the pages scraped from the website(s). It is organized hierarchically to reflect the structure of the original site(s). You can use this table of contents to:

1. Navigate through the scraped content easily
2. Understand the overall structure of the website(s)
3. Quickly find specific pages or topics of interest

Each entry in the table of contents is a link to the corresponding Markdown file in the output directory. The indentation indicates the hierarchy of pages within the site structure.

---

"""

    def _generate_toc_entries(self, sorted_sitemap: List[Tuple[str, str, str, str]]) -> str:
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

    def _save_toc_file(self, toc_content: str) -> None:
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
    parser.add_argument('--combine-markdown', action='store_true', help='Combine markdown files per directory during scraping')
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
        logging.error("Error: No valid URLs provided.")
        sys.exit(1)

    data_limit = None
    if args.data_download_limit:
        try:
            data_limit = parse_size(args.data_download_limit)
        except ValueError as e:
            logging.error(f"Error: {str(e)}")
            sys.exit(1)

    process = CrawlerProcess({
        'USER_AGENT': args.user_agent,
        'LOG_LEVEL': 'DEBUG' if args.verbose else 'INFO'
    })

    process.crawl(WebsiteSpider, start_urls=start_urls, output_dir=output_dir, ignore_links=args.ignore_links,
                  subdir=args.subdir, data_limit=data_limit, combine_markdown=args.combine_markdown)
    process.start()


if __name__ == "__main__":
    main()
