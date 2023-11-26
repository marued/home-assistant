from dependency_injector.wiring import inject
from dataclasses import dataclass
from enum import Enum
from functools import partial
from typing import Union, List


class COMMAND_TYPES(Enum):
    FCT = 1
    OBJECT = 2


class BaseCommand:
    """
    Use this class with a callback function or
    extend this class to add a new voice command.

    Params:
    @command_str: either a string or a list of string that will
                define the type of voice commands the model will
                associate this class to call execute(). The AI is smart
                enough to associate similar phrasing.
    @type:  when extending this class, type should be COMMAND_TYPES.OBJECT
            You can also COMMAND_TYPES.FCT when passing a callback function
            in the constructer.
    @fct:   callback function executed when type is set to COMMAND_TYPES.FCT.
    """

    @inject
    def __init__(
        self,
        command_str: Union[str, List[str]],
        type: COMMAND_TYPES,
        fct: partial = None,
    ) -> None:
        self.command_str = command_str
        self.type = type
        self.fct = fct

    def execute(self, command_text: str = None):
        if command_text is None:
            self.fct()
        else:
            self.fct(command_text)
