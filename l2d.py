# import yahoo_historical as yh
# import datetime
# import time
import pandas as pd
import sys

pd.options.mode.copy_on_write = True

class Options:
    display_method = 1
    method = ""
    version = 103
    l2dProcessBacktest = False
    l2dProcessHits = False
    l2dProcessBuyats = False
    price_low = 0.10
    price_high = 99999.99
    date_low = 11111111
    date_high = 22222222
    debug = 0
    vol_average = 0
    vol_low = 0
    quiet = 0
    outputToFile = False
    percentage = 0.07
    percent1 = 0.07
    percent2 = 0.07
    hold_time = 1
    amt_per_trade = 1500.00
    tl_filename = "--empty--"
    out_filename = "output.csv"
    # Best ma
    periods = 250
    fastMa = 5
    slowMa = 9


class CucOptions:
    optionsDisplayMethod = 1


o = Options()


def main():
    # optionsFilename = "-empty-"
    pd.options.display.float_format = '{:.2f}'.format
    process_method()
    route_by_method()
    exit()
#######################################################################################################################


def process_bma():
    print("process bma()")
    tickers = load_tickers()
    results_count = 0
    results = []

    for tick in tickers:
        if len(tick) == 3:
            print(' ' + tick[0] + tick[1] + tick[2], end='', flush=True)
        df = pd.read_csv(f'/data/stocks/tickers/{tick}.txt', header=None)
        print("\b\b\b\b", end='', flush=True)
        total_rows = df.shape[0]
        required = o.periods + o.slowMa
        if total_rows < required:
            continue
        starting_row = total_rows - required + 1
        mf = df.loc[starting_row:total_rows]
        mf[7] = mf[4].rolling(o.fastMa).mean()
        mf[8] = mf[4].rolling(o.slowMa).mean()
        print(mf.to_string())
        print("\n")
#######################################################################################################################


def route_by_method():
    load_defaults()
    load_options(sys.argv)

    # print(f"o.method = {o.method}")
    if o.method == "l2d":
        process_l2d_options()
        exit()
    if o.method == "cuc":
        load_cuc_defaults()
        load_cuc_options()
    if o.method == "bma":
        process_bma()
#######################################################################################################################


def l2d_display_usage():
    print("USAGE:")
#######################################################################################################################


def validate_volume(df, current_row):
    if current_row < 33:
        return False
    lowest = 999_999_999
    for x in range(0, 10):  # 10 days or 30?
        if lowest > df.iloc[current_row - x, 6]:
            lowest = df.iloc[current_row - x, 6]
    return lowest > float(o.vol_low)
#######################################################################################################################


def load_tickers():
    with open(o.tl_filename) as file:
        tickers = [line.rstrip() for line in file]
    return tickers
#######################################################################################################################


def is_approved(tick, tuesday_date):
    pass
#######################################################################################################################


def l2d_process_buyats():
    print("l2dProcessBuyats")
    tickers = load_tickers()
    print(tickers)
    # with open("/home/rpendrick/stocks/trading.tl.dir.txt") as file:
    #     tickers = [line.rstrip() for line in file]
    results_count = 0
    results = []
    for tick in tickers:
        df = pd.read_csv(f'/data/stocks/tickers/{tick}.txt', header=None)
        # print(df.head())
        # print(f"rows: {df.shape[0]}")
        total_rows = df.shape[0]
        current_row = 2  # 0 indexed, 2 = Wednesday
        if o.vol_average != 0 or o.vol_low != 0:
            current_row += 30

        while current_row < total_rows:
            if int(o.date_low) <= int(df.iloc[current_row, 0]) <= int(o.date_high):
                # mondayDate = int(df.iloc[currentRow-1,0])
                monday_low = float(df.iloc[current_row - 1, 3])
                tuesday_date = int(df.iloc[current_row, 0])
                tuesday_low = float(df.iloc[current_row, 3])

                if monday_low > 0.0:
                    change = (monday_low - tuesday_low) / monday_low
                else:
                    change = 0.000001
                if change > float(o.percent1):
                    if validate_volume(df, current_row):
                        buyat = tuesday_low - (monday_low - tuesday_low)
                        if buyat >= 0.10:
                            shares = 0
                            if int(change*100) <= 8:
                                shares = float(o.amt_per_trade) / buyat
                            if int(change*100) == 9:
                                shares = ( float(o.amt_per_trade) * 1.2) / buyat
                            if int(change*100) == 10:
                                shares = ( float(o.amt_per_trade) * 1.4) / buyat
                            if int(change*100) >= 12:
                                shares = ( float(o.amt_per_trade) * 1.6) / buyat
                            shares = int(shares)
                            if (shares % 10) == 1:
                                shares -= 1
                            if (shares % 10) == 2:
                                shares -= 2
                            if (shares % 10) == 3:
                                shares += 2
                            if (shares % 10) == 4:
                                shares += 1
                            if (shares % 10) == 6:
                                shares -= 1
                            if (shares % 10) == 7:
                                shares -= 2
                            if (shares % 10) == 8:
                                shares += 2
                            if (shares % 10) == 9:
                                shares += 1
                            if record_is_valid(tick, tuesday_date):
                                print(f"{tick:6s} {tuesday_date}  {change * 100:>5.2f}%\t {buyat:>8.4f} {shares}")
                                record = []
                                record.insert(0, tick)
                                record.insert(1, tuesday_date)
                                record.insert(2, change * 100)
                                record.insert(3, buyat)
                                record.insert(4, shares)
                                results.insert(results_count, record)
                                results_count += 1
            current_row += 1
    if o.outputToFile:
        with open(o.out_filename, 'w') as f:
            for result in results:
                f.write(f"{result[0]} ")
                f.write(f"{result[1]} ")
                f.write(f"{result[2]} ")
                f.write(f"{result[3]} ")
                f.write(f"{result[4]}\n")
