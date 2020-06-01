import psutil, win32process, win32gui, time
from threading import Thread
import shelve  # Сохранение данных в файл


def active_window():
    pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    return psutil.Process(pid[-1]).name()


def time_add(name, dt):
    timeToday = time.strftime("%y%m%d.titr")
    timeOfWin = shelve.open(timeToday)
    if name in timeOfWin:
        timeOfWin[name] += dt
    else:
        timeOfWin[name] = dt
    timeOfWin.close()


def time_get():
    timeToday = time.strftime("%y%m%d.titr")
    timeOfWin = shelve.open(timeToday)
    diction = dict()
    for i in timeOfWin:
        diction[i] = timeOfWin[i]
    timeOfWin.close()
    return diction


def add_time(dt, uin):
    while uin != 'exit':
        name = active_window()
        time_add(name, dt)
        time.sleep(dt)


u_in = input("Введите период обновления в секундах: ")
delta = float(u_in)
thr = Thread(target=add_time, args=(delta, u_in))
thr.start()
u_in = input('exit, что бы закончить.\n')
result = time_get()
for i in result:
    print(i, result[i])
