#!/opt/homebrew/Caskroom/miniforge/base/bin/python
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
LEDGER_PATH = '/Users/steve'


def append_row(timestamp:str,item:str,val:int,comment:str=''):
    with open(LEDGER_PATH,'a') as f:
        f.write(f'{timestamp},{item},{val},{comment}')
    return

def display_full():
    display_head(int(1e10))
    return

def display_head(n:int=10):
    with open(LEDGER_PATH,'r') as f:
        line=f.readline()
        for i in range(n):
            print(line)
            if line=='': break
    return

def display_summary():
    print("Summary not yet implemented, calling display_head!")
    display_head() # dummy
    return 

if __name__=="__main__":
    import sys
    from optparse import OptionParser
    from datetime import datetime as dt

    p = OptionParser()
    p.set_usage('ledger.py <>')

    p.add_option('-i','--item',dest='item',type='str',
                 help=f'Item must be in {ITEMS}')
    p.add_option('-v','--dollar_value',dest='dollar_value',
                 type='int',default=0,
                 help=f'Dollar value earned.')
    p.add_option('-c','--comment',dest='comment',type='str',default='',
                 help='')
    p.add_option('-d','--disp',dest='display_mode',type='str',
                 default='summary',
                 help='')

    ops, args = p.parse_args(sys.argv[1:])
    assert args!=[], f'must supply argument `mode` in {MODES}'
    mode = args[0]
    assert mode in MODES, f'could not find {mode} in {MODES}'
    # conditional flow
    if mode=="add":
        assert ops.item in ITEMS, f'could not find {ops.item} in {ITEMS}'
        assert ops.dollar_value==0, f'dollar value must be set with -v,\
                --val to a non-zero value'
        timestamp = dt.now().__str__()
        append_row(timestamp,ops.item,ops.dollar_value,ops.comment)
    elif mode=="show":
        assert ops.display_mode in DISP, f'could not find \
                {ops.display_mode} in DISP'
        if ops.display_mode == 'full': 
            display_full()
        elif ops.display_mode == 'head': 
            display_head()
        elif ops.display_mode == 'summary':
            display_summary()
        else:
            raise Exception('This error message should never display.')
    else:
        raise Exception('This error message should never display.')
    






