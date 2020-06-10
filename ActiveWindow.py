import psutil
import win32process
import win32gui
import time
from threading import Thread
import database as db


spisok = []
s_thread = False


def active_window():
    pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    return psutil.Process(pid[-1]).name()


def add_time(dt):
    while True:
        name = active_window()
        global s_thread
        a = name
        l_time = 0
        while a == name:
            l_time += dt
            name = active_window()
            time.sleep(dt)
            if s_thread:
                break
        spisok.append((name, l_time, time.strftime('%d %m %y')))
        if s_thread:
            break


u_in = input("Введите период обновления в секундах: ")
delta = float(u_in)
thr = Thread(target=add_time, args=(delta,))
thr.start()
u_in = input("Введите что угодно для завершения:")
s_thread = True
for i in spisok:
    db.add_time(i[0], i[1], i[2])
db.save()
for i in db.get():
    print(i[0], ':', i[1])
