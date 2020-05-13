import psutil, subprocess
import os, signal
from PIL import Image
from PIL import ImageTk
from tkinter import Canvas, NW, CENTER
from tkinter import Tk
from PyQt5 import QtWidgets
from threading import Thread
import time


# a = psutil.process_iter(['pid', 'name'])
# for proc in a:
#     if 'chill_bro.exe' in proc.info['name']:
#         print(proc.info['pid'])
#         os.kill(proc.info['pid'], 9)

# Image._show(Image.open(r'C:\Users\cmit\Desktop\dist\resources\icon.ico'))

class Gui():
    def __init__(self):
        self.main = Tk()
        self.main.overrideredirect(True)
        self.main.wm_attributes('-topmost', 'true')
        self.main.wm_attributes('-disabled', 'true')
        self.main.wm_attributes("-transparent", "")
        self.make_center(self.main)
        self.showImg()
        self.main.mainloop()


    def showImg(self):
        load = r'..\resources\process.png'
        render = ImageTk.PhotoImage(file=load)
        canvas = Canvas(self.main, width=125, height=125)
        canvas.imageList = []
        canvas.pack(fill="both", expand=True, padx=20, pady=20)
        # canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        canvas.create_image(0, 0, anchor=NW, image=render)
        canvas.imageList.append(render)

    def make_center(self,main):
        app = QtWidgets.QApplication([])
        screen = app.primaryScreen()
        ht = screen.size().height()
        wt = screen.size().width()
        size = tuple(int(_) for _ in main.geometry().split('+')[0].split('x'))
        x = wt / 2 - size[0] / 2
        y = ht / 2 - size[1] / 2
        main.geometry("+%d+%d" % (x, y))


Gui()
print("veejey")


