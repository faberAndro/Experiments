import datetime as d

birthday_date = "23-10"
f = []
for tempo in range(2016,2066):
    t = str(tempo)
    birthday_future = birthday_date + '-' + t
    try:
        b = d.datetime.strptime(birthday_future, '%d-%m-%Y')
        if b.weekday() in [4,5,6]:
            c = b.strftime('%a-%Y')
            f.append(c)
    except:
        pass
    # check if this year the day is within a weekend
    # ritorna il giorno della settimana
future_dates = ' '.join(f)
print(future_dates)
