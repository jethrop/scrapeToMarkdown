# Web Scraper to Markdown Converter

This project contains a Python script that scrapes websites and converts their content to Markdown format. It's designed to be a flexible tool for creating local, searchable copies of websites or documentation in Markdown format.

The script uses Scrapy for web crawling and html2text for HTML to Markdown conversion. It can scrape a single URL or multiple URLs from a file. The scraped content is saved as separate Markdown files, maintaining the original site structure. Additionally, the script creates a table of contents for the scraped content and automatically updates .gitignore to prevent version control of scraped content.

This script was initially created to convert online documentation to local, LLM-friendly information. The script and documentation have been improved with AI assistance and now incorporate secure coding practices.

## Features

- Crawls specified websites (single URL or multiple URLs from a file)
- Converts HTML content to Markdown
- Saves each page as a separate Markdown file, maintaining the original site structure
- Creates a table of contents for the scraped content
- Automatically updates .gitignore to prevent version control of scraped content
- Configurable options via command line flags
- Ability to limit scraping to specific subdirectories
- Beta feature to limit the amount of data downloaded
- Implements secure coding practices, including input validation and sanitization

## Requirements

- Python 3.x

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required dependencies using the provided requirements.txt file:
   ```
   pip install -r requirements.txt
   ```

This will install the following dependencies:
- scrapy
- html2text
- validators

## Usage

Run the script using one of the following commands:

```
python web_scraper.py -u <url> -o <output_dir> [options]
python web_scraper.py -f <url_file> -o <output_dir> [options]
```

### Options

- `-u, --url URL`: The URL to scrape
- `-f, --file FILE`: File containing URLs to scrape (one per line)
- `-o, --output OUTPUT_DIR`: The directory to save the Markdown files (required)
- `-i, --ignore-links`: Ignore links in the HTML when converting to Markdown
- `-a, --user-agent AGENT`: Set a custom user agent string
- `-v, --verbose`: Increase output verbosity
- `-s, --subdir SUBDIR`: Limit scraping to a specific subdirectory
- `--data-download-limit LIMIT`: Limit the amount of data to download (e.g., 4GB). Beta feature.

### Examples

Scrape a single website:
```
python web_scraper.py -u https://example.com -o output
```

Scrape multiple websites listed in a file:
```
python web_scraper.py -f urls.txt -o output
```

Scrape a website and ignore links:
```
python web_scraper.py -u https://example.com -o output -i
```

Scrape a website with a custom user agent and verbose output:
```
python web_scraper.py -u https://example.com -o output -a "MyBot/1.0" -v
```

Scrape only the '/docs' subdirectory of a website:
```
python web_scraper.py -u https://example.com -o output -s /docs
```

Scrape only the '/blog' subdirectory and its subpages:
```
python web_scraper.py -u https://example.com -o output -s /blog
```

Scrape a specific subdirectory with verbose output and a custom user agent:
```
python web_scraper.py -u https://example.com -o output -s /products -v -a "CustomBot/2.0"
```

Scrape multiple websites from a file, but limit each to a specific subdirectory:
```
python web_scraper.py -f urls.txt -o output -s /api/v1
```

Attempt to limit the amount of data downloaded:
```
python web_scraper.py -u https://example.com -o output --data-download-limit 4GB
```

## Behavior

By default, the script will only scrape pages that are subpages of the original URL. For example, if you scrape `https://example.com/docs`, it will only scrape pages under the `/docs` directory and won't scrape pages like `https://example.com/blog`.

When you use the `-s` or `--subdir` option, the script will limit the scraping to the specified subdirectory for all input URLs. This is useful when you want to scrape only a portion of a large website or maintain consistent behavior across multiple websites.

The `--data-download-limit` option allows you to set a limit on the total amount of data downloaded. The script will stop crawling once this limit is reached.

## Output

The script will create the following in the specified output directory:

1. A directory structure mirroring the scraped website(s)
2. Markdown files for each scraped page
3. A `table_of_contents.md` file providing an overview of all scraped content

## Security Considerations

The script now implements several secure coding practices:

1. Input validation: URLs are validated before processing
2. Sanitization: File paths and content are properly sanitized to prevent directory traversal attacks
3. Error handling: Improved error handling to gracefully manage exceptions
4. Resource limits: The ability to limit the amount of data downloaded

## Note

The script automatically adds the output directory to .gitignore in the Git root directory to prevent version control of scraped content.

## Contributing

Contributions to improve the script or add new features are welcome. Please feel free to submit a pull request or open an issue for any bugs or feature requests.

## Improvements and Resolved Issues

The following improvements have been made to the script:

1. Improved code structure: Large functions have been split into smaller, more manageable functions
2. Enhanced readability: Inline documentation has been updated and improved
3. Better error handling: The script now handles exceptions more gracefully
4. Unique filenames: The file naming logic now creates unique filenames for each scraped page
5. Improved security: Input validation and sanitization have been implemented

## Remaining Considerations

While many issues have been addressed, there are still areas for potential improvement:

1. Testing: Comprehensive unit tests could be added to ensure reliability
2. Performance optimization: The script's performance could be further optimized for large-scale scraping tasks
3. Advanced filtering: More advanced options for filtering content during scraping could be implemented
4. Customizable output formats: Support for additional output formats beyond Markdown could be added

## License

[Specify the license here, e.g., MIT, GPL, etc.]
