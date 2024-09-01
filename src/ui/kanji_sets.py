from utils.constants import ACCENT_COLOR

from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.layout import Layout
from rich import box

from math import ceil


class KanjiSets:

    def __init__(self, console, layout, user_data, app_data):
        
        self.app_data = app_data
        self.user_data = user_data
        self.update_user_info()

        self.console = console
        self.layout = layout

        ### Initialize Menu variabels
         
        # Kanji sets
        self.selected_set_id = 0
        self.kanji_sets = list(self.app_data.keys())
        self.selected_set = self.get_selected_kanji_set()

        # Kanji grades
        self.grades = self.selected_set['grades'] 
        self.selected_grade_id = 0 
        self.selected_grade = self.get_selected_kanji_grade()

        # Kanji pages
        self.selected_page = 0
        self.max_pages = 1


    def get_selected_kanji_set(self) -> dict:
        return self.app_data[self.kanji_sets[self.selected_set_id]]
    
    def get_selected_kanji_grade(self) -> dict:
        key = self.grades[self.selected_grade_id]
        return self.selected_set['kanji'][key]

    def update_user_info(self):
        """Update user information with known kanji data."""
        for set_key, kanji_set in self.app_data.items():
            user_info = { 
                grade_key: [char in self.user_data for char in kanji_grade]
                for grade_key, kanji_grade in kanji_set['kanji'].items()
            }
            self.app_data[set_key]['user_info'] = user_info

    def __rich__(self) -> Panel:

        layout = Layout()
        
        self.update_pages()
  
        # Define the top panel with text
        top_panel = Panel(
            self.create_kanji_text(self.calculate_capacity()),
            border_style=ACCENT_COLOR,
            title=f"漢字 Sets | Page: {self.selected_page + 1}/{self.max_pages}",
            title_align="left",
            box=box.SQUARE,
            padding=(1,2)
        )

        # Define bottom panel with menus
        sets_menu = self.create_menu(self.kanji_sets, self.selected_set_id)
        grades_menu = self.create_menu(self.grades, self.selected_grade_id)       

        menu = Table.grid(expand=True)
        menu.add_column(justify="center")
        menu.add_row(sets_menu)
        menu.add_row()
        menu.add_row(grades_menu)
        
        footer_menu = Panel(
            menu,
            title_align="left",
            box=box.MINIMAL
        )

        layout.split_column(
            Layout(top_panel),  # Adjust size as needed
            Layout(footer_menu, size=5)
        )

        return layout

    def calculate_capacity(self) -> int:
        """Calculate how many kanji do fit on one page"""
        h_padding, v_padding = 2, 1
        border = 1
        menu_width = 30
        header_height = 6
        page_menu_height = 5
        footer_height = 3        

        width = (self.console.size.width - menu_width - 2* (h_padding + border)) //2

        height = self.console.size.height - (header_height + footer_height + page_menu_height) - 2*(border + v_padding)
        capacity = width*height
        return capacity

    def create_menu(self, items: list, selected_index: int) -> Table:
        """Create a menu with a list of items and highlight the selected one."""
        menu = Table.grid(expand=True)
        for i, item in enumerate(items):
            color = f"white on {ACCENT_COLOR}" if selected_index == i else "white"
            menu.add_column(str(i), justify="center", style=color, ratio=1)
        menu.add_row(*items)
        return menu
       
    def create_kanji_text(self, capacity: int) -> Text:
        """Create a Text object for displaying kanji with known ones highlighted."""
        start = capacity * self.selected_page
        end = start + capacity
        kanji_selected = self.selected_grade[start:end]
        grade_known = self.selected_set['user_info'][self.grades[self.selected_grade_id]]
        
        text = Text()
        for i, ch in enumerate(kanji_selected):
            text.append(ch, style=ACCENT_COLOR if grade_known[i] else None)
        
        return text    
    
    # Control logic, used by keyboard inputs
    def update_set(self):
        """Based on changed id's update current kanji set dictionary"""
        # Update all dictionaries
        self.selected_set = self.get_selected_kanji_set()
        self.grades = self.selected_set['grades']
    
    def update_grade(self):
        """Based on changed id's update current kanji grade dictionary"""
        self.selected_grade = self.get_selected_kanji_grade()

    def update_pages(self):
        """Re-calculate the amount of pages needed to store the displayed kanji"""
        self.max_pages = ceil(len(self.selected_grade) / self.calculate_capacity())

    def next_set(self):
        """Move to the next kanji set."""
        self.selected_set_id = (self.selected_set_id + 1) % len(self.kanji_sets)
        self.selected_grade_id = 0
        self.selected_page = 0

        self.update_set()

    def next_grade(self):
        """Move to the next kanji grade."""
        self.selected_grade_id += 1
        self.selected_page = 0
        
        if self.selected_grade_id >= len(self.grades):
            self.next_set()
        self.update_grade()

    def page_right(self):
        """Move to the next page."""
        self.selected_page += 1

        if self.selected_page >= self.max_pages:
            self.next_grade()
            
    def previous_set(self):
        """Move to the previous kanji set."""
        self.selected_set_id = (self.selected_set_id - 1) % len(self.kanji_sets)
        self.selected_grade_id = 0
        self.selected_page = 0

        self.update_set()

    def previous_grade(self):
        """Move to the previous kanji grade."""
        self.selected_grade_id -= 1
        self.selected_page = 0

        if self.selected_grade_id < 0:
            self.previous_set()
            self.selected_grade_id = len(self.grades) - 1
    
        self.update_grade()

    def page_left(self):
        """Move to the previous page."""
        self.selected_page -= 1

        if self.selected_page < 0:
            self.previous_grade()
            self.update_pages()
            self.selected_page = self.max_pages - 1

