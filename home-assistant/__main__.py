from dependency_injector.wiring import Provide, inject
from .dependency_container import AppContainer
from .state_machine.state_machine import StateMachine
import os

keyword = "computer"


@inject
def main(state_machine: StateMachine = Provide[AppContainer.state_machine]):

    while state_machine.alive:
        state_machine.start()


if __name__ == "__main__":
    # command_yml = "./command_list.yml"
    # command_yml = os.path.abspath(
    #    os.path.join(os.path.dirname(__file__), command_yml)
    # ),

    container = AppContainer()
    container.config.keyword.from_value(keyword)
    container.wire(modules=[__name__])

    main()
