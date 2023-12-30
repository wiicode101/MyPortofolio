#Menghitung Panjang karakter
#kalimat tidak termasuk " " (Spasi)
def hitung(kalimat):
    jumlah_karakter = len(kalimat)-kalimat.count(' ')
    return jumlah_karakter
# Input kalimat dari pengguna
kalimat = input("Masukkan kalimat: ")
# Hitung jumlah karakter
jumlah_karakter = hitung(kalimat)
# Tampilkan hasil
print(f"Jumlah karakter dalam kalimat "
      f"tersebut adalah: {jumlah_karakter}")
