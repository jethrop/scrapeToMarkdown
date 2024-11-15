# Web Scraper to Markdown

This Python script is designed to scrape websites and convert their content to Markdown format. It uses Scrapy for web crawling and html2text for HTML to Markdown conversion. The application provides both a command-line interface and a user-friendly GUI. This is primarily for documentation sites so you can feed docs directly to an llm.

## Features

1. Crawls specified websites (single URL or multiple URLs from a file)
2. Converts HTML content to Markdown
3. Saves each page as a separate Markdown file, maintaining the original site structure
4. Creates a table of contents for the scraped content
5. Adds the output directory to .gitignore in the Git root directory
6. Implements secure coding practices including input validation and sanitization
7. Option to combine markdown files per directory during scraping
8. Handles 404 errors by attempting to crawl deeper into the directory structure
9. Implements rate limiting to prevent overwhelming target websites
10. Provides both CLI and GUI interfaces for ease of use
11. Verbose inline documentation for improved code readability and maintainability

## Requirements

- Python 3.7+
- scrapy
- html2text
- validators
- beautifulsoup4
- typing
- nicegui

Install the required packages using:

```
pip install -r requirements.txt
```

## Usage

### GUI Interface

To launch the graphical user interface:

```
python gui.py
```

The GUI provides an intuitive interface with:
- Text area for entering URLs (one per line)
- Output directory selection
- Various options including:
  - Ignore links toggle
  - Verbose output toggle
  - Combine markdown files toggle
  - Delay between requests
  - Custom user agent
  - Subdirectory limitation
  - Data download limit
- Real-time status updates
- Start/Clear buttons

### Command Line Interface

```
python web_scraper.py -u <url> -o <output_dir> [options]
python web_scraper.py -f <url_file> -o <output_dir> [options]
```

### Options

- `-u`, `--url` URL: The URL to scrape
- `-f`, `--file` FILE: File containing URLs to scrape (one per line)
- `-o`, `--output` OUTPUT_DIR: The directory to save the Markdown files
- `-i`, `--ignore-links`: Ignore links in the HTML when converting to Markdown
- `-a`, `--user-agent` AGENT: Set a custom user agent string
- `-v`, `--verbose`: Increase output verbosity
- `-s`, `--subdir` SUBDIR: Limit scraping to a specific subdirectory
- `--data-download-limit` LIMIT: Limit the amount of data to download (e.g., 4GB)
- `--combine-markdown`: Combine markdown files per directory during scraping
- `-d`, `--delay` DELAY: Set the delay between requests in seconds (default: 1.0)

## Examples

1. Using the GUI:
   ```
   python gui.py
   ```

2. Scrape a single URL via CLI:
   ```
   python web_scraper.py -u https://example.com -o scraped_content
   ```

3. Scrape multiple URLs from a file:
   ```
   python web_scraper.py -f urls.txt -o scraped_content
   ```

4. Scrape with a 100MB data limit and custom user agent:
   ```
   python web_scraper.py -u https://example.com -o scraped_content --data-download-limit 100MB -a "MyBot/1.0"
   ```

5. Scrape and combine markdown files per directory:
   ```
   python web_scraper.py -u https://example.com -o scraped_content --combine-markdown
   ```

6. Scrape with a custom delay between requests:
   ```
   python web_scraper.py -u https://example.com -o scraped_content -d 2.0
   ```

## Output

The script creates a directory structure mirroring the scraped website(s) and saves each page as a separate Markdown file. It also generates a `table_of_contents.md` file in the output directory, providing an overview of all scraped pages. If the `--combine-markdown` option is used, it will also create a `combined.md` file in each directory containing all the markdown content for that directory.

## Security Considerations

- The script implements input validation to ensure only valid URLs are processed.
- It uses the `validators` library to verify URL integrity.
- The script sanitizes file paths to prevent directory traversal attacks.
- It limits scraping to the specified domain and subdirectory (if provided) to prevent unintended access to other parts of the website.
- Rate limiting is implemented to prevent overwhelming target websites.

## Limitations/Issues
- The data download limit feature is in beta and may not work as expected in all scenarios.
- The script does not handle JavaScript-rendered content, as it relies on Scrapy's static HTML parsing.
- The combined feature works. However, some websites (like https://supabase.com/docs/reference/javascript/installing) have a directory structure that actually all points to the same document. This causes the script to download the same document multiple times. This is a limitation of the script and not a bug.
- The output may contain some formatting inconsistencies due to the HTML to Markdown conversion process.

## Recent Changes
- Added graphical user interface using NiceGUI
- Added option to combine markdown files per directory during scraping
- Implemented handling of 404 errors by attempting to crawl deeper into the directory structure
- Added verbose inline documentation to improve code readability and maintainability
- Implemented rate limiting to prevent overwhelming target websites

## Contributing

Contributions to improve the script are welcome. Please ensure that any pull requests maintain or improve the existing security measures and code quality.

## License

This project is licensed under the GNU AGPLv3 License - see the [LICENSE](https://choosealicense.com/licenses/agpl-3.0/) file for details.
