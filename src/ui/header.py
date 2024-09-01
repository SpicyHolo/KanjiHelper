from rich.panel import Panel
from rich.text import Text
from rich import box

from textwrap import dedent

from utils.constants import ACCENT_COLOR

class Header:
    """Display header with splash art."""
    def __rich__(self) -> Panel:
        splash = """\
            ┓┏┓    ••  ┏┓   ┓    ┏┓ ┏┓
            ┃┫ ┏┓┏┓┓┓  ┃┓┏┓┏┫  ┓┏┃┫ ┃┫
            ┛┗┛┗┻┛┗┃┗  ┗┛┗┛┗┻  ┗┛┗┛•┗┛
                   ┛ー漢字の神 by ホロ
        """
        text = Text(dedent(splash), justify="full", style=ACCENT_COLOR)
        return Panel(text, style="white", box=box.SQUARE, border_style=ACCENT_COLOR)
    