# Library
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import re
from tkinter import ttk
import wave
import pyaudio
import time
import soundfile as sf

# Variabel global untuk menyimpan lokasi file korpus
WORDS_PRON_DICT = ''
# Ukuran buffer atau blok data adalah 1024 byte
CHUNK = 1024


def remove_punctuation(text):
    text_with_space = text.replace('-', ' ')
    text_without_punctuation = re.sub(r'[^\w\s]', '', text_with_space)
    return text_without_punctuation


def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text, pattern, start=0, end=None):
    if end is None:
        end = len(text)

    M = len(pattern)
    N = end

    lps = compute_lps(pattern)
    i = start
    j = 0

    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1

            if j == M:
                return True
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return False


# Fungsi untuk mencari pola dalam sebuah file
def search_in_file(pattern, file_path):
    with open(file_path, 'r') as file:
        text = file.read().replace('\n', '')
        return pattern in text

# Fungsi mencari file

# Fungsi Kategorisasi Fonem
def kategorisasi_fonem(missing_words, file_path):
    # Definisi Vokal, Konsonan, difthong, konsonan gabungan, dan fonem 3 huruf


    v = ['a', 'i', 'u', 'e', 'o']
    k = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
    v2 = ['ai', 'au', 'oi']
    k2 = ['kh', 'ng', 'ny', 'sy']
    f3 = ['kan', 'nga', 'nya', 'sya', 'nyi', 'nyo', 'tya', 'syu', 'ter', 'ber', 'per', 'pem', 'pri', 'tur',
          'tes', 'pan', 'vei', 'sur', 'men', 'lah']

    #memisahkan kata per kata
    for word in missing_words:
        fonem_awal = []
        fonem_akhir = []
        fonem_tengah = []
        fonem_3 = []

        #mengecek apakah ada fonem 3 huruf dalam kata
        for fonem in f3:
            if kmp_search(word, fonem):
                fonem_3.append(fonem)

        #menghitung panjang string kata tersisa setelah dikurangi panjang fonem 3 huruf(Jika ada)
        remaining_letters = len(word) - (len(fonem_3) * 3)

        #Menentukan Fonem pertama
        if remaining_letters != 0:
            # kondisi string tersisa = Ganjil
            if remaining_letters % 2 == 1:
                # kondisi huruf pertama = vokal, 3 huruf pertama bukan fonem 3 huruf
                if word[0] in v and word[0:3] not in f3:
                    #melakukan pengecekan pada huruf ke 2 dan ke 3 merupakan KK (konsonan konsonan) yang bukan konsonan gabungan
                    #input "indonesia" output : ["in"]
                    if word[1] in k and word[2] in k and word[1:3] not in k2:
                        fonem_awal.append(word[0:2])
                    if word[1] in v and word[0:2] in v2:
                        fonem_awal.append(word[0:2])
                    # input "angsa" output : ["a"], karena walaupun 'n','g' merupakan konsonan namun ia masuk dalam k2
                    else :
                        fonem_awal.append(word[0])

                # kondisi huruf pertama = konsonan, 3 huruf pertama bukan fonem 3 huruf
                elif word[0] in k and word[0:3] not in f3:
                    #melakukan pengecekan huruf ke 2 dan ke 3 merupakan VV (vokal vokal)
                    if word[1] in v and word[2] in v:
                        fonem_awal.append(word[0:2])
                    # kondisi panjang string >3 : pengecekan huruf ke 2,3, dan 4 merupakan VKK (vokal konsonan konsonan)
                    # input "contoh" output : ["co", "n~"]
                    elif len(word) > 3 and word[1] in v and word[2] in k and word[3] in k and word[2:4] not in k2:
                        fonem_awal.append(word[0:2])
                        fonem_awal.append(word[2]+"~")
                    #mengatasi jika pola = KVKV / KK+
                    else:
                        fonem_awal.append(word[0:2])

                # kondisi 3 huruf pertama merupakan fonem 3 huruf
                else:
                    fonem_awal.append(word[0:3])

            # kondisi string tersisa = Genap
            else:
                #memastikan 3 huruf pertama bukan fonem 3 huruf
                if word[0:3] not in f3:
                    #memastikan tidak terjadi pola VV (vokal vokal) yang bukan difthong
                    if word[0] in v and word[1] in v and word[0:2] not in v2:
                        fonem_awal.append(word[0])
                    #memastikan tidak terjadi pola KK pada karakter ke 3 dan 4
                    elif len(word)>3 and word[0] in k and word[1] in v and word[2] in k and word[3] in k and word[2:4] not in k2:
                        fonem_awal.append(word[0:2])
                        fonem_awal.append(word[2]+"~")
                    # mengatasi selain pola VV, seperti VK KV
                    else:
                        fonem_awal.append(word[0:2])
                #kondisi 3 huruf pertama merupakan fonem 3 huruf
                else:
                    fonem_awal.append(word[0:3])

        #kondisi 3 huruf pertama merupakan fonem 3 huruf
        else:
            fonem_awal.append(word[0:3])

        #menghitung sisa string tersisa setelah dikurang jumlah string fonem pertama
        first_fonem = 0
        for fonem in fonem_awal:
            if "~" in fonem:
                first_fonem += len(fonem) - 1
            else:
                first_fonem += len(fonem)

        remaining_letters2 = len(word) - first_fonem

        #kondisi huruf tersisa belum habis
        if remaining_letters2 != 0:
            #kondisi string tersisa = ganjil
            if remaining_letters2 % 2 == 1:
                #kondisi 3 huruf terakhir bukan merupakan fonem 3 huruf
                if word[-3:] not in f3:
                    #kondisi huruf terakhir = vokal
                    if word[-1] in v:
                        #kondisi 2 dan 3 huruf terakhi memenuhi pola KK yang bukan merupakan konsonan gabungan
                        if word[-2] in k and word[-3] in k and word[-3:-1] not in k2:
                            fonem_akhir.append(word[-2:])
                        else:
                            fonem_akhir.append(word[-1])

                    #kondisi huruf terakhir = konsonan
                    else:
                        #menciptakan ruang fonem tengah sementara
                        area_ft = word[first_fonem:len(word) - 1]
                        i = 0
                        ft3 = []

                        #melakukan pengecekan karakter di ruang fonem tengah
                        for char in area_ft:
                            #melakukan pengecekan apakah ada fonem 3huruf di ruang fonem tengah
                            if i + 3 <= len(area_ft) and area_ft[i:i + 3] in f3:
                                ft3.append(area_ft[i:i + 3])
                                i += 3
                            #kondisi ditemukan fonem 3huruf pada ruang fonem tengah
                        if ft3:
                            #kondisi jumlah string fonem 3 huruf = ganjil
                            if len(ft3) % 2 == 1:
                                fonem_akhir.append(word[-2:])
                            #kondisi jumlah string fonem 3 huruf = genap
                            else:
                                fonem_akhir.append(word[-1:] + "~")
                            #kondisi tidak ditemukan fonem 3 huruf pada ruang fonem tenggah
                        else:
                            fonem_akhir.append(word[-1:] + "~")
                #kondisi 3 huruf terakhir merupakan fonem 3 huruf
                else:
                    #memastikan tidak terjadi kondisi vv pada 4 dan 5 karakter terakhir yang bukan difthong
                    if remaining_letters2 > 4 and word[-4] in v and word[-5] in v and word[-5:-3] not in v2:
                        fonem_akhir.append(word[-4:-2])
                        fonem_akhir.append(word[-2:])
                    elif remaining_letters2 > 2 and word[-3:] in f3:
                        fonem_akhir.append(word[-3:])
                    #kondisi apabila string tersisa tidak sampai <3
                    else:
                        fonem_akhir.append(word[-2:])

            #kondisi string tersisa = genap
            else:
                # kondisi 3 huruf terakhir bukan merupakan fonem 3 huruf
                if word[-3:] not in f3:
                    if remaining_letters2 > 4 and word[-3] in v and word[-4] in v and word[-4:-2] not in v2 or remaining_letters2 > 4 and word[-3] in k and word[-4] in k and word[-4:-2] not in k2:
                        fonem_akhir.append(word[-3:-1])
                        if word[-1:] in k:
                            fonem_akhir.append(word[-1:]+"~")
                        else:
                            fonem_akhir.append(word[-1:])
                    else:
                        fonem_akhir.append(word[-2:])
                #kondisi 3 huruf terakhir merupakan fonem 3 huruf
                else:
                    # memastikan tidak terjadi kondisi vv pada 4 dan 5 karakter terakhir yang bukan difthong
                    if remaining_letters2 > 4 and word[-4] in v and word[-5] in v and word[-5:-3] not in v2:
                        fonem_akhir.append(word[-4:-2])
                        fonem_akhir.append(word[-2:])
                    elif remaining_letters2 > 2 and word[-3:] in f3:
                        fonem_akhir.append(word[-3:])
                    # kondisi apabila string tersisa tidak sampai <3
                    else:
                        fonem_akhir.append(word[-2:])

        #menghitung panjang string fonem akhir
        last_fonem = 0
        for fonem in fonem_akhir:
            if "~" in fonem:
                last_fonem += len(fonem) - 1
            else:
                last_fonem += len(fonem)

        #menghitung ruang fonem tengah
        area_ft = word[first_fonem:len(word) - last_fonem]
        if area_ft:

            i = 0

            #fungsi semua karakter di ruang fonem tengah
            for char in area_ft:
                #mengecek setiap 3 karakter dalam area fonem tengah, dan mengecek apakah itu merupakan fonem 3?
                if i + 3 <= len(area_ft) and area_ft[i:i + 3] in f3:
                    fonem_tengah.append(area_ft[i:i + 3])
                    i += 3
                else:
                    if i + 3 <= len(area_ft):
                        if (area_ft[i] in v and area_ft[i+1] in v and area_ft[i:i + 2] not in v2) or (area_ft[i] in k and area_ft[i+1] in k and area_ft[i:i + 2] not in k2):
                            fonem_tengah.append(area_ft[i])
                            i += 1
                        else:
                            fonem_tengah.append(area_ft[i:i + 2])
                            i += 2
                    else:
                        fonem_tengah.append(area_ft[i:i + 2])
                        i += 2

            for i, fonem in enumerate(fonem_tengah):
                if len(fonem) == 1 and fonem in k:
                    fonem_tengah[i] = fonem + "~"



        #memastikan tidak ada fonem kosong
        fonem_awal = [item for item in fonem_awal if item != ""]
        fonem_tengah = [item for item in fonem_tengah if item != ""]
        fonem_akhir = [item for item in fonem_akhir if item != ""]


        if fonem_tengah and fonem_akhir:
            if "~" in fonem_tengah[-1] and fonem_akhir[0] in v:
                fonem_tengah.pop()
                fonem_akhir.pop()
                fonem_akhir.append(word[-2:])


        def clean_and_combine(fonem_list):
            #Bersihkan list dari item kosong dan gabungkan dengan tanda +
            return "+".join([item for item in fonem_list if item != ""])

        # Gabungkan semua fonem yang ada
        combined_fonem = []
        for fonem in [fonem_awal, fonem_tengah, fonem_akhir]:
            if fonem:
                combined_fonem.append(clean_and_combine(fonem))

        content = word + "  " + "+".join(combined_fonem)

        with open(file_path, 'a') as file:
            file.write(content + "\n")

    return "Kata berhasil ditambahkan ke dalam korpus."


