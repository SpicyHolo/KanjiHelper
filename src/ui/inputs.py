
from prompt_toolkit.key_binding import KeyBindings

class keyboardInput():
    def __init__(self, menu, gallery, kanji_sets):
        self.menu = menu
        self.gallery = gallery
        self.kanji_sets = kanji_sets
        self.bindings = KeyBindings()
        self.exit_app = False
        self._setup_key_bindings()

    def _setup_key_bindings(self):
        @self.bindings.add('up')
        @self.bindings.add('j')
        def navigate_up(event):
            self.menu.move_up()
            self.menu.select()
            
        @self.bindings.add('k')
        @self.bindings.add('down')
        def navigate_down(event):
            self.menu.move_down()
            self.menu.select()

        @self.bindings.add('right')
        @self.bindings.add('l')
        def navigate_right(event):
            if self.menu.get_selected_option() == "Kanji Gallery":
                self.gallery.page_right()
            elif self.menu.get_selected_option() == "Kanji Sets":
                self.kanji_sets.page_right()

        @self.bindings.add('left')
        @self.bindings.add('h')
        def navigate_left(event):
            if self.menu.get_selected_option() == "Kanji Gallery":
                self.gallery.page_left()
            elif self.menu.get_selected_option() == "Kanji Sets":
                self.kanji_sets.page_left()

        @self.bindings.add('q')
        def exit(event):
            self.exit_app = True

        @self.bindings.add('tab')
        def navigate_quick_right(event):
            if self.menu.get_selected_option() == "Kanji Sets":
                self.kanji_sets.next_set()
        @self.bindings.add('s-tab')
        def navigate_quick_left(event):
            if self.menu.get_selected_option() == "Kanji Sets":
                self.kanji_sets.previous_set()


    
    def get_exit_app(self):
        return self.exit_app