from dependency_injector.wiring import inject
import pyttsx3 as ttsx


class ComputerVoice:
    @inject
    def __init__(self, voice_name: str = False):
        self.engine = ttsx.init()
        voices = self.engine.getProperty("voices")
        print(
            "List of voices available: \n    ",
            "   \n".join([voice.name for voice in voices]),
        )

        for i in range(len(voices)):
            if voices[i].name == voice_name:
                self.engine.setProperty("voice", voices[i].id)
                self.engine.runAndWait()
                break

    def say(self, text: str):
        if self.engine.isBusy():
            self.engine.stop()
        self.engine.say(text=text)
        self.engine.runAndWait()
