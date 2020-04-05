import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

# speech to text
with open('wit_token.txt', 'r') as f:
  wit_token = f.read()
r = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    print('Speak now...')
    playsound('ready.wav')
    audio = r.listen(source)
    playsound('done.wav')
    print('Got it')

text = r.recognize_wit(audio, wit_token)
print('You said: "{}"'.format(text))

# text to speech
speech = gTTS(text)

mp3_file = 'speech.mp3'
speech.save(mp3_file)

playsound(mp3_file)