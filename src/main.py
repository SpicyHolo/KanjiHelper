import json
from pathlib import Path
from threading import Thread, Event
from time import sleep
from typing import Optional

from rich import box
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from prompt_toolkit import PromptSession

from ui.header import Header
from ui.gallery import Gallery
from ui.menu import Menu
from ui.kanji_sets import KanjiSets
from ui.inputs import keyboardInput
from utils.constants import ACCENT_COLOR


def make_layout() -> Layout:
    """Define and return the application layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=6),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3),
    )
    layout["main"].split_row(
        Layout(name="menu", size=30),
        Layout(name="body", minimum_size=60),
    )
    return layout


def load_user_data(file_path: Path) -> Optional[str]:
    """Load user data from the given JSON file."""
    try:
        with file_path.open('r', encoding='utf-8') as f:
            return "".join(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        Console().log(f"Error loading user data: {e}")
        return None
    
def load_app_data(file_path: Path) -> Optional[str]:
    """Load app data from the given JSON file."""
    try:
        with file_path.open('r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        Console().log(f"Error loading app data: {e}")
        return None

def run_prompt_loop(session: PromptSession, keyboard_input: keyboardInput, console: Console, stop_event: Event) -> None:
    """Run the input prompt loop in a separate thread."""
    while not stop_event.is_set():
        try:
            session.prompt()
        except KeyboardInterrupt:
            stop_event.set()
            break

def main() -> None:
    """Main function to run the application."""
    console = Console()
    layout = make_layout()

    # Determine the path to the data files
    script_dir = Path(__file__).parent.resolve()
    user_data_file = script_dir / 'data' / 'user_kanji.json'
    app_data_file = script_dir / 'data' / 'kanji_lists.json'

    # Load user data
    user_data = load_user_data(user_data_file)
    if not user_data:
        console.log("Failed to load user data. Exiting...")
        return

    # Load app data
    app_data = load_app_data(app_data_file)
    if not app_data:
        console.log("Failed to load app data. Exiting...")
        return

    # Initialize UI components
    menu = Menu(console, layout)
    gallery = Gallery(console, layout, user_data)
    kanji_sets = KanjiSets(console, layout, user_data, app_data)

    layout["menu"].update(menu)
    layout["body"].update(gallery)
    layout["header"].update(Header())
    layout["footer"].update(Panel(Text("Hello there", style="white on black"), box=box.MINIMAL))

    # Manage keyboard input
    keyboard_input = keyboardInput(menu, gallery, kanji_sets)
    session = PromptSession(key_bindings=keyboard_input.bindings)

    # Create a stop event to signal the thread to exit
    stop_event = Event()

    # Start the prompt loop in a separate thread
    thread = Thread(target=run_prompt_loop, args=(session, keyboard_input, console, stop_event), daemon=True)
    thread.start()

    try:
        # Start the live display
        with Live(layout, refresh_per_second=10, screen=True):
            while not stop_event.is_set() and not keyboard_input.get_exit_app():
                selected_menu = menu.get_selected_option()
                if selected_menu == "Kanji Gallery":
                    layout["body"].update(gallery)
                elif selected_menu == "Kanji Sets":
                    layout["body"].update(kanji_sets)

                sleep(0.1)
    except KeyboardInterrupt:
        console.log("Application interrupted by user")
    finally:
        # Signal the background thread to stop and wait for it to finish
        stop_event.set()
        thread.join()
        console.log("Application exiting")


if __name__ == "__main__":
    main()