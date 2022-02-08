from .base_command import BaseCommand


class Command(BaseCommand):
    def __init__(self) -> None:
        super().__init__()

    def execute(self):
        print("\nClosing Camera.\n")
