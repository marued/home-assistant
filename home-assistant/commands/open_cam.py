from dependency_injector.wiring import inject
from paramiko import SSHClient, AutoAddPolicy
from functools import partial
from typing import Any
from .base_command import BaseCommand, COMMAND_TYPES
from subprocess import Popen
import keyring
import json
import pathlib, os
from .close_cam import CloseCam


class OpenCam(BaseCommand):
    @inject
    def __init__(
        self,
        command_str: str,
        type: COMMAND_TYPES,
        fct: partial = None,
        close_cam: CloseCam = None,
    ) -> None:
        super().__init__(command_str, type, fct)
        file_path = os.path.join(
            pathlib.Path(__file__).parent.resolve(), "open_cam_config.json"
        )
        with open(file_path) as json_file:
            self.config = json.load(json_file)
            self.popen = None
        close_cam.terminate_fct = self.terminate

    def __connect__(run_fct):
        def run(self, command_text: str = None):
            try:
                client = SSHClient()
                client.set_missing_host_key_policy(AutoAddPolicy())
                password = keyring.get_password(
                    self.config.get("system"), self.config.get("username")
                )
                client.connect(
                    "raspberrypi.local",
                    username=self.config.get("username"),
                    password=password,
                )
                run_fct(self, client, command_text)
            finally:
                if client is not None:
                    client.close()

        return run

    @__connect__
    def terminate(self, client=None, command_text: str = None):
        print("\nClosing Cam...\n")
        if self.popen is not None:
            self.popen.terminate()

        stdin, stdout, stderr = client.exec_command("pkillall mjpg_streamer")
        print("Done.\n")

    @__connect__
    def execute(self, client, command_text: str = None):
        if self.popen is None:
            print("\nStarting Cam...\n")
            stdin, stdout, stderr = client.exec_command("./startcam.sh")
            self.popen = Popen([self.config.get("executable_path")])
            print("Done.\n")

        return self.terminate
