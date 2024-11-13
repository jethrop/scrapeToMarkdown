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

from web_scraper import start_scraping, set_status_callback

class WebScraperGUI:
    def __init__(self):
        self.status_messages: List[str] = []
        self.scraping_in_progress = False
        
        # Main container
        with ui.column().classes('w-full max-w-3xl mx-auto p-4 gap-4'):
            ui.label('Web Scraper').classes('text-2xl')
            
            # URL Input
            ui.label('URLs').classes('text-lg')
            self.url_input = ui.textarea(
                label='Enter URLs (one per line)',
                placeholder='https://example.com'
            ).props('outlined').classes('w-full')
            
            # Output Directory
            ui.label('Output Directory').classes('text-lg')
            with ui.row().classes('w-full'):
                self.output_dir = ui.input(
                    label='Output Directory',
                    placeholder='Select output directory'
                ).props('outlined').classes('flex-grow')
                ui.button(icon='folder', on_click=self.browse_directory)
            
            # Options
            with ui.expansion('Options', icon='settings').classes('w-full'):
                with ui.column().classes('w-full gap-2'):
                    self.ignore_links = ui.switch('Ignore links')
                    self.verbose = ui.switch('Verbose output')
                    self.combine_markdown = ui.switch('Combine markdown files')
                    
                    ui.number('Delay (seconds)', 
                             value=1.0, 
                             min=0.1, 
                             max=10.0, 
                             step=0.1, 
                             on_change=lambda e: setattr(self, 'delay', e.value))
                    
                    self.user_agent = ui.input(
                        label='User Agent',
                        value='Mozilla/5.0'
                    ).props('outlined')
                    
                    self.subdir = ui.input(
                        label='Subdirectory (optional)',
                        placeholder='docs'
                    ).props('outlined')
                    
                    self.data_limit = ui.input(
                        label='Data limit (optional)',
                        placeholder='4GB'
                    ).props('outlined')
            
            # Status Area
            with ui.card().classes('w-full'):
                ui.label('Status').classes('text-lg')
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

    async def browse_directory(self):
        """Open a directory picker dialog."""
        result = await ui.run_javascript('''
            async function browseDirectory() {
                try {
                    const dirHandle = await window.showDirectoryPicker();
                    return dirHandle.name;
                } catch (err) {
                    return null;
                }
            }
            browseDirectory();
        ''')
        if result:
            self.output_dir.value = result

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
