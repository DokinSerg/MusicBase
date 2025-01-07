import os,sys
from glob import glob
from rich import print as rpn
from shutil import copy
try:
    spath = 'E:\\!MP3\\'

    rez = sorted(os.listdir(spath))
    for n, item in enumerate(rez):
        newdir  = f'H:\\{n//50:0>2}'
        curfile = os.path.join(spath,item)
        if not os.path.isfile(curfile):continue #А вдруг это папка или симлинк
        # rpn(f'[khaki1]{newdir}')
        if not os.path.isdir(newdir):
            os.mkdir(newdir)
            rpn(f'[khaki1]{newdir}')
        newfile = os.path.join(newdir,item)
        if os.path.isfile(newfile):
            rpn(f'\t[cyan1]{newfile}')
            continue
        copy(curfile,newdir)
        rpn(f'\t[green1]{newdir}\\{item}')
#-------------------------------------------------------------------
except Exception as ErrMs:
    rpn(f'[orchid]{ErrMs}')
    # rpn(f'[orchid]{traceback.format_exc()}')
#Numba
#Nuitca
#mypyc
#-----------------------------------------------------------------
if not (len(sys.argv) > 1 and sys.argv[1] == 'cons'):input(':-> ')
sys.exit(0)
