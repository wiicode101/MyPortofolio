#rumus Luas Segitiga L = 1/2 x a x t
def luas(alas, tinggi):
    luas = 0.5 * alas * tinggi
    return luas
# Input alas dan tinggi dari pengguna
alas = float(input("Masukkan panjang alas segitiga: "))
tinggi = float(input("Masukkan tinggi segitiga: "))

# Hitung luas segitiga
luas_segitiga = luas(alas, tinggi)

# Tampilkan hasil
print(f"Luas segitiga dengan alas {alas} dan tinggi {tinggi} adalah {luas_segitiga}")
