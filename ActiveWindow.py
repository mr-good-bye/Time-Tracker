import psutil
import win32process
import win32gui
import time
from threading import Thread
import database as db


spisok = []


class stoppingThread:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False
        print('Terminated')

    def run(self, dt):
        global spisok
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


u_in = input("Введите период обновления в секундах: ")
delta = float(u_in)
thread = stoppingThread()
thr = Thread(target=thread.run, args=(delta,))
thr.start()
u_in = input("Введите что угодно для завершения:")
thread.terminate()
thr.join()
for i in spisok:
    db.add_time(i[0], i[1], i[2])
db.save()
for i in db.get():
    print(i[0], ':', i[1])
