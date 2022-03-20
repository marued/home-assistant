from dependency_injector.wiring import inject
from .base_command import BaseCommand, COMMAND_TYPES
from functools import partial
from word2number import w2n

import threading


class SetTimer(BaseCommand):
    @inject
    def __init__(
        self, command_str: str, type: COMMAND_TYPES, fct: partial = None
    ) -> None:
        super().__init__(command_str, type, fct)

    def execute(self, command_text: str = None):

        start_idx = command_text.lower().find("for ") + 4
        if start_idx != -1:
            minute_idx = command_text.lower().find("minute")
            second_idx = command_text.lower().find("second")
            hour_idx = command_text.lower().find("hour")
            if minute_idx != -1:
                name = "min."
                number = w2n.word_to_num(command_text[start_idx:minute_idx])
                threading.Timer(number * 60, self.timer_sound).start()
            elif second_idx != -1:
                name = "sec."
                number = w2n.word_to_num(command_text[start_idx:second_idx])
                threading.Timer(number, self.timer_sound).start()
            elif hour_idx != -1:
                name = "hour."
                number = w2n.word_to_num(command_text[start_idx:hour_idx])
                threading.Timer(number * 60 * 60, self.timer_sound).start()
            else:
                name = "min."
                number = w2n.word_to_num(command_text[start_idx:])
                threading.Timer(number * 60, self.timer_sound).start()

        print("\n  Timmer set for {} {}...\n".format(number, name))

    def timer_sound(self):
        print("Time is up!")
