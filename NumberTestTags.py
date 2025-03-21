import os
from rich import print as rpn
import traceback
import sqlite3

author = 't.me/dokin_sergey'
_version = '1.0.1'
_verdate = '2024-10-05 15:34'

SQLiteBase = f"{os.environ['APPDATA']}\\foobar2000-v2\\configuration\\foo_sqlite.user.db"
#"""C:/Users/dokin/AppData/Roaming/foobar2000/configuration/foo_sqlite.user.db"""
print(f'{SQLiteBase = }')
##########################################################################################################################
def Ntr(lens:int)->int:
    # for i in range(2,lens,2):
        # yield i
    yield from list(range(2,lens + 1,2))
##########################################################################################################################
if __name__ == '__main__':
    print (f'Тест модуля работы SQL Lite {_version}  SQLite {sqlite3.sqlite_version}') # print (SQLiteBase)
    try:
        with sqlite3.connect(SQLiteBase) as MB:
            cur = MB.cursor()
            SQLTxt = "select Id_DP, locale, artist, title from CurPlaylist where Locale = 'En' order by locale, Id_DP"
            cur.execute(SQLTxt)
            crsr = cur.fetchall()
        #-------------------------------------
            SQLTxt = "Select max(Id_DP) from CurPlaylist"
            cur.execute(SQLTxt)
            ali = cur.fetchone()
            # rpn(f'{type(ali[0]) = } >< {ali[0] = }' )
            # input()
            a = ali[0]
###########################################################################################################################
        # a = max(n[0] for n in crsr)
        gen = Ntr(a)
        # ni = next(gen)
        for row,Lkl,artist,NameTr in crsr:
            ni = next(gen)
            while ni < row:
                rpn(f'[yellow]{ni:5}')
                ni = next(gen)
            rpn(f'[green1]{ni:5} {row:5} {Lkl} {artist:22} [cyan]{NameTr}')
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
        IB = 'Ok'
    rpn('[cyan1]-'*100)
    rpn(f'Работа завершена успешно! SQLite {sqlite3.sqlite_version}')
    print(IB)
