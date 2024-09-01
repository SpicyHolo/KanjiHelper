from utils.constants import ACCENT_COLOR

from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.layout import Layout
from rich import box
from rich.tree import Tree

from math import ceil

import os

class Importer:
    def __init__(self, console, layout, user_data):
        self.usr_data = user_data
        self.console = console
        self.layout = layout

    def __rich__(self) -> Panel:
        return Panel(
            Text("おはよう、世界"),
            border_style=ACCENT_COLOR,
            title=f"漢字 Importer",
            title_align="left",
            box=box.SQUARE,
            padding=(1, 2)
        )
