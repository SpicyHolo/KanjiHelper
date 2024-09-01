from utils.constants import ACCENT_COLOR

from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.layout import Layout
from rich import box

from math import ceil

class Gallery:
    def __init__(self, console, layout, usr_data):
        self.usr_data = usr_data
        self.page = 0
        self.max_pages = 1

        self.console = console
        self.layout = layout

    def calculate_page_capacity(self) -> int:
        h_padding, v_padding = 2, 1
        border = 1
        menu_width = 30
        header_height = 6
        page_menu_height = 3
        footer_height = 3

        width = (self.console.size.width - menu_width - 2* (h_padding + border)) // 2
        height = self.console.size.height - (header_height + footer_height + page_menu_height) - 2*(border + v_padding)
        return width * height
    
    def create_top_panel(self) -> Panel:
        kanji_content = self.get_kanji_content()
        return Panel(
            kanji_content,
            border_style=ACCENT_COLOR,
            title=f"漢字 Gallery | Page: {self.page + 1}/{self.max_pages}",
            title_align="left",
            box=box.SQUARE,
            padding=(1, 2)
        )
    
    def get_kanji_content(self) -> Text:
        text = Text()
        capacity = self.calculate_page_capacity()
        start = self.page * capacity
        end = start + capacity
        text.append(self.usr_data[start:end])
        return text
    
    def create_footer_menu(self) -> Panel:
        menu_buttons = self.create_menu_buttons()
        return Panel(
            menu_buttons,
            title_align="left",
            box=box.SQUARE
        )
    
    def create_menu_buttons(self) -> Table:
        menu_buttons = Table.grid(expand=True)
        for n in range(self.max_pages):
            style = f"white on {ACCENT_COLOR}" if n == self.page else "white"
            menu_buttons.add_column(str(n + 1), justify="center", style=style)
        menu_buttons.add_row(*[f'Page {n + 1}' for n in range(self.max_pages)])
        return menu_buttons
    
    def __rich__(self) -> Panel:
        # Calculate capacity of one page
        capacity = self.calculate_page_capacity()
        self.max_pages = ceil(len(self.usr_data) / capacity)

        layout = Layout()

        top_panel = self.create_top_panel()
        footer_menu = self.create_footer_menu()

        layout.split_column(
            Layout(top_panel),
            Layout(footer_menu, size=3)
        )

        return layout

    def page_right(self):
        self.page = (self.page + 1) % self.max_pages

    def page_left(self):
        self.page = (self.page - 1) % self.max_pages
