import pandas as pd
import os.path

if not os.path.isfile("pandasBase"):
    data = pd.DataFrame(columns=['app', 'time', 'date'])
    data.to_csv("pandasBase", index=False)
else:
    data = pd.read_csv("pandasBase")


def add_time(app, time, date):
    if data[data['date'] == date].empty:
        data.loc[len(data)] = [app, time, date]
        return 1
    t_data = data[data['date'] == date]
    t_data = t_data[t_data['app'] == app]
    if t_data.empty:
        data.loc[len(data)] = [app, time, date]
        return 1
    else:
        data.loc[t_data.index] += ['', time, '']


def get():
    result = []
    for i in data.index:
        result.append([data.iloc[i]['app'], data.iloc[i]['time'], data.iloc[i]['date']])
    return result


def save():
    data.to_csv("pandasBase", index=False)
