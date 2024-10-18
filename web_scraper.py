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
9. Implements rate limiting to prevent overwhelming target websites

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
    -d, --delay DELAY         Set the delay between requests in seconds (default: 1.0)
                              The actual delay will be randomized between 0.5 * DELAY and 1.5 * DELAY

Dependencies:
    - scrapy
    - html2text
    - validators
    - beautifulsoup4
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
from bs4 import BeautifulSoup


def find_git_root(path: str) -> Optional[str]:
    """
    Find the root directory of the Git repository.

    This function attempts to locate the root directory of a Git repository
    by executing the 'git rev-parse --show-toplevel' command.

    Args:
        path (str): The starting path to search from.

    Returns:
        Optional[str]: The path to the Git root directory if found, None otherwise.
    """
    try:
        return subprocess.check_output(['git', 'rev-parse', '--show-toplevel'],
                                       cwd=path,
                                       stderr=subprocess.STDOUT).decode().strip()
    except subprocess.CalledProcessError:
        return None


def escape_gitignore_pattern(pattern: str) -> str:
    """
    Escape special characters in a gitignore pattern.

    This function escapes special characters (#, !, [, ]) in a gitignore pattern
    to ensure they are treated literally.

    Args:
        pattern (str): The gitignore pattern to escape.

    Returns:
        str: The escaped gitignore pattern.
    """
    return re.sub(r'([#!\[\]])', r'\\\1', pattern)


def update_gitignore(output_dir: str, negate: bool = False) -> None:
    """
    Update .gitignore file in the Git root directory to include the output directory.

    This function adds the output directory to the .gitignore file in the Git root directory.
    If the .gitignore file doesn't exist, it creates one.

    Args:
        output_dir (str): The output directory to add to .gitignore.
        negate (bool, optional): If True, negates the gitignore entry. Defaults to False.
    """
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
    """
    Read URLs from a file, one URL per line.

    This function reads a file containing URLs (one per line) and returns a list
    of valid URLs.

    Args:
        file_path (str): The path to the file containing URLs.

    Returns:
        List[str]: A list of valid URLs read from the file.
    """
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    return [url for url in urls if validators.url(url)]


