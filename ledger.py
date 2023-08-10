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
ITEMS = ('coffee','youtube','nebula','chess','podcast','icecream',
         'sport','chinese','painting','code','writing','reading',
         'task','bulletlog')
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
    print("Summary not yet implemented, calling balance!")
    balance() # dummy
    return 

def balance():
    df=read_csv(LEDGER_PATH,header=None)
    print(df[2].sum())

if __name__=="__main__":
    import sys
    from argparse import ArgumentParser
    from datetime import datetime as dt
    from pandas import read_csv

    p = ArgumentParser(prog='ledger',
                       description='keep track of spending & earning')

    p.add_argument('mode',type=str,
                   help=f'Mode must be in {MODES}')
    p.add_argument('-i','--item',dest='item',type=str,
                 help=f'Item must be in {ITEMS}')
    p.add_argument('-v','--dollar_value',dest='dollar_value',
                 type=int,default=0,
                 help=f'Dollar value earned.')
    p.add_argument('-c','--comment',dest='comment',type=str,default='',
                 help='')
    p.add_argument('-d','--disp',dest='display_mode',type=str,
                 default='summary',
                 help=f'Disp must be in {DISP}')

    args = p.parse_args()
    print(f"args {args}\n")
    assert args.mode in MODES, f'could not find {args.mode} in {MODES}'
    # conditional flow
    if args.mode=="add":
        assert args.item in ITEMS, f'could not find {args.item} in {ITEMS}'
        assert args.dollar_value!=0, f'dollar value must be set with -v,\
                --val to a non-zero value'
        timestamp = dt.now().__str__()
        append_row(timestamp,args.item,args.dollar_value,args.comment)
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
    






