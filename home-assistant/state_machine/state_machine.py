from dependency_injector.wiring import inject
from .IState import IState


class StateMachine:
    @inject
    def __init__(self, initial_state: IState) -> None:
        self.state = initial_state
        self.previous_state: IState = None
        self.alive = True

    def start(self):
        self.state.handle(self)

    def change_state(self, new_state: IState):
        self.state.exit()
        self.previous_state = self.state
        self.state = new_state

    def fall_back(self):
        if self.previous_state is not None:
            try:
                self.state.exit()
            except:
                print("Unable to exit state properly...")
            self.state = self.previous_state
            self.previous_state = None
            if self.state is None:
                self.alive = False
