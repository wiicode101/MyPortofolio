# Import Library
import bs4 as bs
import urllib.request
# Tokenisasi dengan NLTK
import nltk
# Download package punkt
nltk.download('punkt')
#import pandas as pd

# Scraping data artikel tentang Kucing di Wikipedia
wiki_data = urllib.request.urlopen('https://id.wikipedia.org/wiki/Joko_Widodo').read()
#data=open('filename.txt')

# Menemukan keseluruhan paragraf html dari laman web
wiki_data_paragraphs  = bs.BeautifulSoup(wiki_data,'lxml').find_all('p')

# Membuat korpus dari keseluruhan paragraf artikel di situs web
wiki_text = ''
# Membuat korpus teks huruf kecil pada paragraf tentang kucing
for p in wiki_data_paragraphs:
    wiki_text += p.text.lower()

# Regular Expressions
import re

wiki_text = re.sub(r'\s+', ' ', re.sub(r'\[[0-9]*\]', ' ', wiki_text))

wiki_sentences = nltk.sent_tokenize(wiki_text)

# TF-IDF Algorithm
from sklearn.feature_extraction.text import TfidfVectorizer
# Cosine Similartity
from sklearn.metrics.pairwise import cosine_similarity

def chatbot_response(user_query):
  # Menambahkan kueri ke sentences list atau daftar kalimat
  wiki_sentences.append(user_query)
  # Membuat basis vektor kalimat ke dalam list
  vectorizer = TfidfVectorizer()
  sentences_vectors = vectorizer.fit_transform(wiki_sentences)
  #Mengukur cosine similarity dan ambil indeks terdekat yang kedua
  #karena indeks pertama adalah masukkan teks kueri atau permintaan user
  vector_values = cosine_similarity(sentences_vectors[-1], sentences_vectors)
  answer = wiki_sentences[vector_values.argsort()[0][-2]]
  #Pemeriksaan akhir untuk memastikan adanya hasil atau respon bot.
  #Jika keseluruhannya bernilai 0, maka teks yang di input tidak terdapat dalam korpus
  input_check = vector_values.flatten()
  input_check.sort()

  if input_check[-2] == 0:
    return "Mohon dicoba lagi yaa"
  else:
    return answer

print("Halo, saya Wiki-Bot. Apakah kamu punya pertanyaan seputar Bapak Jokowi?:")
while(True):
  query = input().lower()
  if query not in ['bye', 'goodbye', 'take care', 'sayonara', 'dadah']:
    print("wiki-Bot: ", end="")
    print(chatbot_response(query))
    wiki_sentences.remove(query)
  else:
    print("See You Again!")
    break