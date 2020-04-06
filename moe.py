import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO

# speech to text
with open('wit_token.txt', 'r') as f:
  wit_token = f.read()
r = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    r.adjust_for_ambient_noise(source)
    print('Speak now...')
    playsound('ready.wav')
    audio = r.listen(source)
    playsound('done.wav')
    print('Got it')

# text = r.recognize_wit(audio, wit_token)
text = r.recognize_google(audio)
print('You said: "{}"'.format(text))

# text to speech
speech = gTTS(text, lang='it')

# mp3_file = 'speech.mp3'
# speech.save(mp3_file)
mp3_fp = BytesIO()
speech.write_to_fp(mp3_fp)
mp3_fp.seek(0)
play(AudioSegment.from_file(mp3_fp, format="mp3"))