def run_search():
    loaded_words = load_words(WORDS_PRON_DICT)
    # kalimat = kalimat_entry.get()
    kalimat = kalimat_entry.get('1.0', 'end-1c')
    corpus_file_path = corpus_file_entry.get()

    kalimat = kalimat.lower()
    kalimat_without_punctuation = remove_punctuation(kalimat)
    kata_kata = kalimat_without_punctuation.split()

    file_path = corpus_file_path
    found_words = []
    missing_words = []

    with open(file_path, 'r') as file:
        lines = file.read().split("\n\n")
        for line in lines:
            words = line.split()
            for word in words:
                found_indices = kmp_search(kalimat_without_punctuation, word.lower())
                if found_indices:
                    found_words.append(word)
                else:
                    missing_words.append(word)
    missing_words = list(set(kata_kata) - set(found_words))

    if missing_words:
        result_label.config(text="Kata yang tidak ditemukan dalam korpus: " + ", ".join(missing_words))
        response = messagebox.askquestion("Konfirmasi",
                                          "Apakah Anda yakin kata-kata tersebut merupakan bahasa Indonesia? Apakah Anda ingin menambahkannya ke dalam korpus?")
        if response == 'yes':
            result_message = kategorisasi_fonem(missing_words, file_path)
            result_label.config(text=result_message)
        else:
            print("Kata tidak ditemukan dalam korpus, pastikan kata merupakan bahasa Indonesia.")
    else:
        result_label.config(text="Semua kata ditemukan dalam korpus.")



