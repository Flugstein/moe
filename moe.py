import speech_recognition as sr
from gtts import gTTS
from googletrans import Translator
import sounddevice as sd
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO
import subprocess
from threading import Thread
from queue import Queue
import signal
import sys
import numpy as np


def queue_record(recognizer, microphone, record_queue):
    id = 0
    while True:
        with microphone as source:
            print('{} - Recording...'.format(id))
            record = recognizer.listen(microphone)
            print('{} - Got it'.format(id))

        record_dict = {'id': id, 'record': record}
        record_queue.put_nowait(record_dict)

        id += 1

def queue_record_to_text_thread(record_queue, text_queue):
    while True:
        record_dict = record_queue.get()
        if record_dict:
            id = record_dict['id']
            record = record_dict['record']

            print('{} - Generating text...'.format(id))
            try:
                text = recognizer.recognize_google(record, language='de-DE')  # set your spoken language here
                print('{} - You said: "{}"'.format(id, text))

                text_dict = {'id': id, 'text': text}
                text_queue.put_nowait(text_dict)

            except sr.RequestError:
                print('{} - Error: API unavailable'.format(id))
            except sr.UnknownValueError:
                print('{} - Error: Unable to recognize speech'.format(id))

        record_queue.task_done()

def queue_text_to_playback_thread(text_queue, playback_queue):
    while True:
        text_dict = text_queue.get()
        if text_dict:
            id = text_dict['id']
            text = text_dict['text']

            print('{} - Generating playback for: "{}"'.format(id, text))
            text = translator.translate(text, dest='en').text  # translate generated text if needed
            speech = gTTS(text, lang='it')  # set spoken output language to speak in different accent
            mp3_fp = BytesIO()
            speech.write_to_fp(mp3_fp)
            mp3_fp.seek(0)

            playback_dict = {'id': id, 'text': text, 'playback': mp3_fp}
            playback_queue.put_nowait(playback_dict)

        text_queue.task_done()

def queue_playback_thread(playback_queue):
    while True:
        playback_dict = playback_queue.get()
        if playback_dict:
            id = playback_dict['id']
            text = playback_dict['text']
            playback = playback_dict['playback']

            print('{} - Playback: "{}"'.format(id, text))
            audio = AudioSegment.from_file(playback, format='mp3')
            sd.play(np.array(audio.get_array_of_samples()), samplerate=audio.frame_rate)

        playback_queue.task_done()


if __name__ == '__main__':

    print(sd.query_devices())
    # sd.default.device = 12  # set output device id here if you don't want to use the default device

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

    translator = Translator()

    record_queue = Queue(maxsize=0)
    text_queue = Queue(maxsize=0)
    playback_queue = Queue(maxsize=0)

    record_thread = Thread(target=queue_record, args=[recognizer, microphone, record_queue])
    record_thread.start()
    record_to_text_thread = Thread(target=queue_record_to_text_thread, args=[record_queue, text_queue])
    record_to_text_thread.start()
    text_to_playback_thread = Thread(target=queue_text_to_playback_thread, args=[text_queue, playback_queue])
    text_to_playback_thread.start()
    playback_thread = Thread(target=queue_playback_thread, args=[playback_queue])
    playback_thread.start()
