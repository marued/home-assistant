from dependency_injector.wiring import Provide, inject
from .dependency_container import AppContainer
from .state_machine.keyword_state import ListenForKeywordState, IState
from functools import partial

keyword = "computer"
commands = ["Open webcam.", "Close webcam.", "Open web page.", "Open youtube music.", "Set timer."]
command_ftc = [
    partial(print, "\n Opening web cam.\n"), 
    partial(print, "\n Closing web cam.\n"), 
    partial(print, "\n Opening web Page.\n"),
    partial(print, "\n Opening youtube music.\n"), 
    partial(print, "\n Setting timer.\n"), 
]

@inject
def main(keyword_state: IState = Provide[AppContainer.keyword_state]):
    state: IState = keyword_state
    state = state.handle()

if __name__ == "__main__":
    container = AppContainer()
    container.config.keyword.from_value(keyword)
    container.config.commands.from_value(dict(zip(commands, command_ftc)))
    container.wire(modules=[__name__])

    main()