# -*- coding: utf-8 -*-
from game import *
from tkinter import *


if __name__ == "__main__":
    root = Tk()
    title = Label(root, text='Reversi', font=('Arial', 30), width=20, height=3)
    title.pack()
    btn1 = Button(root, text='human first', width=20, height=2, command=lambda: init_game(root, 0))
    btn1.place(x=125, y=130)
    btn2 = Button(root, text='AI first', width=20, height=2, command=lambda: init_game(root, 1))
    btn2.place(x=125, y=200)
    root.wm_title("Reversi")
    root.wm_geometry('400x300')
    root.mainloop()
