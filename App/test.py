import tkinter as tk
from datalist import DataList
from styles import Theme

app = tk.Tk()
app.geometry("500x500")
app.config(background=Theme().background)

data = [x+1 for x in range(100)]

frame = tk.Frame(app, background=Theme().background)
frame.pack()

d = DataList(frame, data)

app.mainloop()