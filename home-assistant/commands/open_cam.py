from dependency_injector.wiring import inject
from paramiko import SSHClient, AutoAddPolicy
from functools import partial
from typing import Any
from .base_command import BaseCommand, COMMAND_TYPES
import subprocess


class OpenCam(BaseCommand):
    @inject
    def __init__(self, command_str: str, type: COMMAND_TYPES, fct: partial = None) -> None:
        super().__init__(command_str, type, fct)

    def execute(self):
        # TODO: use config...
        try:
            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect("raspberrypi.local", username="xx", password="xxxxx")
            print("\nStarting Cam...\n")
            stdin, stdout, stderr = client.exec_command("./startcam.sh")
            subprocess.call(["xxxxx"])
            print("Done.\n")
        finally:
            client.close()
