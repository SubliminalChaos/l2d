history = []

def lookup_date(date_to_locate) -> int:
    for i, line in enumerate(history):
        if date_to_locate == line['date']:
            return i
    return -1


with open("AAPL.txt") as file:
    for line in file:
        date, open, high, low, close, _, volume = line.rstrip().split(',')
        history.append({'date': int(date), 'open': float(open), 
                        'high': float(high), 'low': float(low),
                        'close': float(close), 'volume': int(volume)})

print(history[0]['open'])
print(type(history[0]['open']))
r = lookup_date(20250107)
print('record for 20250107 is', r)
