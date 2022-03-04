from dependency_injector.wiring import inject
from typing import Any, Mapping, Tuple, List
import sys
from functools import partial
import torch
import numpy as np

from .base_command import BaseCommand, COMMAND_TYPES

default_commands = zip(
    [
        "Open web page.",
        "Set timer.",
        "Exit program.",
    ],
    [
        partial(print, "\n Opening web Page.\n"),
        partial(print, "\n Setting timer.\n"),
        partial(sys.exit),
    ],
)


class CommandExecuter:
    @inject
    def __init__(
        self, sentence_matching_model, command_objects: List[BaseCommand]
    ) -> None:
        self.sentence_matching_model = sentence_matching_model
        self.commands: List[BaseCommand] = []
        self.verbal_command_list: List[str] = []
        self.embeddings: List[Any] = None
        self.add_ftc_commands(default_commands)
        for cmd_obj in command_objects:
            self.add_command(cmd_obj)

    def add_ftc_commands(
        self, new_commands: List[Tuple[str, partial]]
    ) -> Mapping[str, Any]:
        for cmd_str, fct in new_commands:
            self.commands.append(BaseCommand(cmd_str, COMMAND_TYPES.FCT, fct))
            self.verbal_command_list.append(cmd_str)
        self.embeddings = self.sentence_matching_model.get_embeddings(
            self.verbal_command_list
        )

    def add_command(self, command: BaseCommand, force: bool = False) -> bool:
        # if self.commands.get(command.command_str) is not None and not force:
        #    return False
        self.commands.append(command)
        self.verbal_command_list.append(command.command_str)
        self.embeddings = self.sentence_matching_model.get_embeddings(
            self.verbal_command_list
        )
        return True

    def get_commands_str(self) -> List[str]:
        return list(self.commands.keys())

    def match(self, query: str):
        embeddings = torch.FloatTensor(self.embeddings)
        query_result = self.sentence_matching_model.match(
            self.verbal_command_list, embeddings, query
        )
        return query_result

    def execute(self, command_str: str):
        try:
            command_idx = self.verbal_command_list.index(command_str)
            self.commands[command_idx].execute()
        except ValueError as ve:
            print(ve)
        # if command.type == COMMAND_TYPES.FCT:
        #    command.get('fct')()
        # elif command.get("type").lower() == "script":
        #    script = command.get('script')
        #    script_abs_path = os.path.abspath(script)
        #    return_value = subprocess.run("H:/Program_Files/AI_Perso/personnal/home-assistant/.venv/Scripts/activate; python " + script_abs_path, capture_output=True, shell=True)
        #    print("Subprocess exited with the fallowing: {}".format(return_value.stdout.decode()))
