from gtts import gTTS
import os
input_text = input("Masukkan teks: ")
output_file_name = input("Masukkan nama file keluaran : ")
tts = gTTS(text=input_text, lang='id', slow=False)
output_directory = 'TTS_Out'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
output_file_path = os.path.join(output_directory, output_file_name + '.mp3')
tts.save(output_file_path)
os.system("start " + output_file_path)
