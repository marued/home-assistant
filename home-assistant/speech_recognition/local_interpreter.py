from typing import Any
import sounddevice as sd
import speech_recognition as sr
from dependency_injector.wiring import inject

RATE = 16000
language_code = "en-US"  # a BCP-47 language tag

fs = 44100
sd.default.samplerate = fs
sd.default.channels = 2


class SphinxInterpreter:
    @inject
    def __init__(self, timeout=5, phrase_time_limit=10) -> None:
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone(sample_rate=fs)
        self.timeout = timeout
        self.phrase_time_limit = phrase_time_limit
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)

    def listen(self, timeout=None, phrase_time_limit=None):
        timeout = timeout if timeout is not None else self.timeout
        phrase_time_limit = (
            phrase_time_limit
            if phrase_time_limit is not None
            else self.phrase_time_limit
        )
        with self.mic as source:
            return self.recognizer.listen(source, timeout, phrase_time_limit)

    def async_listen(self, call_back) -> Any:
        with self.mic as source:
            stop_listening = self.recognizer.listen_in_background(source, call_back)
        return stop_listening

    def speech_recognition(self, audio: Any) -> str:
        """
        Uses recognize_sphinx from speech_recognition lib.
        """
        speech_to_text = None
        try:
            speech_to_text = self.recognizer.recognize_sphinx(audio)
            print("Sphinx thinks you said: " + speech_to_text)
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

        return speech_to_text

    def from_sounddevice():
        """
        Other way of listening on microphone... Not used
        """
        duration = 5  # seconds
        print("Recording for {} seconds...".format(duration))
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()
        print("Done!")

        sd.play(myrecording, fs)
        sd.wait()
