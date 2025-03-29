import argparse

parser = argparse.ArgumentParser(description="Meow like a cat")
parser.add_argument('-dm', default=1, help='display method', type=int)
parser.add_argument('-m', default=1, help='l2d method', type=int)
parser.add_argument('-v', 0.01, help='version', type=float)
parser.add_argument('-n', default=1, help='number of times to meow', type=int)
parser.add_argument('-b', help='process l2d buyats', action='store_true')
parser.add_argument('-h', help='process l2d hits', action='store_true')
parser.add_argument('-t', help='process l2d backtest', action='store_true')
parser.add_argument('-dl', 0.15, help='dollar low value', type=float)
parser.add_argument('-dh', 999.99, help='dollar high value', type=float)
parser.add_argument('-cl', 19900100, help='calendar low date', type=int)
parser.add_argument('-ch', 20291232, help='calendar high date', type=int)
parser.add_argument('-d', 1, help='debug level', type=int)
args = parser.parse_args()

for _ in range(args.n):
    print('Meow')

print(args.t)


    # vol_average = 0
    # vol_low = 0
    # quiet = 0
    # outputToFile = False
    # percentage = 0.07
    # percent1 = 0.07
    # percent2 = 0.07
    # hold_time = 1
    # amt_per_trade = 1500.00
    # tl_filename = "--empty--"
    # out_filename = "output.csv"
    # # Best ma
    # periods = 250
    # fastMa = 5
    # slowMa = 9
