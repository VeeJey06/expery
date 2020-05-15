import pyautogui
import time
from pywinauto import Application
from datetime import datetime
import pytz
from infi.systray import SysTrayIcon
import sys
from psutil import process_iter
import os
import multiprocessing
from PIL import ImageTk
from tkinter import Canvas, NW, CENTER, messagebox
from tkinter import Tk
from PyQt5 import QtWidgets


class Main(object):
    def __init__(self):
        self.app_name = 'chill_bro.exe'
        self.icon_path = os.getcwd() + os.sep + "resources"
        self.flag = 0
        self.processes = []
        self.tray_created = False

    def mov_cur(self):
        pyautogui.move(10, 100)
        pyautogui.move(-10, -100)
        pyautogui.press('esc')
        try:
            app = Application(backend='uia').connect(title_re=".*Skype*.", found_index=0, timeout=5)
        except:
            root = Tk()
            root.withdraw()
            messagebox.showerror(title="Application not found",
                                        message="Skype for bussiness is currently not running in the machine. Start Skype for Bussiness before starting chill_bro")
            root.destroy()
            root.mainloop()
            sys.exit()
        win = app.window(title_re=".*Skype*.", found_index=0, visible_only=False)
        win.set_focus()
        win.minimize()
        self.tray() if not self.tray_created else None
        self.tray_created = True
        return self.flag

    def timu(self):
        # get time in tz
        tz = pytz.timezone('Asia/Calcutta')
        dt = datetime.fromtimestamp(time.time(), tz)
        # print it
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    def quit_tray(self, systray):
        self.flag = 1
        process = multiprocessing.Process(target=Gui, args=())
        process.start()
        self.processes.append(process)
        processes = process_iter(['pid','name'])
        for process in processes:
            if self.app_name in process.info['name']:
                os.kill(process.info['pid'], 9)
        try:
            systray.shutdown()
        except:
            pass

    def tray(self):
        systray = SysTrayIcon(self.icon_path + os.sep + "icon.ico", "online daw", on_quit=self.quit_tray)
        systray.start()


class Gui(Main):
    def __init__(self):
        super().__init__()
        self.main = Tk()
        self.main.overrideredirect(True)
        self.main.wm_attributes('-topmost', 'true')
        self.main.wm_attributes('-disabled', 'true')
        self.make_center(self.main)
        self.showImg()
        self.main.mainloop()

    def showImg(self):
        load = self.icon_path + os.sep + 'process.png'
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


if __name__ == '__main__':
    obj = Main()
    log = open("debug.txt", "a")
    sys.stdout = log
    try:
        app = Application(backend='uia').connect(title_re=".*py\.exe*.", found_index=0, timeout=3)
        app.top_window().minimize()
    except Exception as e:
        print(e)
    while True:
        ret = obj.mov_cur()
        if ret == 1:
            break
        print("Enjoy the day: ", obj.timu())
        time.sleep(30)
    print('done')
    for process in obj.processes:
        process.terminate()
    sys.exit()
