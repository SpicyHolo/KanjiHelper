from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.table import Table

from textwrap import dedent

from utils.constants import ACCENT_COLOR

import getpass

class Footer:
    def __init__(self, user_data):
        self.user_data = user_data
        self.footer_items = list()

    def __rich__(self) -> Panel:
        info_grid = Table.grid(expand=True)
        for item in self.footer_items:
            info_grid.add_column(item, justify="left")
        info_grid.add_row(*self.footer_items)

        return Panel(info_grid, box=box.MINIMAL)
    
    def clear_footer(self):
        self.footer_items = list()

    def add_item(self, item: str):
        self.footer_items.append(item)

    def add_default_footer(self) -> str:
        username = getpass.getuser()
        username = "holo" if username == "konra" else username
        self.footer_items.append(f'Hello, {username} :flushed_face:')

        kanji_total = len(self.user_data)
        self.footer_items.append(f'You know {kanji_total} Kanji already! :eyes:')
