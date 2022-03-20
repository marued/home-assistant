from dependency_injector.wiring import inject
from .base_command import BaseCommand, COMMAND_TYPES
from functools import partial
import webbrowser


class SearchGoogleMaps(BaseCommand):
    @inject
    def __init__(
        self, command_str: str, type: COMMAND_TYPES, fct: partial = None
    ) -> None:
        super().__init__(command_str, type, fct)

    def execute(self, command_text: str = None):
        # http://www.google.com/search?
        print("\n Opening Google maps.\n")
        search_text = ""
        idx_nearest = command_text.lower().find("nearest ")
        idx_to = command_text.lower().find("to ")
        if idx_nearest != -1:
            search_text = command_text[idx_nearest + 8 :]
        elif idx_to != -1:
            search_text = command_text[idx_to + 3 :]
        webbrowser.open_new_tab(
            "https://www.google.com/maps/search/{}".format(search_text.replace(" ", "+"))
        )
