"""
GUI interface for the web scraper using NiceGUI.
This provides a user-friendly interface for the web scraping functionality.
"""

import os
import tempfile
from typing import List, Optional
from nicegui import ui, app
from pathlib import Path
import asyncio
import queue
import threading

from web_scraper import start_scraping, set_status_callback

# Queue for status messages
status_queue = queue.Queue()

def create_temp_url_file(urls: List[str]) -> str:
    """Create a temporary file containing URLs."""
    temp = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    for url in urls:
        temp.write(f"{url}\n")
    temp.close()
    return temp.name

class WebScraperGUI:
    def __init__(self):
        self.status_messages: List[str] = []
        self.scraping_in_progress = False
        
        # Create the main layout
        with ui.card().classes('w-full max-w-3xl mx-auto mt-4 p-4'):
            ui.label('Web Scraper').classes('text-2xl mb-4')
            
            # URL Input Section
            with ui.card().classes('w-full mb-4 p-4'):
                ui.label('URLs').classes('text-lg mb-2')
                self.url_input = ui.textarea(
                    placeholder='Enter URLs (one per line)',
                    rows=5
                ).classes('w-full')

            # Output Directory Section
            with ui.card().classes('w-full mb-4 p-4'):
                ui.label('Output Directory').classes('text-lg mb-2')
                with ui.row().classes('w-full'):
                    self.output_dir = ui.input(
                        placeholder='Enter output directory path'
                    ).classes('flex-grow')
                    ui.button('Browse', on_click=self.browse_directory).classes('ml-2')

            # Options Section
            with ui.card().classes('w-full mb-4 p-4'):
                ui.label('Options').classes('text-lg mb-2')
                with ui.grid(columns=2).classes('w-full gap-4'):
                    self.ignore_links = ui.switch('Ignore links')
                    self.verbose = ui.switch('Verbose output')
                    self.combine_markdown = ui.switch('Combine markdown files')
                    
                    with ui.row():
                        ui.label('Delay (seconds):')
                        self.delay = ui.number(value=1.0, min=0.1, max=10.0, step=0.1)
                    
                    with ui.row():
                        ui.label('User Agent:')
                        self.user_agent = ui.input(
                            value='Mozilla/5.0',
                            placeholder='Enter user agent string'
                        )
                    
                    with ui.row():
                        ui.label('Subdirectory:')
                        self.subdir = ui.input(placeholder='Optional: Limit to subdirectory')
                    
                    with ui.row():
                        ui.label('Data limit:')
                        self.data_limit = ui.input(
                            placeholder='Optional: e.g., 4GB'
                        )

            # Status Section
            with ui.card().classes('w-full mb-4 p-4'):
                ui.label('Status').classes('text-lg mb-2')
                self.status_area = ui.textarea(
                    readonly=True,
                    rows=10
                ).classes('w-full font-mono')

            # Action Buttons
            with ui.row().classes('w-full gap-4 justify-center'):
                self.start_button = ui.button(
                    'Start Scraping',
                    on_click=self.start_scraping
                ).classes('bg-green-500')
                self.clear_button = ui.button(
                    'Clear',
                    on_click=self.clear_form
                ).classes('bg-gray-500')

        # Start the status update task
        asyncio.create_task(self.update_status_area())

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
        status_queue.put(message)

    async def update_status_area(self):
        """Continuously update the status area with new messages."""
        while True:
            try:
                # Update status area with any new messages
                while not status_queue.empty():
                    message = status_queue.get_nowait()
                    self.status_messages.append(message)
                    # Keep only the last 100 messages
                    self.status_messages = self.status_messages[-100:]
                    self.status_area.value = '\n'.join(self.status_messages)
                    # Scroll to bottom
                    await ui.run_javascript(
                        f'document.getElementById("{self.status_area.id}").scrollTop = '
                        f'document.getElementById("{self.status_area.id}").scrollHeight'
                    )
            except queue.Empty:
                pass
            await asyncio.sleep(0.1)

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
        self.delay.value = 1.0
        self.user_agent.value = 'Mozilla/5.0'
        self.subdir.value = ''
        self.data_limit.value = ''
        self.status_messages = []
        self.status_area.value = ''

    def start_scraping(self):
        """Start the web scraping process."""
        if self.scraping_in_progress:
            self.update_status("Scraping already in progress")
            return

        error = self.validate_inputs()
        if error:
            self.update_status(f"Error: {error}")
            return

        # Disable the start button and enable the stop button
        self.start_button.disabled = True
        self.scraping_in_progress = True

        # Get URLs from textarea
        urls = [url.strip() for url in self.url_input.value.split('\n') if url.strip()]
        
        # Create a temporary file for URLs
        url_file = create_temp_url_file(urls)

        # Start scraping in a separate thread
        def scrape_thread():
            try:
                set_status_callback(self.update_status)
                start_scraping(
                    urls=urls,
                    output_dir=self.output_dir.value,
                    ignore_links=self.ignore_links.value,
                    user_agent=self.user_agent.value,
                    verbose=self.verbose.value,
                    subdir=self.subdir.value if self.subdir.value else None,
                    data_limit=self.data_limit.value if self.data_limit.value else None,
                    combine_markdown=self.combine_markdown.value,
                    delay=self.delay.value
                )
            except Exception as e:
                self.update_status(f"Error: {str(e)}")
            finally:
                # Clean up
                try:
                    os.unlink(url_file)
                except:
                    pass
                self.scraping_in_progress = False
                ui.run_javascript(f'document.getElementById("{self.start_button.id}").disabled = false')

        threading.Thread(target=scrape_thread, daemon=True).start()

# Create and run the app
def main():
    app.add_static_files('/static', str(Path(__file__).parent / 'static'))
    WebScraperGUI()
    ui.run(title='Web Scraper', favicon='🕷️')

if __name__ == '__main__':
    main()