# Fungsi untuk memuat kata-kata dari file korpus
def load_words(words_pron_dict):
    corpus = {}
    with open(words_pron_dict, 'r') as file:
        for line in file:
            if not (line.startswith(';;;') or line.strip() == ''):
                # Lakukan sesuatu dengan baris yang tidak merupakan komentar atau baris koson
                key, val = line.split('  ', 2)
                corpus[key] = re.findall(r"[\w~#]+", val)
    return corpus

def get_pronunciation(corpus, str_input):
    list_pron = []
    list_corpus =[]
    # print(str_input) #terbaca
    x = re.sub(r"\s+", ' # ', str_input)
    str_input = x

    for word in re.findall(r"[\w#]+", str_input.lower()):  # ambil tiap kata
        if word in corpus:  # cek kata ada dalam corpus? tidak terdeteksi
            list_pron.extend(corpus[word])
        else:
            print("word tidak terbaca di corpus")

    delay = 0.145
    result = '\nFonem: {}'.format(list_pron)
    tab1_display.insert(tk.END, result)


    for pron in list_pron:
        sound_fonem = play_audio(pron, delay)

# Fungsi untuk memainkan audio berdasarkan fonem
def play_audio(sound, delay):
    try:
        time.sleep(delay)
        wf = wave.open("Fonem/" + sound + ".wav", 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(CHUNK)

        while data:
            stream.write(data)
            data = wf.readframes(CHUNK)

        stream.stop_stream()
        stream.close()

        p.terminate()

        return wf
    except:
        pass

# Fungsi untuk mengonversi teks menjadi audio
def convert_audio1():
    loaded_words = load_words(WORDS_PRON_DICT)
    # text_info = text.get()
    text_info = kalimat_entry.get('1.0', 'end-1c')
    get_pronunciation(loaded_words, text_info)
# Fungsi untuk menyimpan audio
def save_audio(corpus,str_input):
    list_pron = []
    dir_fon = "E:\AI\Sistem Terbaru fix\Fonem"
    dir_out = "E:\AI\Sistem Terbaru fix\Output"
    #print(corpus) #terbaca
    x = re.sub(r"\s+", ' # ', str_input)
    str_input = x
    for word in re.findall(r"[\w#]+", str_input.lower()):  # ambil tiap kata
        if word in corpus:  # cek kata ada dalam corpus? tidak terdeteksi
            list_pron.extend(corpus[word])
        else:
            print("word tidak terbaca di corpus")

    output_audio = []

    for file in list_pron:
        audio_data, _ = sf.read(os.path.join(dir_fon, f'{file}.wav'))
        output_audio.append(audio_data)

    combined_audio = output_audio[0]
    delay = 0.145

    for audio_data in output_audio[1:]:

        silent_samples = int(delay * 44100)  # Assuming a sample rate of 44100 Hz
        silence = [0.0] * silent_samples
        combined_audio = list(combined_audio) + silence + list(audio_data)
          # Menambahkan penundaan untuk fonem berikutnya

    output_filename = f'{str_input}.wav'  # Tambahkan ekstensi .wav
    output_file = os.path.join(dir_out, output_filename)
    sf.write(output_file, combined_audio, 44100)  # Writing the combined audio data

# Fungsi mengeksekusi penyimpanan audio
def saved():
    loaded_words = load_words(WORDS_PRON_DICT)
    # text_info = text.get()
    text_info = kalimat_entry.get('1.0', 'end-1c')
    save_audio(loaded_words,text_info)

def clear_text():
    tab1_display.delete(1.0, tk.END)
def browse_corpus_file():
    global WORDS_PRON_DICT
    file_path = filedialog.askopenfilename(title="Select Corpus File", filetypes=[("Text Files", "*.txt")])
    WORDS_PRON_DICT = file_path
    corpus_file_entry.delete(0, tk.END)
    corpus_file_entry.insert(tk.END, file_path)

def retrieve_input():
    global text
    text = kalimat_entry.get('1.0', 'end-1c')

def mulai():
    retrieve_input()
    browse_corpus_file()

# Membuat jendela utama aplikasi
root = tk.Tk()
root.title("TTS With Kategorisasi Fonem")
root.geometry("650x500")

# Membuat tab menggunakan ttk.Notebook
tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text="Project")
tab_control.pack(expand=1, fill='both')

