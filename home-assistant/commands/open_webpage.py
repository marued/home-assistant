from dependency_injector.wiring import inject
from .base_command import BaseCommand, COMMAND_TYPES
from functools import partial
import webbrowser


class OpenWebpage(BaseCommand):
    @inject
    def __init__(
        self, command_str: str, type: COMMAND_TYPES, fct: partial = None
    ) -> None:
        super().__init__(command_str, type, fct)

    def execute(self, command_text: str = None):
        # http://www.google.com/search?
        print("\n Opening web Page.\n")
        search_text = ""
        idx_search = command_text.lower().find("search for ")
        idx_about = command_text.lower().find("about ")
        idx_page = command_text.lower().find("page ")
        if idx_search != -1:
            search_text = command_text[idx_search + 11 :]
        elif idx_about != -1:
            search_text = command_text[idx_about + 6 :]
        elif idx_page != -1:
            search_text = command_text[idx_page + 5 :]
        webbrowser.open_new_tab(
            "https://www.google.com/search?q={}".format(search_text.replace(" ", "+"))
        )
