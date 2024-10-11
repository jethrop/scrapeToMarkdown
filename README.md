# Web Scraper to Markdown Converter

This project contains a Python script that scrapes websites and converts their content to Markdown format. It's designed to be a flexible tool for creating local, searchable copies of websites or documentation in Markdown format.

## Features

- Crawls specified websites (single URL or multiple URLs from a file)
- Converts HTML content to Markdown
- Saves each page as a separate Markdown file, maintaining the original site structure
- Creates a table of contents for the scraped content
- Automatically updates .gitignore to prevent version control of scraped content
- Configurable options via command line flags

## Requirements

- Python 3.x
- scrapy
- html2text

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required dependencies:
   ```
   pip install scrapy html2text
   ```

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

## Output

The script will create the following in the specified output directory:

1. A directory structure mirroring the scraped website(s)
2. Markdown files for each scraped page
3. A `table_of_contents.md` file providing an overview of all scraped content

## Note

The script automatically adds the output directory to .gitignore in the Git root directory to prevent version control of scraped content.

## Contributing

Contributions to improve the script or add new features are welcome. Please feel free to submit a pull request or open an issue for any bugs or feature requests.

## License

[Specify the license here, e.g., MIT, GPL, etc.]
