from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from .state_machine import (
    keyword_state as kes,
    activation_state as acs,
    state_machine as stm,
)
from .speech_recognition import local_interpreter, sentence_matching
from .commands import command_executer, open_cam


class AppContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    sphinx_interpreter = providers.Singleton(local_interpreter.SphinxInterpreter)

    matching_model = providers.Singleton(sentence_matching.MatchingTransformerModel)

    # Declaring Commands
    open_cam = providers.Factory(
        open_cam.OpenCam,
        command_str="Open Cam",
        type=command_executer.COMMAND_TYPES.OBJECT,
    )
    executer = providers.ThreadSafeSingleton(
        command_executer.CommandExecuter, 
        sentence_matching_model=matching_model, 
        command_objects = providers.List(
            open_cam
        )
    )

    # Declaring app states
    activation_state = providers.Singleton(
        acs.ActivationState,
        command_executer=executer,
        interpreter=sphinx_interpreter,
    )
    keyword_state = providers.Singleton(
        kes.ListenForKeywordState,
        keyword=config.keyword,
        interpreter=sphinx_interpreter,
        activation_state=activation_state,
    )
    state_machine = providers.ThreadSafeSingleton(
        stm.StateMachine, initial_state=keyword_state
    )
