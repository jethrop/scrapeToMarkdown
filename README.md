# Web Scraper

This Python script is designed to scrape websites and convert their content to Markdown format. It uses Scrapy for web crawling and html2text for HTML to Markdown conversion.

## Features

1. Crawls specified websites (single URL or multiple URLs from a file)
2. Converts HTML content to Markdown
3. Saves each page as a separate Markdown file, maintaining the original site structure
4. Creates a table of contents for the scraped content
5. Adds the output directory to .gitignore in the Git root directory
6. Implements secure coding practices including input validation and sanitization

## Requirements

- Python 3.7+
- scrapy
- html2text
- validators

Install the required packages using:

```
pip install -r requirements.txt
```

## Usage

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

## Examples

1. Scrape a single URL:
   ```
   python web_scraper.py -u https://example.com -o scraped_content
   ```

2. Scrape multiple URLs from a file:
   ```
   python web_scraper.py -f urls.txt -o scraped_content
   ```

3. Scrape with a 100MB data limit and custom user agent:
   ```
   python web_scraper.py -u https://example.com -o scraped_content --data-download-limit 100MB -a "MyBot/1.0"
   ```

## Output

The script creates a directory structure mirroring the scraped website(s) and saves each page as a separate Markdown file. It also generates a `table_of_contents.md` file in the output directory, providing an overview of all scraped pages.

## Security Considerations

- The script implements input validation to ensure only valid URLs are processed.
- It uses the `validators` library to verify URL integrity.
- The script sanitizes file paths to prevent directory traversal attacks.
- It limits scraping to the specified domain and subdirectory (if provided) to prevent unintended access to other parts of the website.

## Limitations

- The data download limit feature is in beta and may not work as expected in all scenarios.
- The script does not handle JavaScript-rendered content, as it relies on Scrapy's static HTML parsing.

## Contributing

Contributions to improve the script are welcome. Please ensure that any pull requests maintain or improve the existing security measures and code quality.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
