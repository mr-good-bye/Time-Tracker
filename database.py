import sqlite3

conn = sqlite3.connect("lttDataBase.db")
cursor = conn.cursor()



def add(app, time, date):
    cursor.execute("SELECT * FROM apps WHERE app = ? AND date = ?", (app, date))
    data = cursor.fetchone()
    if not data:
        cursor.execute("INSERT INTO apps VALUES (?,?,?)", (app, date, time))
    else:
        time += data[1]
        cursor.execute("UPDATE apps SET time = ? WHERE app = ? AND date = ?", (time, app, date))
    conn.commit()


def get(app, date):
    cursor.execute("SELECT * FROM apps WHERE app = ? AND date = ?", (app, date))
    return cursor.fetchone()


def get_all():
    cursor.execute("SELECT * FROM apps")
    return cursor.fetchall()