def parse_size(size: str) -> int:
    """
    Parse a human-readable size string (e.g., '4GB') to bytes.

    This function converts a human-readable size string to its equivalent in bytes.
    It supports units B, KB, MB, GB, and TB.

    Args:
        size (str): A string representing a file size (e.g., '4GB', '100MB').

    Returns:
        int: The size in bytes.

    Raises:
        ValueError: If the size format is invalid.
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
    """
    A Scrapy spider for crawling websites and converting content to Markdown.

    This spider crawls specified URLs, converts HTML content to Markdown,
    and saves the results in a structured manner.
    """

    name = 'website_spider'
    handle_httpstatus_list = [404]  # Tell Scrapy to process 404 responses

    def __init__(self, start_urls: List[str], output_dir: str, ignore_links: bool = False,
                 subdir: Optional[str] = None, data_limit: Optional[int] = None,
                 combine_markdown: bool = False, *args, **kwargs):
        """
        Initialize the WebsiteSpider.

        Args:
            start_urls (List[str]): List of URLs to start crawling from.
            output_dir (str): Directory to save the scraped content.
            ignore_links (bool, optional): Whether to ignore links when converting to Markdown. Defaults to False.
            subdir (Optional[str], optional): Subdirectory to limit crawling to. Defaults to None.
            data_limit (Optional[int], optional): Limit on the amount of data to download. Defaults to None.
            combine_markdown (bool, optional): Whether to combine Markdown files per directory. Defaults to False.
        """
        super(WebsiteSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.allowed_domains = [urlparse(url).netloc for url in start_urls]
        self.output_dir = os.path.abspath(output_dir)
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = ignore_links
        self.h2t.body_width = 0  # Disable line wrapping
        self.sitemap: List[Tuple[str, str, str, str]] = []
        self.subdir = subdir
        self.original_url_path = urlparse(start_urls[0]).path
        self.data_limit = data_limit
        self.total_data_downloaded = 0
        self.combine_markdown = combine_markdown
        self.combined_content: Dict[str, str] = {}
        self.visited_urls: Set[str] = set()
        self.max_subdirectory_depth = 3  # Maximum depth for subdirectory attempts
        self.processed_urls: Set[str] = set()  # New: Track processed URLs

    def parse(self, response: Response):
        """
        Parse the response from a crawled URL.

        This method is called for each response downloaded from the web. It handles
        the main logic for processing the page, including checking data limits,
        handling 404 errors, and processing valid pages.

        Args:
            response (Response): The response object from Scrapy.

        Yields:
            Generator: May yield new requests to follow.
        """
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
        """
        Check if the data download limit has been reached.

        Returns:
            bool: True if the limit has been reached, False otherwise.
        """
        if self.data_limit and self.total_data_downloaded >= self.data_limit:
            self.logger.info("Data download limit reached. Stopping crawl.")
            return True
        return False

    def _is_valid_url(self, url: str) -> bool:
        """
        Check if the URL is valid and within the allowed scope.

        Args:
            url (str): The URL to check.

        Returns:
            bool: True if the URL is valid and within scope, False otherwise.
        """
        parsed_url = urlparse(url)
        current_path = parsed_url.path

        # Check if the URL is within the original domain and path
        if not current_path.startswith(self.original_url_path):
            return False

        # If subdir is specified, check if the URL is within the subdirectory
        if self.subdir:
            subdir_path = os.path.join(self.original_url_path, self.subdir.strip('/'))
            if not current_path.startswith(subdir_path):
                return False

        return True

    def _handle_404(self, response: Response):
        """
        Handle 404 errors by attempting to crawl subdirectories.

        This method tries to navigate up the URL path to find valid pages when a 404 is encountered.

        Args:
            response (Response): The 404 response object.

        Yields:
            Generator: New requests for potential valid URLs.
        """
        self.logger.info(f"Attempting to crawl subdirectories for: {response.url}")
        parsed_url = urlparse(response.url)
        path_parts = parsed_url.path.rstrip('/').split('/')
        
        for i in range(len(path_parts), 0, -1):
            new_path = '/'.join(path_parts[:i])
            new_url = parsed_url._replace(path=new_path).geturl()
            if new_url != response.url and new_url not in self.visited_urls and self._is_valid_url(new_url):
                self.visited_urls.add(new_url)
                yield scrapy.Request(new_url, callback=self.parse, dont_filter=True,
                                     meta={'depth': response.meta.get('depth', 0) + 1})
            
            if response.meta.get('depth', 0) >= self.max_subdirectory_depth:
                self.logger.info(f"Reached maximum subdirectory depth for {response.url}")
                break

    def _process_page(self, response: Response):
        """
        Process a successfully scraped page.

        This method handles the main logic for processing a valid page, including
        content extraction, Markdown conversion, and file saving.

        Args:
            response (Response): The response object for the scraped page.

        Yields:
            Generator: May yield new requests to follow links.
        """
        if response.url in self.processed_urls:
            self.logger.info(f"Skipping already processed URL: {response.url}")
            return

        self.processed_urls.add(response.url)

        markdown_content = self._extract_and_convert_content(response)
        file_path = self._create_file_path(response.url)
        
        if self.combine_markdown:
            self._add_to_combined_content(file_path, markdown_content, response.url)
        else:
            self._save_markdown_file(file_path, markdown_content)

        title = self._extract_title(response)
        self._update_sitemap(response.url, title, file_path)

        if not self.h2t.ignore_links:
            yield from self._follow_links(response)

    def _extract_and_convert_content(self, response: Response) -> str:
        """
        Extract main content from the response and convert it to Markdown.

        Args:
            response (Response): The response object containing the HTML content.

        Returns:
            str: The extracted content converted to Markdown.
        """
        soup = BeautifulSoup(response.body, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extract main content
        main_content = soup.find('main') or soup.find('article') or soup.find('body')
        
        if main_content:
            # Convert to string and then to Markdown
            html_content = str(main_content)
            markdown_content = self.h2t.handle(html_content)
            
            # Remove extra newlines and spaces
            markdown_content = re.sub(r'\n\s*\n', '\n\n', markdown_content)
            markdown_content = re.sub(r'^\s+', '', markdown_content, flags=re.MULTILINE)
            
            return f"Original page: {response.url}\n\n{markdown_content}"
        else:
            return f"Original page: {response.url}\n\nNo content found."

    def _create_file_path(self, url: str) -> str:
        """
        Create a file path for the Markdown file based on the URL.

        Args:
            url (str): The URL of the scraped page.

        Returns:
            str: The file path where the Markdown content will be saved.
        """
        domain = urlparse(url).netloc
        url_path = urlparse(url).path
        if url_path.endswith('/') or url_path == '':
            url_path += 'index'

        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        file_name = f"{os.path.basename(url_path)}_{url_hash}.md"
        return os.path.join(self.output_dir, domain, os.path.dirname(url_path.lstrip('/')), file_name)

    def _save_markdown_file(self, file_path: str, content: str) -> None:
        """
        Save the Markdown content to a file.

        Args:
            file_path (str): The path where the file should be saved.
            content (str): The Markdown content to save.
        """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _add_to_combined_content(self, file_path: str, content: str, url: str) -> None:
        """
        Add content to the combined markdown for the directory.

        This method is used when the combine_markdown option is enabled.

        Args:
            file_path (str): The file path for the individual Markdown file.
            content (str): The Markdown content to add.
            url (str): The URL of the original page.
        """
        directory = os.path.dirname(file_path)
        if directory not in self.combined_content:
            self.combined_content[directory] = ""
        
        # Add a clear separator and URL before the content
        self.combined_content[directory] += f"\n\n{'=' * 80}\n"
        self.combined_content[directory] += f"# {os.path.basename(file_path)}\n"
        self.combined_content[directory] += f"URL: {url}\n\n"
        self.combined_content[directory] += content

    def _extract_title(self, response: Response) -> str:
        """
        Extract the title from the page.

        Args:
            response (Response): The response object containing the HTML content.

        Returns:
            str: The extracted title or the basename of the URL if no title is found.
        """
        return response.css('title::text').get() or os.path.basename(response.url)

    def _update_sitemap(self, url: str, title: str, file_path: str) -> None:
        """
        Update the sitemap with the scraped page information.

        Args:
            url (str): The URL of the scraped page.
            title (str): The title of the page.
            file_path (str): The path where the Markdown file is saved.
        """
        domain = urlparse(url).netloc
        self.sitemap.append((domain, title, url, file_path))
        self.logger.info(f"Scraped: {url} -> {file_path}")

    def _follow_links(self, response: Response):
        """
        Follow links within the same domain and original URL path.

        This method is called when ignore_links is False.

        Args:
            response (Response): The response object containing the HTML content.

        Yields:
            Generator: New requests for links to follow.
        """
        domain = urlparse(response.url).netloc
        for href in response.css('a::attr(href)').getall():
            url = urljoin(response.url, href)
            if self._is_valid_url(url) and url not in self.visited_urls:
                self.visited_urls.add(url)
                yield scrapy.Request(url, callback=self.parse)

    def closed(self, reason):
        """
        Called when the spider is closed.

        This method handles final tasks such as saving combined Markdown files
        and creating the table of contents.

        Args:
            reason: The reason for closing the spider.
        """
        if self.combine_markdown:
            self._save_combined_markdown_files()
        self._create_table_of_contents()

    def _save_combined_markdown_files(self) -> None:
        """
        Save the combined markdown content for each directory.

        This method is called when the combine_markdown option is enabled.
        """
        for directory, content in self.combined_content.items():
            combined_file_path = os.path.join(directory, 'combined.md')
            os.makedirs(os.path.dirname(combined_file_path), exist_ok=True)
            with open(combined_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.logger.info(f"Saved combined markdown file: {combined_file_path}")

    def _create_table_of_contents(self) -> None:
        """
        Create a table of contents for the scraped content.

        This method generates a Markdown file containing a structured table of contents
        for all scraped pages.
        """
        toc_content = self._generate_toc_header()
        sorted_sitemap = sorted(self.sitemap, key=lambda x: (x[0], x[3]))
        toc_content += self._generate_toc_entries(sorted_sitemap)
        self._save_toc_file(toc_content)

    def _generate_toc_header(self) -> str:
        """
        Generate the header for the table of contents.

        Returns:
            str: The header content for the table of contents.
        """
        return """# Table of Contents

