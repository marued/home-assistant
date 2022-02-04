class IState:
    def __init__(self) -> None:
        pass

    def handle(self, state_machine) -> "IState":
        raise NotImplementedError("Handle is not implemented yet.")
        return self

    def exit(self):
        return self