#######################################################################################################################


def l2d_process_hits():
    print("l2dProcessHits")
    tickers = load_tickers()
    # with open("/home/rpendrick/stocks/trading.tl.dir.txt") as file:
    #     tickers = [line.rstrip() for line in file]
    results_count = 0
    results = []
    for tick in tickers:
        df = pd.read_csv(f'/data/stocks/tickers/{tick}.txt', header=None)
        total_rows = df.shape[0]
        current_row = 2  # 0 indexed, 2 = Wednesday
        if o.vol_average != 0 or o.vol_low != 0:
            current_row += 30

        while current_row < total_rows:
            if int(o.date_low) <= int(df.iloc[current_row, 0]) <= int(o.date_high):
                # mondayDate = int(df.iloc[currentRow-2,0])
                monday_low = float(df.iloc[current_row - 2, 3])
                # tuesdayDate = int(df.iloc[currentRow-1,0])
                tuesday_low = float(df.iloc[current_row - 1, 3])
                wednesday_date = int(df.iloc[current_row, 0])
                wedneday_low = float(df.iloc[current_row, 3])

                if monday_low > 0.0:
                    change = (monday_low - tuesday_low) / monday_low
                else:
                    change = 0.000001
                if change > float(o.percent1):
                    if validate_volume(df, current_row):
                        buyat = tuesday_low - (monday_low - tuesday_low)
                        if wedneday_low <= buyat and buyat >= 0.10:
                            if record_is_valid(tick, wednesday_date):
                                print(f"{tick:6s} {wednesday_date}  {change * 100:>5.2f}%\t ${buyat:>8.4f}")
                                record = []
                                record.insert(0, tick)
                                record.insert(1, wednesday_date)
                                record.insert(2, change * 100)
                                record.insert(3, buyat)
                                results.insert(results_count, record)
                                results_count += 1
            current_row += 1
    if o.outputToFile:
        with open(o.out_filename, 'w') as f:
            for result in results:
                f.write(f"{result[0]} ")
                f.write(f"{result[1]} ")
                f.write(f"{result[2]} ")
                f.write(f"{result[3]}\n")


#######################################################################################################################


def record_is_valid(tick, date):
    with open("/home/rpendrick/stocks/trading.avoids.txt") as f:
        lines = f.read().splitlines()
    for line in lines:
        a = line.split()
        ticker = a[0]
        low_date = a[1]
        high_date = a[2]
        # reason = a[3]
        if ticker == tick and int(low_date) <= date <= int(high_date):
            # print(f"line = {ticker} {low_date} {high_date}")
            return False
    return True
#######################################################################################################################


