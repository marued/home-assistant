from dependency_injector.wiring import inject
from typing import Any, List, Mapping
import numpy as np
import time
from functools import partial
from ..commands.command_executer import CommandExecuter
from .IState import IState


class ActivationState(IState):
    @inject
    def __init__(
        self,
        command_executer: CommandExecuter,
        interpreter: Any,
        number_of_tries: int = 3,
    ) -> None:
        super().__init__()
        self.interpreter = interpreter
        self.number_of_tries = number_of_tries
        self.fallback_state: IState = None
        self.command_str_list: List[str] = []
        self.command_emb_list: List[np.array] = np.array([])
        self.command_executer = command_executer
        self.yes_and_no = ["yes", "no"]
        self.yes_and_no_emb = command_executer.sentence_matching_model.get_embeddings(
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
            query_result = self.command_executer.match(query)

            if len(query_result) > 0 and query_result[0][1] > 0.5:
                verbal_command = query_result[0][0]
                self.command_executer.execute(verbal_command)
            else:
                print("Did you mean: '{}'?".format(query_result[0][0]))
                awnser = self.listen_to_command()
                yes_or_no = self.command_executer.sentence_matching_model.match(
                    self.yes_and_no, self.yes_and_no_emb, awnser
                )
                if yes_or_no[0][0].lower() == "yes" and yes_or_no[0][1] > 0.7:
                    verbal_command = query_result[0][0]
                    self.command_executer.execute(verbal_command)
                else:
                    print("Sorry I was not able to help.... :'( ")

            return state_machine.fall_back()

    def exit(self) -> "IState":
        pass
