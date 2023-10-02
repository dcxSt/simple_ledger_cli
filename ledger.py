#!/Users/steve/Documents/code/simple_ledger/ledgerenv/bin/python
"""
This code enables you to add things to a ledger or display account summary.
There are two modes: `add` and `show`. 
Examples
   ledger.py add --type coffee --cost 5
   ledger.py add --type sport --revenue 5
   ledger.py add -i coffee -c=-5
   ledger.py show -d full
   ledger.py show 
"""

# Valid items
ITEMS_SPEND = ("coffee", "youtube", "nebula", "chess", "podcast", "icecream")
ITEMS_EARN = (
    "sport",
    "chinese",
    "painting",
    "code",
    "writing",
    "reading",
    "task",
    "bulletlog",
)
ITEMS = ITEMS_SPEND + ITEMS_EARN
# Valid modes
MODES = ("add", "show")
# Valid display options
DISP = ("full", "head", "summary")
# Path to ledger .csv database file
LEDGER_PATH = "/Users/steve/.ledger.csv"

from datetime import datetime as dt
import datetime

def parse_timestamp_string(timestamp_string):
    return dt.strptime(timestamp_string[:4+1+2+1+2+1+2+1+2+1+2], "%Y-%m-%d %H:%M:%S")


def get_yesterday_bulletlog_val():
    with open(LEDGER_PATH, "r") as f:
        lines = f.readlines()[-30:] # heuristic, not gonna be more than 30 away
    timestamp_str,item,val,_ = lines[-1].split(",")
    timestamp = parse_timestamp_string(timestamp_str)
    delta = dt.now() - timestamp
    while delta < datetime.timedelta(days=1,hours=12) and len(lines)>0:
        if item == "bulletlog":
            return int(val)
        timestamp_str,item,val,_ = lines[-1].split(",")
        timestamp = parse_timestamp_string(timestamp_str)
        delta = dt.now() - timestamp
        lines = lines[:-1]
    return 0

DEFAULT_VALUES = {
    "painting": 60,
    "bulletlog": min(5 + get_yesterday_bulletlog_val(), 30)
        }


def append_row(timestamp: str, item: str, val: int, comment: str = ""):
    with open(LEDGER_PATH, "a") as f:
        f.write(f"{timestamp},{item},{val},{comment}\n")
    return

def display_full():
    display_head(int(1e10))
    return

def display_head(n: int = 10):
    with open(LEDGER_PATH, "r") as f:
        lines = f.readlines()
    for i in lines[-n:]:
        print(i)
    return

def display_summary():
    df = read_csv(LEDGER_PATH, header=None)
    # Get pie chart data, one for spending, one for earning
    spend_y = []
    spend_labels = []
    for i in ITEMS_SPEND:
        amount_spent = abs(df.loc[df[1] == i][2].sum())  # all negative
        if amount_spent > 0:
            spend_y.append(amount_spent)
            spend_labels.append(f"{i} ${amount_spent}")
    earn_y = []
    earn_labels = []
    for i in ITEMS_EARN:
        amount_earned = df.loc[df[1] == i][2].sum()  # all positive
        if amount_earned > 0:
            earn_y.append(amount_earned)
            earn_labels.append(f"{i} ${amount_earned}")
    # Plot both pie charts
    plt.ion()
    plt.subplots(1, 2, figsize=(12, 6))
    plt.suptitle(f"Balance = ${df[2].sum()}",fontsize=24)
    plt.subplot(1, 2, 1)
    plt.title("Spendings",fontsize=18)
    plt.pie(spend_y, labels=spend_labels)
    plt.subplot(1, 2, 2)
    plt.title("Earnings",fontsize=18)
    plt.pie(earn_y, labels=earn_labels)
    plt.tight_layout()
    plt.show()
    plt.pause(0.1)
    input("Hit [enter] to exit")
    return

def balance():
    df = read_csv(LEDGER_PATH, header=None)
    print(f"balance={df[2].sum()}")
    return

if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    from datetime import datetime as dt
    from pandas import read_csv
    import matplotlib.pyplot as plt
    
    # Parse input
    p = ArgumentParser(
        prog="ledger", description="Keep track of spending & earning"
    )
    p.add_argument("mode", type=str, help=f"Mode must be in {MODES}")
    p.add_argument(
        "-i", "--item", dest="item", type=str, help=f"Item must be in {ITEMS}"
    )
    p.add_argument(
        "-v", "--val", dest="val", type=int, default=0, help=f"Dollar value earned."
    )
    p.add_argument(
        "-c",
        "--comment",
        dest="comment",
        type=str,
        default="",
        help="Add a comment, type any string here.",
    )
    p.add_argument(
        "-d",
        "--disp",
        dest="display_mode",
        type=str,
        default="summary",
        help=f"Disp must be in {DISP}",
    )
    args = p.parse_args()
    assert args.mode in MODES, f"Could not find {args.mode} in {MODES}"
    # Control flow, logic for different args
    if args.mode == "add":
        assert args.item in ITEMS, f"Couldn't find {args.item} in {ITEMS}"
        # if there's a default value and the val is not specified, add that
        if args.item in DEFAULT_VALUES.keys():
            default_val = DEFAULT_VALUES[args.item]
            if args.val == 0:
                args.val = default_val
        assert args.val != 0, f"$ value must be set and !=0 (-v, --val)"
        # Decide whether item is spending or revenue
        if args.item in ITEMS_SPEND:
            print(f"{args.item} is a sin. Interpret val {args.val} as $ spent.")
            args.val = -abs(args.val)
        elif args.item in ITEMS_EARN:
            print(f"{args.item} is virtuous. Interpret val {args.val} as income.")
            args.val = abs(args.val)
        else:
            raise Exception("This should never execute.")
        # Append row to databse
        timestamp = dt.now().__str__()
        append_row(timestamp, args.item, args.val, args.comment)
    elif args.mode == "show":
        assert (
            args.display_mode in DISP
        ), f"could not find {args.display_mode} in DISP"
        if args.display_mode == "full":
            display_full()
        elif args.display_mode == "head":
            display_head()
        elif args.display_mode == "summary":
            display_summary()
        else:
            raise Exception("This error message should never display.")
    else:
        raise Exception("This error message should never display.")
    print("Success")