def generate_backtest_summary(unfiltered, approved_only):
    # DataFrame = tick, drop, date, buyat, low, close, approvedT/F
    # Frames to generate are: "% below buyat", "points between buyat and close" and "percent change"
    #   with summary based on "percent change" and approved flag.
    trades = 0
    gain = 0.0
    win_count = 0
    loss_count = 0
    for i in unfiltered.index:
        if approved_only and (unfiltered.iloc[i, 6] is True):
            trades += 1
            gain += unfiltered.iloc[i, 7]

            if unfiltered.iloc[i, 7] < 0:
                loss_count += 1
            else:
                win_count += 1
            # print(f"{trades}: {unfiltered.iloc[i,7]}")
        if not approved_only:
            trades += 1
            gain += unfiltered.iloc[i, 7]
            if unfiltered.iloc[i, 7] < 0:
                loss_count += 1
            else:
                win_count += 1
            # print(f"{trades}: {unfiltered.iloc[i,7]}")
    print(unfiltered.to_string())
    if o.outputToFile:
        unfiltered.to_csv(o.out_filename, index=False)
    if trades == 0:
        print(f"\n    results:  0 (0:0)   0.0%")
    else:
        print(f"\n    results:  {trades} ({win_count}:{loss_count})   {gain / trades}%")


#######################################################################################################################


def l2d_process_backtest():
    tickers = load_tickers()
    # with open("/home/rpendrick/stocks/trading.tl.dir.txt") as file:
    #     tickers = [line.rstrip() for line in file]
    results_count = 0
    results = []
    backtestWinCount = 0
    backtestLossCount = 0
    backtestWinPct = 0.0
    backtestLossPct = 0.0
    backtestPct = 0.0

    for tick in tickers:
        # print(f"tick: {tick}")
        # show approximation of our progress through the ticker list
        # if len(tick) == 3:
        #     print(' ' + tick[0] + tick[1] + tick[2], end='', flush=True)
        df = pd.read_csv(f'/data/stocks/tickers/{tick}.txt', header=None)
        # print("\b\b\b\b", end='', flush=True)

        total_rows = df.shape[0]
        current_row = 2 + int(o.hold_time)  # 0 indexed, 2 = Wednesday --- +1 is default value (thursday) for -ht (hold time)
        if int(o.vol_average) != 0 or int(o.vol_low) != 0:
            current_row += 30
        while current_row < total_rows - int(o.hold_time) + 1:
            if int(o.date_low) <= int(df.iloc[current_row-1, 0]) <= int(o.date_high):
                mon = -1 * int(o.hold_time) - 2
                monday_low = float(df.iloc[current_row + mon, 3])
                tuesday_low = float(df.iloc[current_row + mon + 1, 3])
                wednesday_date = int(df.iloc[current_row + mon + 2, 0])
                wednesday_open = float(df.iloc[current_row + mon + 2, 1])  # 427
                wedneday_low = float(df.iloc[current_row + mon + 2, 3])
                # monday_low = float(df.iloc[current_row - 3, 3])
                # tuesday_low = float(df.iloc[current_row - 2, 3])
                # wednesday_date = int(df.iloc[current_row - 1, 0])
                # wednesday_open = float(df.iloc[current_row - 1, 1])  # 427
                # wedneday_low = float(df.iloc[current_row - 1, 3])
                thursday_close = float(df.iloc[current_row + int(o.hold_time) - 1, 4])

                if monday_low > 0.0:
                    change = (monday_low - tuesday_low) / monday_low
                else:
                    change = 0.000001
                if change > float(o.percent1):
                    if validate_volume(df, current_row-2):
                        buyat = tuesday_low - (monday_low - tuesday_low)
                        if wednesday_open < buyat:  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! DONT BUY
                            buyat = wednesday_open
                        if wedneday_low <= buyat and buyat >= 0.10 and record_is_valid(tick, wednesday_date):
                            record = []
                            record.insert(0, tick)
                            record.insert(1, change)
                            record.insert(2, wednesday_date)
                            record.insert(3, buyat)
                            record.insert(4, wedneday_low)
                            record.insert(5, thursday_close)
                            record.insert(6, record_is_valid(tick, wednesday_date))  # in if statement now - all results not avoided
                            results.insert(results_count, record)
                            results_count += 1
                            gain = (thursday_close - buyat) / buyat * 100
                            if gain >= 0.0:
                                backtestWinCount += 1
                                backtestWinPct += gain
                            else:
                                backtestLossCount += 1
                                backtestLossPct += gain
                            backtestPct += gain
                            print(f"{tick:6} {int(change * 100):2}  {wednesday_date} {buyat:8.4f} {wedneday_low:8.4f} {thursday_close:8.4f} {gain:7.2f}")
                            with open("output.out", "a") as myfile:
                                myfile.write(f"{tick:6} {int(change * 100):2}  {wednesday_date} {buyat:8.4f} {wedneday_low:8.4f} {thursday_close:8.4f} {gain:7.2f}\n")

            current_row += 1
    perTradePct = backtestPct / (backtestWinCount + backtestLossCount + .00001)
    perWinPct = backtestWinPct / (backtestWinCount + .00001)
    perLossPct = backtestLossPct / (backtestLossCount + .00001)
    print(f"trades: {backtestWinCount + backtestLossCount} ({backtestWinCount}:{backtestLossCount})   {perTradePct:.2f}% ( {perWinPct:.2f} : {perLossPct:.2f})")
    with open("output.out", "a") as myfile:
        myfile.write(
            f"trades: {backtestWinCount + backtestLossCount} ({backtestWinCount}:{backtestLossCount})   {perTradePct:.2f}% ( {perWinPct:.2f} : {perLossPct:.2f})\n")
    unfiltered = pd.DataFrame(results, columns=['Tick', 'Drop', 'Date', 'Buyat', 'Low', 'Close', 'Approved'])
    unfiltered['Gain'] = (unfiltered['Close'] - unfiltered['Buyat']) / unfiltered['Buyat'] * 100
    # print(unfiltered.to_string())
    #generate_backtest_summary(unfiltered, approved_only=False)
    #generate_backtest_summary(unfiltered, approved_only=True)
