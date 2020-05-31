import psutil, win32process, win32gui, time
from threading import Thread


def active_window():
    pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    return psutil.Process(pid[-1]).name()


timeOfWin = dict()


def add_time(delta, uin):
    while uin != 'exit':
        name = active_window()
        if name in timeOfWin:
            timeOfWin[name] += delta
        else:
            timeOfWin[name] = delta
        time.sleep(delta)


u_in = input("Введите период обновления в секундах: ")
delta = float(u_in)
thr = Thread(target=add_time, args=(delta, u_in))
thr.start()
u_in = input('exit, что бы закончить.\n')
for i in timeOfWin:
    print(i, ':', timeOfWin[i])
