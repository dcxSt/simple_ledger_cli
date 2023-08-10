#!/Users/steve/Documents/code/simple_ledger/ledgerenv/bin/python
"""
This code enables you to add things to a ledger or display account summary.
There are two modes: `add` and `show`. 
Examples
-- ledger.py add --type coffee --cost 5
-- ledger.py add --type sport --revenue 5
-- ledger.py add -i coffee -c=-5
-- ledger.py show -d full
-- ledger.py show 
"""

# Valid items
ITEMS_SPEND = ('coffee','youtube','nebula','chess','podcast','icecream')
ITEMS_EARN  = ('sport','chinese','painting','code','writing','reading',
                 'task','bulletlog')
ITEMS = ITEMS_SPEND + ITEMS_EARN
# Valid modes
MODES = ('add','show')
# Valid display options
DISP = ('full','head','summary')
# Path to ledger .csv database file
LEDGER_PATH = '/Users/steve/.ledger.csv'


def append_row(timestamp:str,item:str,val:int,comment:str=''):
    with open(LEDGER_PATH,'a') as f:
        f.write(f'{timestamp},{item},{val},{comment}\n')
    return

def display_full():
    display_head(int(1e10))
    return

def display_head(n:int=10):
    with open(LEDGER_PATH,'r') as f:
        line=f.readline()
        for i in range(n):
            print(line)
            line=f.readline()
            if line=='': break
    return

def display_summary():
    df=read_csv(LEDGER_PATH,header=None)
    # Fill pie chart data arrays
    spend_y=[]
    spend_labels=[]
    for i in ITEMS_SPEND:
        amount_spent=abs(df.loc[df[1]==i][2].sum()) # all negative
        if amount_spent > 0:
            spend_y.append(amount_spent)
            spend_labels.append(f'{i} ${amount_spent}')
    earn_y =[]
    earn_labels=[]
    for i in ITEMS_EARN:
        amount_earned=df.loc[df[1]==i][2].sum() # all positive
        if amount_earned > 0:
            earn_y.append(amount_earned)
            earn_labels.append(f'{i} ${amount_earned}')
    # Plot both pie charts
    plt.ion()
    plt.subplots(1,2,figsize=(12,6))
    plt.suptitle(f'balance={df[2].sum()}')
    plt.subplot(1,2,1)
    plt.title("Spendings")
    plt.pie(spend_y,labels=spend_labels)
    plt.subplot(1,2,2)
    plt.title("Earnings")
    plt.pie(earn_y,labels=earn_labels)
    plt.show()
    plt.pause(0.1)
    input("Hit [enter] to exit")
    return 

def balance():
    df=read_csv(LEDGER_PATH,header=None)
    print(f"balance={df[2].sum()}")
    return

if __name__=="__main__":
    import sys
    from argparse import ArgumentParser
    from datetime import datetime as dt
    from pandas import read_csv
    import matplotlib.pyplot as plt

    p = ArgumentParser(prog='ledger',
                       description='keep track of spending & earning')

    p.add_argument('mode',type=str,
                   help=f'Mode must be in {MODES}')
    p.add_argument('-i','--item',dest='item',type=str,
                 help=f'Item must be in {ITEMS}')
    p.add_argument('-v','--val',dest='val',
                 type=int,default=0,
                 help=f'Dollar value earned.')
    p.add_argument('-c','--comment',dest='comment',type=str,default='',
                 help='Add a comment, type any string here.')
    p.add_argument('-d','--disp',dest='display_mode',type=str,
                 default='summary',
                 help=f'Disp must be in {DISP}')
    args = p.parse_args()
    assert args.mode in MODES, f'could not find {args.mode} in {MODES}'
    # Conditional Flow
    if args.mode=="add":
        assert args.item in ITEMS, f'could not find {args.item} in {ITEMS}'
        assert args.val!=0, f'$ value must be set & !=0 (-v, --val)'
        if args.item in ITEMS_SPEND:
            print(f"{args.item} is a sin. Interpret val as $ spent.")
            args.val = -abs(args.val)
        elif args.item in ITEMS_EARN:
            print(f"{args.item} is virtuous. Interpret val as income.")
            args.val = abs(args.val)
        else:
            raise Exception("This should never execute.")

        timestamp = dt.now().__str__()
        append_row(timestamp,args.item,args.val,args.comment)
    elif args.mode=="show":
        assert args.display_mode in DISP, f'could not find \
{args.display_mode} in DISP'
        if args.display_mode == 'full':
            display_full()
        elif args.display_mode == 'head':
            display_head()
        elif args.display_mode == 'summary':
            display_summary()
        else:
            raise Exception('This error message should never display.')
    else:
        raise Exception('This error message should never display.')
    print("Success")
    
    






