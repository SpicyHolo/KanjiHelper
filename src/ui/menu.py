from utils.constants import ACCENT_COLOR

from rich.panel import Panel
from rich.text import Text
from rich import box

class Menu:
    """Display side menu controlled by keyboard"""

    def __init__(self, console, layout):
        self.selected_index = 0
        self.hover_index = 0
        self.options = ["Kanji Gallery", "Import Kanji", "Kanji Sets"]
        self.max_index = len(self.options)

        self.console = console
        self.layout = layout

    def __rich__(self) -> Panel:
        menu_text = Text(justify="left")
        for i, option in enumerate(self.options):
            if i == self.hover_index and i == self.selected_index:
                # Both hovered and selected: Magenta text on White background
                menu_text.append(f"{option}\n", style="bold black on " + ACCENT_COLOR)
            elif i == self.hover_index:
                # Hovered: White text on Black background
                menu_text.append(f"{option}\n", style="bold white on " + ACCENT_COLOR)
            elif i == self.selected_index:
                # Selected: Magenta text
                menu_text.append(f"{option}\n", style="bold " + ACCENT_COLOR)
            else:
                # Default: No special style
                menu_text.append(f"{option}\n")

        return Panel(menu_text, title="Menu", border_style=ACCENT_COLOR, title_align="left", padding=(1, 2), box=box.SQUARE)
    
    def move_down(self):
        self.hover_index = (self.hover_index + 1) % self.max_index

    def move_up(self):
        self.hover_index = (self.hover_index - 1) % self.max_index

    def select(self):
        self.selected_index = self.hover_index

    def get_selected_option(self):
        return self.options[self.selected_index]