from typing import Any
from dependency_injector.wiring import Provide, inject
import time
from functools import partial

from .IState import IState
from ..speech_recognition.local_interpreter import SphinxInterpreter


class ListenForKeywordState(IState):
    @inject
    def __init__(
        self,
        keyword: str,
        interpreter: SphinxInterpreter = None,
        activation_state: IState = None,
    ) -> None:
        super().__init__()
        self.keyword = keyword
        self.interpreter: SphinxInterpreter = (
            SphinxInterpreter() if interpreter is None else interpreter
        )
        self.activation_state: IState = activation_state
        self.activation_state.set_fallback_state(self)

    def interpret_sound(self, recognizer: Any, audio: Any):
        if audio is not None:
            text = self.interpreter.speech_recognition(recognizer, audio)
            if text.lower() == self.keyword.lower():
                print("{} at your service. Actively listening...".format(self.keyword))
                self.stop_listening(wait_for_stop=False)
                return self.activation_state.handle()

    def handle(self) -> "IState":
        """
        Listen and dispatch.
        """
        print("Listening...")
        self.stop_listening = self.interpreter.async_listen(self.interpret_sound)
        for _ in range(500): time.sleep(0.1)
        self.stop_listening(wait_for_stop=False)