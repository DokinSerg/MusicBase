import os
import sys
import traceback
import sqlite3
from rich import print as rpn

author = 't.me/dokin_sergey'
__version__ = '1.0.4'
__verdate__ = '2025-02-26 10:23'

SQLiteBase = f"{os.environ['APPDATA']}\\foobar2000-v2\\configuration\\foo_sqlite.user.db"
#"""C:/Users/dokin/AppData/Roaming/foobar2000/configuration/foo_sqlite.user.db"""
print(f'{SQLiteBase = }')
##########################################################################################################################
def Ntr(lens:int)->int:
    # for i in range(2,lens,2):
        # yield i
    yield from list(range(2,lens + 1,2))
#######################################################################################################################
if __name__ == '__main__':
    print (f'Тест модуля работы SQL Lite {__version__}  SQLite {sqlite3.sqlite_version}') # print (SQLiteBase)
    try:
        while True:
            with sqlite3.connect(SQLiteBase) as MB:
                cur = MB.cursor()
                SQLTxt = "select Id_DP, locale, artist, title from CurPlaylist order by Id_DP"
                cur.execute(SQLTxt)
                crsr = cur.fetchall()
            #-------------------------------------
                SQLTxt = "Select max(Id_DP) from CurPlaylist"
                cur.execute(SQLTxt)
                ali = cur.fetchone()
                a = ali[0]
        #--------------------------------------------------------------------------------------------------------------
            en = 0;ru = 0
            for ni,row in enumerate(crsr,1):
                Ntr,Lkl,artist,NameTr = row
                if ni % 2:
                    if Lkl == 'Ru':rpn(f'[bright_blue]{ni:5} {Ntr:5} {Lkl} {artist:22} {NameTr}')
                    else:
                        rpn(f'[bright_yellow]{ni:5} {Ntr:5} {Lkl} {artist:22} {NameTr}')
                        en += 1
                else:
                    if Lkl == 'En':rpn(f'[cyan]{ni:5} {Ntr:5} {Lkl} {artist:22} {NameTr}')
                    else:
                        rpn(f'[green1]{ni:5} {Ntr:5} {Lkl} {artist:22} {NameTr}')
                        ru += 1
        #--------------------------------------------------------------------------------------------------------------
            rpn('[cyan1]-'*100)
            rpn(f'Работа завершена успешно! SQLite {sqlite3.sqlite_version}')
            rpn(f'Качество обработки Русских {ru:2} английских {en:2}')
            if input('Повторить? :-> '):break
    except sqlite3.Warning as Warn:
        IB = Warn
    except sqlite3.Error as DErr:
        print(str(DErr))
        print(traceback.format_exc())
    except Exception as ErrMs:
        print(f'EO:{str(ErrMs)}')
        print(traceback.format_exc())
        rpn(ni, row)
    finally:
        MB.commit()
        MB.close()
#############################################################################
# input('Выход:-> ')
os._exit(0)
