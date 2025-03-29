import argparse

parser = argparse.ArgumentParser(description="Meow like a cat")
parser.add_argument('-n', default=1, help='number of times to meow', type=int)
parser.add_argument('-c', help='test argument flag', action='store_true')
args = parser.parse_args()

for _ in range(args.n):
    print('Meow')

print(args.c)