# Membuat elemen-elemen GUI
kalimat_label = tk.Label(tab1, text="Masukkan kalimat:")
kalimat_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
kalimat_entry = tk.Text(tab1,height=5, width=37)
kalimat_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W)
save_var = tk.Button(tab1, text = 'Save to Variable "text"', command = retrieve_input)


corpus_file_label = tk.Label(tab1, text="Lokasi Corpus File:")
corpus_file_entry = tk.Entry(tab1, width=50)
corpus_file_entry.insert(tk.END, "Pilih Corpus Dulu ^_*")
corpus_file_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
corpus_file_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

corpus_file_button = tk.Button(tab1, text="Browse", command=mulai)
search_button = tk.Button(tab1, text="Cek Corpus", command=run_search)
corpus_file_button.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
search_button.grid(row=0, column=2, padx=5, pady=5,sticky=tk.W)


result_label = tk.Label(tab1, text="", wraplength=400)
result_label.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

tab1_display = tk.Text(tab1)
tab1_display.grid(row=7, column=0, columnspan=3, padx=5, pady=5)
button = tk.Button(tab1, text="Convert To Audio", command=convert_audio1, width="15", bg="#03A9F4", fg="#FFF")
button.grid(row=2, column=0, padx=5, pady=10,sticky=tk.W)
button = tk.Button(tab1, text="Save Audio", command=saved, width="15", bg="#03A9F4", fg="#FFF")
button.grid(row=2, column=1, padx=5, pady=10,sticky=tk.W)
clear_button = tk.Button(tab1, text="Clear", command=clear_text)
clear_button.grid(row=2, column=2, padx=5, pady=0,sticky=tk.W)

# Menjalankan loop utama GUI
tab1.mainloop()
