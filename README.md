# MOE - Mouth of Emy
A simple speech to text to speech program that enables you to talk without revealing your voice.

## Setup
- Tested only on Windows
- Install Python packages `SpeechRecognition` `PyAudio` `gtts` `playsound`. Using conda (miniconda or anaconda) is recommend to install PyAudio since pip cannot install the dependency PortAudio on it's own.
- Make an account at https://wit.ai and put the token into `wit_token.txt`.

## Run
Run `moe.py` and start speaking after the first beep. After you stop talking the second beep marks the ending of the recording.

### Credit
Sounds made with [sfxr](http://www.drpetter.se/project_sfxr.html)