#######################################################################################################################


def process_method():
    if len(sys.argv) < 3:
        l2d_display_usage()
        exit()

    argument_number = 1
    for arg in sys.argv[1:]:
        if arg == "-m":
            o.method = sys.argv[argument_number + 1]
        argument_number += 1
#######################################################################################################################


def load_defaults():
    # read one line from file .trading.defaults.txt
    options_filename = "/home/rpendrick/stocks/trading.l2d.defaults.txt"
    with open(options_filename) as file:
        lines = [line.rstrip() for line in file]
    a = lines[0].split()
    load_options(a)
#######################################################################################################################


def load_options(opt):
    if len(opt) < 2:
        l2d_display_usage()
        exit()

    # print(f"\na = {opt}")
    argument_number = 1
    for arg in opt[1:]:
        if arg == "-p":
            o.percentage = opt[argument_number + 1]
            o.percent1 = opt[argument_number + 1]
            o.percent2 = opt[argument_number + 1]
            print("-pa found, set to " + opt[argument_number + 1])
        if opt[argument_number] == "-dm":
            o.display_method = opt[argument_number + 1]
            # print("-dm found, set to " + opt[argumentNumber + 1])
        if opt[argument_number] == "-d":
            o.debug = opt[argument_number + 1]
            # print("-d found, set to " + opt[argumentNumber + 1])
        if opt[argument_number] == "-ht":
            o.hold_time = opt[argument_number + 1]
            # print("-ht found, set to " + opt[argumentNumber + 1])
        if opt[argument_number] == "-lm":
            o.version = opt[argument_number + 1]
            # print("-lm found, set to " + opt[argumentNumber + 1])
        if opt[argument_number] == "-pa":
            o.percent1 = opt[argument_number + 1]
            # print("-pa found, set to " + opt[argumentNumber + 1])
        if opt[argument_number] == "-pb":
            o.percent2 = opt[argument_number + 1]
            # print("-pb found, set to " + opt[argumentNumber + 1])
        if opt[argument_number] == "-dl":
            o.price_low = opt[argument_number + 1]
            # print("-dl found, set to " + opt[argumentNumber + 1])
        if opt[argument_number] == "-dh":
            o.price_high = opt[argument_number + 1]
            # print("-dh found, set to " + opt[argumentNumber + 1])
        if opt[argument_number] == "-c":
            o.date_high = opt[argument_number + 1]
            o.date_low = opt[argument_number + 1]
            # print("-c found, set to " + opt[argumentNumber + 1])
        if opt[argument_number] == "-cl":
            o.date_low = opt[argument_number + 1]
            # print("-cl found, set to " + opt[argumentNumber + 1])
        if opt[argument_number] == "-ch":
            o.date_high = opt[argument_number + 1]
            # print("-ch found, set to " + opt[argumentNumber + 1])
        if opt[argument_number] == "-va":
            o.vol_average = opt[argument_number + 1]
            # print("-va found, set to " + opt[argumentNumber + 1])
        if opt[argument_number] == "-vl":
            o.vol_low = opt[argument_number + 1]
            # print("-vl found, set to " + opt[argumentNumber + 1])
        if opt[argument_number] == "-q":
            o.quiet = True
            # print("-q found, set options Quiet to True")
        if opt[argument_number] == "-a":
            o.amt_per_trade = opt[argument_number + 1]
            # print("-a found, set to " + opt[argumentNumber + 1])
        if opt[argument_number] == "-t":
            o.l2dProcessBacktest = True
            o.l2dProcessHits = False
            o.l2dProcessBuyats = False
            # print("-t found, backtesting")
        if opt[argument_number] == "-h":
            o.l2dProcessBacktest = False
            o.l2dProcessHits = True
            o.l2dProcessBuyats = False
            o.date_low = opt[argument_number + 1]
            o.date_high = opt[argument_number + 1]
            o.display_method = 5  # ?????????????????????????????????????
            # print("-h found, processing hits")
        if opt[argument_number] == "-b":
            o.l2dProcessBacktest = False
            o.l2dProcessHits = False
            o.l2dProcessBuyats = True
            o.date_low = opt[argument_number + 1]
            o.date_high = opt[argument_number + 1]
            # print("-t found, processing buyats")
        if opt[argument_number] == "-o":
            # load approp ticker list
            o.outputToFile = True
            o.out_filename = opt[argument_number + 1]
        if opt[argument_number] == "-tl":
            # load approp ticker list
            tl = opt[argument_number + 1].split(sep=",")
            for t in tl:
                # load this list t
                o.tl_filename = "/home/rpendrick/stocks/trading.tl." + t + ".txt"
        if opt[argument_number] == "-l":
            o.periods = int(opt[argument_number + 1])
            # print("-l found, set to " + opt[argumentNumber + 1])
        if opt[argument_number] == "-f":
            o.fastMa = int(opt[argument_number + 1])
            # print("-f found, set to " + opt[argumentNumber + 1])
        if opt[argument_number] == "-s":
            o.slowMa = int(opt[argument_number + 1])
            # print("-s found, set to " + opt[argumentNumber + 1])

        argument_number += 1
