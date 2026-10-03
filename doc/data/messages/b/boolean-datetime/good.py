import datetime

time_now_utc = datetime.datetime.now(tz=datetime.UTC).time()

if time_now_utc > datetime.time(6, 0):
    print("Daytime!")

if time_now_utc < datetime.time(6, 0):
    print("Nighttime!")
