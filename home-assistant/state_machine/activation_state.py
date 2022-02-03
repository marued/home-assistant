from dependency_injector.wiring import inject
from typing import Any, List, Tuple, Mapping
import numpy as np

from .IState import IState


class ActivationState(IState):
    @inject
    def __init__(
        self,
        commands: Mapping[str, Any],
        interpreter: Any,
        sentence_matching_model: Any,
        number_of_tries: int = 3,
    ) -> None:
        super().__init__()
        self.interpreter = interpreter
        self.number_of_tries = number_of_tries
        self.fallback_state: IState = None
        self.sentence_matching_model: Any = sentence_matching_model
        self.command_str_list: List[str] = []
        self.command_emb_list: List[np.array] = np.array([])
        self.commands = commands
        self.update_commands(commands)

    def update_commands(self, commands: Mapping[str, Any]):
        self.commands = commands
        self.command_str_list = list(commands.keys())
        if len(self.command_str_list) > 0:
            self.command_emb_list = self.sentence_matching_model.get_embeddings(
                self.command_str_list
            )

    def set_fallback_state(self, state: IState):
        self.fallback_state = state

    def listen_to_command(self):
        for i in range(self.number_of_tries + 1):
            sound = self.interpreter.listen()
            query = self.interpreter.speech_recognition(self.interpreter.recognizer, sound)
            if query is not None:
                break
            else:
                print("Sorry, I did not hear what you said. Try again...")
        return query

    def handle(self):

        query = self.listen_to_command()
        if query is None:
            print("Unable to hear. Please call me again when you need me.")
            return self.fallback_state
        else:
            values = self.sentence_matching_model.match(self.command_str_list, self.command_emb_list, query)

            # execute here!
            if len(values) > 0 and values[0][1] > 0.5:
                self.commands.get(values[0][0])()
            else:
                print("Did you mean: '{}'?".format(values[0][0]))
                awnser = self.listen_to_command()
                if awnser.lower() == "yes":
                    self.commands.get(values[0][0])()
                else:
                    print("Sorry I was not able to help.... :'( ")

            return self.fallback_state
