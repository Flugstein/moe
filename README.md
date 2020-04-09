# MOE - Mouth of Emy
A simple speech to text to speech program that enables you to talk without revealing your voice.

## Setup
- Tested only on Windows
- Install Python packages `SpeechRecognition` `PyAudio` `gtts` `googletrans` `sounddevice` `pydub`. Using conda (miniconda or anaconda) is recommend to install PyAudio since pip cannot install the dependency PortAudio on it's own.
- Set the language parameters in `moe.py`
- If you want to use a different audio device, run `moe.py` once (will display audio devices) and set `sd.default.device` to the device id you need.

## Run
Run `moe.py`, wait a few seconds and start speaking. With a delay of ~10s the program will repeat what you said (and translate or speak with a different accent if you set the language parameters right).

## Issues
- Recording sometimes doesn't detect when you stop talking (thus increasing the delay)
- 10s delay too long

### Credit
- Thanks to Google for providing free language and speech APIs
- Based on https://realpython.com/python-speech-recognition/
- Sounds made with [sfxr](http://www.drpetter.se/project_sfxr.html)
