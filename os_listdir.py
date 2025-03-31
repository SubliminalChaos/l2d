import os

print(os.getcwd())

os.chdir('/home/rpendrick/tickers')

print(os.getcwd())

files_and_dirs = os.listdir()

for file in files_and_dirs:
    if '.txt' in file:
        print(file)

# print(os.environ)
