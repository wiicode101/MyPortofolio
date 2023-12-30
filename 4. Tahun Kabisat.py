#Tahun kabisat adalah saat tanggal febuari
#mencapai angka 29, dan ini hanya terjadi
# 1x dalam 4 tahun

# Input tahun
tahun = int(input("Masukkan tahun: "))

# Cek apakah tahun kabisat atau bukan
if (tahun % 4 == 0 and tahun % 100 != 0) or (tahun % 400 == 0):
    print(f"{tahun} adalah tahun kabisat.")
else:
    print(f"{tahun} bukan tahun kabisat.")

