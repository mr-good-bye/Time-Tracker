import psutil
import win32process
import win32gui
import time
from threading import Thread
import database as db
from appJar import gui


spisok = []


class stoppingThread:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False
        print('Terminated')

    def run(self, dt):
        global spisok
        self._running = True
        while self._running:
            name = active_window()
            a = name
            l_time = 0
            while a == name and self._running:
                time.sleep(dt)
                l_time += dt
                name = active_window()
            spisok.append((name, l_time, time.strftime('%d %m %y')))


def active_window():
    pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    return psutil.Process(pid[-1]).name()


thread = stoppingThread()
thr = ''


def pressed(val):
    global running
    global thr
    if val == "Start" and not running:
        app.setLabel("run_l", 'Running')
        app.setLabelBg("run_l", "cyan")
        thr = Thread(target=thread.run, args=(0.5,))
        thr.start()
        running = True
    elif val == "Stop" and running:
        app.setLabel("run_l", 'Not Running')
        app.setLabelBg("run_l", 'orange')
        thread.terminate()
        thr.join()
        running = False
        for i in spisok:
            db.add_time(i[0], i[1], i[2])
        db.save()
        for i in db.get():
            print(i[0], ':', i[1])


app = gui()
app.setTitle("time-tracker control")
app.setSize("300x100")
app.setResizable(canResize=False)
app.setLocation("CENTER")
app.addLabel("run_l", "Not Running", colspan=2, rowspan=1)
app.setLabelBg("run_l", "orange")
app.startFrame("LEFT", row=1, column=0)
app.addButton('Start', pressed)
app.stopFrame()
app.startFrame("RIGHT", row=1, column=1)
app.addButton('Stop', pressed)
app.stopFrame()
running = False
app.go()
