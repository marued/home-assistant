from dependency_injector.wiring import inject
from paramiko import SSHClient, AutoAddPolicy
from functools import partial
from typing import Any
from .base_command import BaseCommand, COMMAND_TYPES
import subprocess


class CloseCam(BaseCommand):
    @inject
    def __init__(
        self, command_str: str, type: COMMAND_TYPES, fct: partial = None
    ) -> None:
        super().__init__(command_str, type, fct)
        self.terminate_fct = None

    def execute(self):
        # TODO: use config...
        if self.terminate_fct is not None:
            self.terminate_fct()
