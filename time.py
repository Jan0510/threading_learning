import datetime
print(datetime.datetime.now().isocalendar())    # (2020, 45, 7)tuple(年，周，日)
print(datetime.datetime.now().isocalendar()[2]) # 日
