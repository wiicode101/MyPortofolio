import tkinter as tk
from tkinter import *
from tkinter import ttk
import re
import wave
import pyaudio
import _thread
import time


class TextToSpeech:
    CHUNK = 1024

    def __init__(self, words_pron_dict: str = 'cmudict10pengujian.txt'):
        self._l = {}
        self._load_words(words_pron_dict)

    def _load_words(self, words_pron_dict: str):
        with open(words_pron_dict, 'r') as file:
            for line in file:
                if not line.startswith(';;;'):
                    key, val = line.split('  ', 2)
                    self._l[key] = re.findall(r"[A-Z]+", val)

    def get_pronunciation(self, str_input):
        list_pron = []
        for word in re.findall(r"[\w']+", str_input.upper()):
            if word in self._l:
                list_pron += self._l[word]
        print(list_pron)
        delay = 0
        result = '\nDiphone: {}'.format(list_pron)
        tab1_display.insert(tk.END, result)
        for pron in list_pron:
            _thread.start_new_thread(TextToSpeech._play_audio, (pron, delay,))
            delay += 0.145

    def _play_audio(sound, delay):
        try:
            time.sleep(delay)
            wf = wave.open("diphone/" + sound + ".wav", 'rb')
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

            data = wf.readframes(TextToSpeech.CHUNK)

            while data:
                stream.write(data)
                data = wf.readframes(TextToSpeech.CHUNK)

            stream.stop_stream()
            stream.close()

            p.terminate()
            return
        except:
            pass


def convert_audio1():
    text_info = text.get()
    tts.get_pronunciation(text_info)


app = Tk()
app.geometry("500x500")
app.title("Text To Speech With GTTS")

tts = TextToSpeech()

# menu
tab_control = ttk.Notebook(app)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)

tab_control.add(tab1, text="Project")
tab_control.add(tab2, text="File Process")
tab_control.add(tab3, text="About")
tab_control.pack(expand=1, fill='both')

label1 = Label(tab1, text='Text To Speech', padx=5, pady=5)
label1.grid(column=0, row=0)
label2 = Label(tab2, text='File', padx=5, pady=5)
label2.grid(column=0, row=0)
label3 = Label(tab3, text='About', padx=5, pady=5)
label3.grid(column=0, row=0)

text_field = Label(tab1, text="Masukkan Kata Disini :")
text_field.place(x=15, y=70)
text = StringVar()

text_entry = Entry(tab1, textvariable=text, width="100")
text_entry.place(x=15, y=100)

button = Button(tab1, text="Convert To Audio", command=convert_audio1, width="15", bg="#03A9F4", fg="#FFF")
button.grid(row=4, column=0, padx=10, pady=100)

tab1_display = Text(tab1)
tab1_display.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

mainloop()