#######################################################################################################################


def load_cuc_defaults():
    return None
#######################################################################################################################


def load_cuc_options():
    return None
#######################################################################################################################


def print_l2d_options():
    print("-dm found, set to " + str(o.display_method))
    print("-d found, set to " + str(o.debug))
    print("-ht found, set to " + str(o.hold_time))
    print("-lm found, set to " + str(o.method))
    print("-pa found, set to " + str(o.percent1))
    print("-pb found, set to " + str(o.percent2))
    print("-dl found, set to " + str(o.price_low))
    print("-dh found, set to " + str(o.price_high))
    print("-c found, set to " + str(o.date_high))
    print("-cl found, set to " + str(o.date_low))
    print("-ch found, set to " + str(o.date_high))
    print("-va found, set to " + str(o.vol_average))
    print("-vl found, set to " + str(o.vol_low))
    print("-q found, set options Quiet to True")
    print("-a found, set to " + str(o.amt_per_trade))
    if o.l2dProcessBacktest:
        print("-t found, backtesting")
    if o.l2dProcessBuyats:
        print("-b found, processing buyats")
    if o.l2dProcessHits:
        print("-h found, processing hits")
    print("-l found, set to " + str(o.periods))
    print("-f found, set to " + str(o.fastMa))
    print("-s found, set to " + str(o.slowMa))
#######################################################################################################################


def process_l2d_options():
    if o.l2dProcessHits:
        l2d_process_hits()
    if o.l2dProcessBuyats:
        l2d_process_buyats()
    if o.l2dProcessBacktest:
        l2d_process_backtest()
#######################################################################################################################


def average(col):
    return col.mean()
#######################################################################################################################


def ticker_fixes(tick):
    # drop the column (axis=1), in place.  axis=0 when dropping a row.
    tick.drop('Adj Close', axis=1, inplace=True)
    tick['Date'] = pd.to_datetime(tick['Date'])
    tick['Date'] = tick['Date'].dt.strftime('%Y%m%d')
    tick['volume30'] = tick['Volume'].rolling(window=30).mean()
#######################################################################################################################


if __name__ == '__main__':
    main()
