from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from .state_machine import (
    keyword_state as kes,
    activation_state as acs,
    state_machine as stm,
)
from .speech_recognition import local_interpreter, sentence_matching


class AppContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    sphinx_interpreter = providers.Singleton(local_interpreter.SphinxInterpreter)

    matching_model = providers.Singleton(sentence_matching.MatchingTransformerModel)

    activation_state = providers.Singleton(
        acs.ActivationState,
        commands=config.commands,
        interpreter=sphinx_interpreter,
        sentence_matching_model=matching_model,
    )

    keyword_state = providers.Singleton(
        kes.ListenForKeywordState,
        keyword=config.keyword,
        interpreter=sphinx_interpreter,
        activation_state=activation_state,
    )

    state_machine = providers.ThreadSafeSingleton(stm.StateMachine, initial_state=keyword_state)
