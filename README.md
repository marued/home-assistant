# home-assistant
Home-assistant is an application that can respond to custom voice commands, mutch like a Google Home or Alexa. No internet connection is required, since by default all the necessary models run locally. It's possible to configure your activation word and to add new voice commands to the application. 

By default, this uses 'pocketsphinx' to do the voice to text. It's possible to configure it to use Google API for better results, but by default it will download an open source model to run locally. For the voice to command, the library 'sentence-transformers' from HuggingFace is used to generate sentence embeddings to enable command matching. This is equivelent to a zero shot classification.  

# Getting started
This project uses [Poetry](https://python-poetry.org/docs/) as a package management tool. 
To get started:
```
$ cd home-assistant
$ poetry install
```
To run the application:
```
$ poetry run home-assistant
# or
$ poetry run python -m home-assistant
```
Once it's started, the default voice activation command is 'Hello Charlie'. 

## Windows installation
Some of the packages are not always installed properly on windows and may cause errors. The fallowing packages can be found on the following links and installed by referencing the .whl file downloaded manually.
### Pocketsphinx: Sound to text
Get the .whl here for windows:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pocketsphinx

### Pyaudio: Sound capture (optional)
Get the .whl here for windows:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

### Pyttsx3: text to voice
If you recieve errors such as No module named win32com.client, No module named win32, or No module named win32api, you will need to additionally install pypiwin32.

# License
[MIT](https://github.com/marued/home-assistant/blob/main/LICENSE)
