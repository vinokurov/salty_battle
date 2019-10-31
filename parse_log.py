import pandas

LOG_PATH = 'c:/Users/vnkrv/Downloads/salty_battle_log.txt'

datetime_start = None

with open(LOG_PATH, 'r') as fp:
    line = fp.readline()
    fields = line.split(' - ')
    datetime_start = pandas.to_datetime(fields[0])
    while line:
        fields = line.split(' - ')
        dt = pandas.to_datetime(fields[0])
        no_second = (dt-datetime_start).seconds
        if 'STARTED' in fields[-1] or 'STOPPED' in fields[-1]:
            print(f'[{no_second}, "{fields[-1].strip()}"],')
        elif 'left' in fields[-1]:
            print(f'[{no_second}, {fields[-1].strip()}],')
        line = fp.readline()
