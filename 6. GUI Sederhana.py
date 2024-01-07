#GUI "HALLO, Nama"
from tkinter import *
def on_button_click():
    label_out.config(text="Halo, " + entry.get())
app = Tk()
app.geometry("300x100")
app.title("GUI Sederhana")
label = Label(app, text="Masukkan nama:")
label.pack()
entry = Entry(app)
entry.pack()
button = Button(app, text="Klik saya!", command=on_button_click)
button.pack()
label_out = Label(app, text="")
label_out.pack(side=BOTTOM)
app.mainloop()
