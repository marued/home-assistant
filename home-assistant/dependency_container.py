from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from .state_machine import (
    keyword_state as kes,
    activation_state as acs,
    state_machine as stm,
)
from .speech_recognition import local_interpreter, sentence_matching
from .commands import command_executer, open_cam, close_cam, open_webpage, set_timer, maps_command
from .text_to_speech import computer_voice


class AppContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    # Speech to text
    sphinx_interpreter = providers.Singleton(local_interpreter.SphinxInterpreter)
    matching_model = providers.Singleton(sentence_matching.MatchingTransformerModel)

    # Text to speech
    computer_voice = providers.ThreadSafeSingleton(
        computer_voice.ComputerVoice,
        voice_name=config.voice_name,
    )

    # Declaring Commands
    close_cam = providers.ThreadSafeSingleton(
        close_cam.CloseCam,
        command_str="Close Camera",
        type=command_executer.COMMAND_TYPES.OBJECT,
    )
    open_cam = providers.ThreadSafeSingleton(
        open_cam.OpenCam,
        command_str="Open Camera",
        type=command_executer.COMMAND_TYPES.OBJECT,
        close_cam=close_cam,
    )
    web_page = providers.Factory(
        open_webpage.OpenWebpage,
        command_str=["Open web page", "Search for", "Open Google search."],
        type=command_executer.COMMAND_TYPES.OBJECT,
    )
    maps = providers.Factory(
        maps_command.SearchGoogleMaps,
        command_str=["Find nearest", "Find route", "Get directions to"],
        type=command_executer.COMMAND_TYPES.OBJECT,
    )
    timer = providers.ThreadSafeSingleton(
        set_timer.SetTimer,
        command_str="Set timer",
        type=command_executer.COMMAND_TYPES.OBJECT,
    )
    executer = providers.ThreadSafeSingleton(
        command_executer.CommandExecuter,
        sentence_matching_model=matching_model,
        command_objects=providers.List(open_cam, close_cam, web_page, maps, timer),
    )

    # Declaring app states
    activation_state = providers.Singleton(
        acs.ActivationState,
        command_executer=executer,
        interpreter=sphinx_interpreter,
        computer_voice=computer_voice,
    )
    keyword_state = providers.Singleton(
        kes.ListenForKeywordState,
        keyword=config.keyword,
        interpreter=sphinx_interpreter,
        activation_state=activation_state,
        listen_timeout=2,
        phrase_time_limit=3,
        computer_voice=computer_voice,
    )
    state_machine = providers.ThreadSafeSingleton(
        stm.StateMachine, initial_state=keyword_state
    )
