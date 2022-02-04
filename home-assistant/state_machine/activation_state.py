from dependency_injector.wiring import inject
from typing import Any, List, Mapping
import numpy as np
import time
from functools import partial

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
        self.yes_and_no = ["yes", "no"]
        self.update_commands(commands)

    def update_commands(self, commands: Mapping[str, Any]):
        self.commands = commands
        self.command_str_list = list(commands.keys())
        if len(self.command_str_list) > 0:
            self.command_emb_list = self.sentence_matching_model.get_embeddings(
                self.command_str_list
            )
        self.yes_and_no_emb = self.sentence_matching_model.get_embeddings(
            self.yes_and_no
        )

    def set_fallback_state(self, state: IState):
        self.fallback_state = state

    def listen_to_command(self):
        for i in range(self.number_of_tries + 1):
            sound = self.interpreter.listen(10, 10)
            query = self.interpreter.speech_recognition(sound)
            if query is not None:
                break
            else:
                print("Sorry, I did not hear what you said. Try again...")
        return query

    def handle(self, state_machine):

        query = self.listen_to_command()
        if query is None:
            print("Unable to hear. Please call me again when you need me.")
            return state_machine.fall_back()
        else:
            values = self.sentence_matching_model.match(
                self.command_str_list, self.command_emb_list, query
            )

            if len(values) > 0 and values[0][1] > 0.5:
                # Execute command calback
                self.commands.get(values[0][0])()
            else:
                print("Did you mean: '{}'?".format(values[0][0]))
                awnser = self.listen_to_command()
                yes_or_no = self.sentence_matching_model.match(
                    self.yes_and_no, self.yes_and_no_emb, awnser
                )
                if yes_or_no[0][0].lower() == "yes" and yes_or_no[0][1] > 0.8:
                    # Execute command calback
                    self.commands.get(values[0][0])()
                else:
                    print("Sorry I was not able to help.... :'( ")

            return state_machine.fall_back()

    def exit(self) -> "IState":
        pass
