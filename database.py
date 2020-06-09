import sqlite3

conn = sqlite3.connect("lttDataBase.db")
cursor = conn.cursor()



def add(app, time, date):
    vals = [(app, time, date)]
    cursor.execute("SELECT * FROM apps WHERE app = {app} AND date = {date}")
    data = cursor.fetchone()
    if not data:
        cursor.execute("INSERT INTO apps VALUES (?,?,?), vals)
    else:
        time += data[1]
        cursor.execute("UPDATE apps SET time = {time} WHERE app = {app} AND date = {date}")
    conn.commit()


def get(app, date):
    cursor.execute("SELECT * FROM apps WHERE app = {app} AND date = {date}")
    return cursor.fetchone()


def get_all():
    cursor.execute("SELECT * FROM apps")
    return cursor.fetchall()
