#Membuat catatan harian
from tkinter import *
from tkinter import messagebox
from datetime import datetime
def save_note():
    note_text = text_entry.get("1.0", END)
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    note_content = f"{current_date}\n{note_text}\n{'='*30}\n"

    try:
        with open("catatan_harian.txt", "a") as file:
            file.write(note_content)
        messagebox.showinfo("Sukses", "Catatan berhasil disimpan!")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

app = Tk()
app.title("Catatan Harian")
text_entry = Text(app, height=10, width=40)
text_entry.pack(pady=10)
save_button = Button(app, text="Simpan Catatan", command=save_note)
save_button.pack(side=RIGHT)
app.mainloop()
