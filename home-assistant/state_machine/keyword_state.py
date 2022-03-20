from typing import Any
from dependency_injector.wiring import inject
from functools import partial

from .IState import IState
from ..speech_recognition.local_interpreter import SphinxInterpreter


class ListenForKeywordState(IState):
    @inject
    def __init__(
        self,
        keyword: str,
        interpreter: SphinxInterpreter,
        activation_state: IState = None,
        listen_timeout=None,
        phrase_time_limit=None,
        computer_voice: Any = None,
    ) -> None:
        super().__init__(computer_voice)
        self.keyword = keyword
        self.interpreter = interpreter
        self.activation_state: IState = activation_state
        self.activation_state.set_fallback_state(self)
        self.listen_timeout = listen_timeout
        self.phrase_time_limit = phrase_time_limit

    def interpret_sound(self, state_machine, audio: Any):
        if audio is not None:
            text = self.interpreter.speech_recognition(audio)
            if text.lower() == self.keyword.lower():
                self.say("Yes?")
                print("{} at your service. Actively listening...".format(self.keyword))
                return state_machine.change_state(self.activation_state)

    def handle(self, state_machine) -> "IState":
        """
        Listen and dispatch.
        """
        print("Listening...")
        try:
            audio = self.interpreter.listen(self.listen_timeout, self.phrase_time_limit)
            self.interpret_sound(state_machine, audio)
        except Exception as e:
            print(e)

    def exit(self) -> "IState":
        pass
        # self.stop_listening(wait_for_stop=False)
