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
ITEMS = ('coffee','youtube','nebula','','','','','','','','','','')
# Valid modes
MODES = ('add','show')
# Valid display options
DISP = ('full','head','summary')
# Path to ledger .csv database file
LEDGER_PATH = ''


def append_row(timestamp:str,item:str,val:int,comment:str=''):
    with open(LEDGER_PATH,'a') as f:
        f.write(f'{timestamp},{item},{val},{comment}')

if __name__=="__main__":
    import sys
    from optparse import OptionParser
    from datetime import datetime as dt

    p = OptionParser()
    p.set_usage('ledger.py <>')

    p.add_option('-i','--item',dest='item',type='',help='')
    p.add_option('-v','--val',dest='dollar_value',type='',help='')
    p.add_option('-c','--comment',dest='comment',type='str',default='',help='')
    p.add_option('-d','--disp',dest='',type='str',default='summary',help='')
    p.add_option('-','--',dest='',type='',help='')
    p.add_option('-','--',dest='',type='',help='')

    # asserts

    # conditional flow
    






