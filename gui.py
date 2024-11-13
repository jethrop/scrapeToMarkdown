"""
GUI interface for the web scraper using NiceGUI.
This provides a user-friendly interface for the web scraping functionality.
"""

import os
import tempfile
from typing import List, Optional
from nicegui import ui, app
import asyncio
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

from web_scraper import start_scraping, set_status_callback

class WebScraperGUI:
    def __init__(self):
        self.status_messages: List[str] = []
        self.scraping_in_progress = False
        
        # Initialize tkinter for file dialog
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the tkinter root window
        
        # Main container
        with ui.column().classes('w-full max-w-3xl mx-auto p-4 gap-4'):
            ui.label('Web Scraper').classes('text-2xl')
            
            # URL Input
            with ui.card().classes('w-full p-4'):
                ui.label('URLs').classes('text-lg')
                ui.label('''Enter one or more URLs to scrape, one per line. 
                        The scraper will convert each page to Markdown format.
                        Example: https://example.com/docs''').classes('text-sm text-gray-500')
                self.url_input = ui.textarea(
                    label='Enter URLs (one per line)',
                    placeholder='https://example.com'
                ).props('outlined').classes('w-full')
            
            # Output Directory
            with ui.card().classes('w-full p-4'):
                ui.label('Output Directory').classes('text-lg')
                ui.label('''Select where to save the scraped content. 
                        A directory structure matching the website will be created.
                        The output will include Markdown files and a table of contents.''').classes('text-sm text-gray-500')
                with ui.row().classes('w-full'):
                    self.output_dir = ui.input(
                        label='Output Directory',
                        placeholder='Select output directory'
                    ).props('outlined').classes('flex-grow')
                    ui.button('Browse', on_click=self.browse_directory).props('icon=folder')
            
            # Options
            with ui.expansion('Options', icon='settings').classes('w-full'):
                with ui.column().classes('w-full gap-4 p-4'):
                    with ui.card().classes('w-full p-4'):
                        with ui.row():
                            self.ignore_links = ui.switch('Ignore links')
                            ui.label('''When enabled, links in the content will be removed during conversion. 
                                    This creates cleaner Markdown without external references.''').classes('text-sm text-gray-500 ml-2')
                    
                    with ui.card().classes('w-full p-4'):
                        with ui.row():
                            self.verbose = ui.switch('Verbose output')
                            ui.label('''Enable detailed logging of the scraping process. 
                                    Useful for debugging or monitoring progress.''').classes('text-sm text-gray-500 ml-2')
                    
                    with ui.card().classes('w-full p-4'):
                        with ui.row():
                            self.combine_markdown = ui.switch('Combine markdown files')
                            ui.label('''Combine all Markdown files in each directory into a single file.
                                    Useful for creating comprehensive documentation files.''').classes('text-sm text-gray-500 ml-2')
                    
                    with ui.card().classes('w-full p-4'):
                        ui.label('Delay Settings').classes('text-lg')
                        ui.label('''Set the delay between requests to prevent overwhelming the target website.
                                The actual delay will be randomized between 0.5× and 1.5× this value.''').classes('text-sm text-gray-500')
                        ui.number('Delay (seconds)', 
                                value=1.0, 
                                min=0.1, 
                                max=10.0, 
                                step=0.1, 
                                on_change=lambda e: setattr(self, 'delay', e.value))
                    
                    with ui.card().classes('w-full p-4'):
                        ui.label('User Agent').classes('text-lg')
                        ui.label('''Specify the User-Agent string for requests.
                                Some websites may block or behave differently based on this.''').classes('text-sm text-gray-500')
                        self.user_agent = ui.input(
                            label='User Agent',
                            value='Mozilla/5.0'
                        ).props('outlined')
                    
                    with ui.card().classes('w-full p-4'):
                        ui.label('Subdirectory Limitation').classes('text-lg')
                        ui.label('''Optionally limit scraping to a specific subdirectory.
                                Example: Enter "docs" to only scrape pages under the /docs/ path.''').classes('text-sm text-gray-500')
                        self.subdir = ui.input(
                            label='Subdirectory (optional)',
                            placeholder='docs'
                        ).props('outlined')
                    
                    with ui.card().classes('w-full p-4'):
                        ui.label('Data Download Limit').classes('text-lg')
                        ui.label('''Set a limit on the total amount of data to download.
                                Format: 4GB, 100MB, etc. Helps prevent excessive downloads.''').classes('text-sm text-gray-500')
                        self.data_limit = ui.input(
                            label='Data limit (optional)',
                            placeholder='4GB'
                        ).props('outlined')
            
            # Status Area
            with ui.card().classes('w-full p-4'):
                ui.label('Status').classes('text-lg')
                ui.label('''Real-time status updates of the scraping process.
                        Shows progress, errors, and completion status.''').classes('text-sm text-gray-500')
                self.status = ui.textarea(
                    label='Status Messages'
                ).props('outlined readonly').classes('w-full font-mono')
            
            # Action Buttons
            with ui.row().classes('w-full gap-4 justify-center'):
                self.start_button = ui.button(
                    'Start Scraping',
                    on_click=self.start_scraping
                ).props('color=primary')
                ui.button(
                    'Clear',
                    on_click=self.clear_form
                ).props('color=secondary')

    def browse_directory(self):
        """Open a directory picker dialog using tkinter."""
        directory = filedialog.askdirectory(
            title='Select Output Directory',
            initialdir=os.path.expanduser('~')
        )
        if directory:
            self.output_dir.value = directory

    def update_status(self, message: str):
        """Update status messages."""
        self.status_messages.append(message)
        self.status_messages = self.status_messages[-100:]  # Keep last 100 messages
        self.status.value = '\n'.join(self.status_messages)

    def validate_inputs(self) -> Optional[str]:
        """Validate user inputs before starting the scraping process."""
        if not self.url_input.value or not self.url_input.value.strip():
            return "Please enter at least one URL"
        
        if not self.output_dir.value or not self.output_dir.value.strip():
            return "Please specify an output directory"
        
        urls = [url.strip() for url in self.url_input.value.split('\n') if url.strip()]
        for url in urls:
            if not url.startswith(('http://', 'https://')):
                return f"Invalid URL format: {url}"
        
        return None

    def clear_form(self):
        """Clear all form inputs."""
        self.url_input.value = ''
        self.output_dir.value = ''
        self.ignore_links.value = False
        self.verbose.value = False
        self.combine_markdown.value = False
        self.delay = 1.0
        self.user_agent.value = 'Mozilla/5.0'
        self.subdir.value = ''
        self.data_limit.value = ''
        self.status_messages = []
        self.status.value = ''

    async def start_scraping(self):
        """Start the web scraping process."""
        if self.scraping_in_progress:
            self.update_status("Scraping already in progress")
            return

        error = self.validate_inputs()
        if error:
            self.update_status(f"Error: {error}")
            return

        # Disable the start button
        self.start_button.disabled = True
        self.scraping_in_progress = True

        try:
            # Get URLs from textarea
            urls = [url.strip() for url in self.url_input.value.split('\n') if url.strip()]
            
            # Set up status callback
            set_status_callback(self.update_status)
            
            # Start scraping
            await asyncio.get_event_loop().run_in_executor(
                None,
                start_scraping,
                urls,
                self.output_dir.value,
                self.ignore_links.value,
                self.user_agent.value,
                self.verbose.value,
                self.subdir.value if self.subdir.value else None,
                self.data_limit.value if self.data_limit.value else None,
                self.combine_markdown.value,
                getattr(self, 'delay', 1.0)
            )
            
            self.update_status("Scraping completed successfully!")
            
        except Exception as e:
            self.update_status(f"Error during scraping: {str(e)}")
        
        finally:
            self.scraping_in_progress = False
            self.start_button.disabled = False

def main():
    """Initialize and run the application."""
    scraper_gui = WebScraperGUI()
    
    # Enable FastAPI docs
    app.include_router = True
    
    ui.run(
        title='Web Scraper',
        favicon='🕷️',
        dark=True,
        reload=False,
        show=True,
        port=8080,
        host='127.0.0.1',  # Only expose on localhost
        storage_secret='web_scraper'  # Enable storage features
    )

if __name__ == '__main__':
    main()
