from typing import Any


class IState:
    def __init__(self, computer_voice: Any = None):
        self.computer_voice = computer_voice

    def handle(self, state_machine: Any) -> "IState":
        raise NotImplementedError("Handle is not implemented yet.")

    def exit(self):
        return self

    def say(self, text: str):
        print(text)
        if self.computer_voice is not None:
            self.computer_voice.say(text)
