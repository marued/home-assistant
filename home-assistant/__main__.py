from dependency_injector.wiring import Provide, inject
from .dependency_container import AppContainer
from .state_machine.state_machine import StateMachine, IState
from functools import partial
import sys

keyword = "computer"
commands = [
    "Open webcam.",
    "Close webcam.",
    "Open web page.",
    "Open youtube music.",
    "Set timer.",
    "Exit program.",
]
command_ftc = [
    partial(print, "\n Opening web cam.\n"),
    partial(print, "\n Closing web cam.\n"),
    partial(print, "\n Opening web Page.\n"),
    partial(print, "\n Opening youtube music.\n"),
    partial(print, "\n Setting timer.\n"),
    partial(sys.exit),
]


@inject
def main(state_machine: StateMachine = Provide[AppContainer.state_machine]):

    while state_machine.alive:
        state_machine.start()


if __name__ == "__main__":
    container = AppContainer()
    container.config.keyword.from_value(keyword)
    container.config.commands.from_value(dict(zip(commands, command_ftc)))
    container.wire(modules=[__name__])

    main()
