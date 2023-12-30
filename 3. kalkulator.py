#Membuat Kalkulator BMI
#BMI = Berat/(tinggi)^2
def bmi(berat_badan, tinggi_badan):
    bmi = berat_badan / (tinggi_badan ** 2)
    return bmi
# Input berat badan dan tinggi badan dari pengguna
berat_badan = float(input("Masukkan berat badan (kg): "))
tinggi_badan = float(input("Masukkan tinggi badan (m): "))
# Hitung BMI
bmi = bmi(berat_badan, tinggi_badan)
if bmi <= 18.5:
    status = "Kurus"
elif bmi < 25:
    status = "Normal"
elif bmi < 28:
    status = "Gemuk"
else:
    status = "Obesitas"
# Tampilkan hasil
print(f"BMI Anda adalah: {bmi}")
print(f"Status Berat Anda adalah: {status}")