This table of contents provides an overview of all the pages scraped from the website(s). It is organized hierarchically to reflect the structure of the original site(s). You can use this table of contents to:

1. Navigate through the scraped content easily
2. Understand the overall structure of the website(s)
3. Quickly find specific pages or topics of interest

Each entry in the table of contents is a link to the corresponding Markdown file in the output directory. The indentation indicates the hierarchy of pages within the site structure.

---

"""

    def _generate_toc_entries(self, sorted_sitemap: List[Tuple[str, str, str, str]]) -> str:
        """
        Generate the entries for the table of contents.

        Args:
            sorted_sitemap (List[Tuple[str, str, str, str]]): A sorted list of sitemap entries.

        Returns:
            str: The generated table of contents entries.
        """
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
        """
        Save the table of contents to a file.

        Args:
            toc_content (str): The content of the table of contents.
        """
        toc_file_path = os.path.join(self.output_dir, 'table_of_contents.md')
        os.makedirs(os.path.dirname(toc_file_path), exist_ok=True)
        with open(toc_file_path, 'w', encoding='utf-8') as f:
            f.write(toc_content)


def main():
    """
    The main function to run the web scraper.

    This function parses command-line arguments, sets up logging,
    initializes the web scraper, and starts the crawling process.
    """
    parser = argparse.ArgumentParser(description='Scrape website(s) and convert to Markdown.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--url', help='The URL to scrape')
    group.add_argument('-f', '--file', help='File containing URLs to scrape (one per line)')
    parser.add_argument('-o', '--output', required=True, help='The directory to save the Markdown files')
    parser.add_argument('-i', '--ignore-links', action='store_true', help='Ignore links in the HTML when converting to Markdown')
    parser.add_argument('-a', '--user-agent', default='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', help='Set a custom user agent string')
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity')
    parser.add_argument('-s', '--subdir', help='Limit scraping to a specific subdirectory. Example: If you want to scrape only the "/docs" subdirectory from https://example.com, use "--subdir docs".')
    parser.add_argument('--data-download-limit', help='Limit the amount of data to download (e.g., 4GB). Note: This is a beta feature.')
    parser.add_argument('--combine-markdown', action='store_true', help='Combine markdown files per directory during scraping')
    parser.add_argument('-d', '--delay', type=float, default=1.0, help='Set the delay between requests in seconds (default: 1.0). The actual delay will be randomized between 0.5 * DELAY and 1.5 * DELAY')
    args = parser.parse_args()

    # Set up logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

    # Prepare output directory
    output_dir = os.path.abspath(args.output)
    os.makedirs(output_dir, exist_ok=True)

    # Update .gitignore
    update_gitignore(output_dir)

    # Prepare start URLs
    if args.file:
        start_urls = read_urls_from_file(args.file)
    else:
        start_urls = [args.url] if validators.url(args.url) else []

    if not start_urls:
        logging.error("Error: No valid URLs provided.")
        sys.exit(1)

    # Parse data download limit
    data_limit = None
    if args.data_download_limit:
        try:
            data_limit = parse_size(args.data_download_limit)
        except ValueError as e:
            logging.error(f"Error: {str(e)}")
            sys.exit(1)

    # Set up and start the Scrapy crawler
    process = CrawlerProcess({
        'USER_AGENT': args.user_agent,
        'LOG_LEVEL': 'DEBUG' if args.verbose else 'INFO',
        'DOWNLOAD_DELAY': args.delay,  # Add delay between requests
        'RANDOMIZE_DOWNLOAD_DELAY': True  # Randomize the delay
    })

    process.crawl(WebsiteSpider, start_urls=start_urls, output_dir=output_dir, ignore_links=args.ignore_links,
                  subdir=args.subdir, data_limit=data_limit, combine_markdown=args.combine_markdown)
    process.start()


if __name__ == "__main__":
    main()
