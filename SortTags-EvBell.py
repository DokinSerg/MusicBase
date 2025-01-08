import os, sys
import traceback
import sqlite3
from rich import print as rpn

__author__ = 't.me/dokin_sergey'
__version__ = '1.4.5'
__verdate__ = '2025-01-08 10:45'

SQLiteBase = fr"{os.environ['APPDATA']}\foobar2000-v2\configuration\foo_sqlite.user.db"
#"""C:/Users/dokin/AppData/Roaming/foobar2000/configuration/foo_sqlite.user.db"""
rpn(f'База {SQLiteBase}')
#################################################################################################################
def SQLiteWrite(IdTrack: int, NewNumTrakc: int) ->None :
    try:
        with sqlite3.connect(SQLiteBase) as conn:
        # conn = sqlite3.connect( SQLiteBase )
            conn.execute("Update CurPlaylist Set NewTrack = ? Where Id_DP = ? ;", (NewNumTrakc, IdTrack))
            conn.commit()
    except sqlite3.Warning as Warn:
        rpn(f'\t[red1]{Warn}')
    except sqlite3.Error as DErr:
        rpn(f'\t[red1]{DErr}')
#################################################################################################################
def NewStep (IdTrack: int, OldStp: int, ArtStp: int, GrStp: int) ->int:#, dbg:bool = False
    res = 0
    try: # парт намба 1. Начинаем с предыдушего, если занято шагаем по GrStep
        CurTrk = OldStp + ArtStp * GrStp
        while CurTrk <= AllCount : # первое условие, вмещаемся, проверяем на занятость
            if ListTrack[CurTrk] == 0:
                ListTrack[CurTrk] = IdTrack
                res = CurTrk
                break
            CurTrk += GrStp
        else:
            for ns in range(ArtStp + 1, 1,-1): # пытаемся впихнуть деля шаг пополам от текущего значения
                CurTrk = OldStp + GrStp * ns //2   # С нормальным шагом не нашли, нужно уменьшить шаг
                while CurTrk <= AllCount :
                    if ListTrack[CurTrk] == 0:
                        ListTrack[CurTrk] = IdTrack
                        res = CurTrk
                        break
                    CurTrk += GrStp * ns //2
                if res: break
    except Exception as ErrMs:
        rpn (f'NewStep except: [red1]{ErrMs} {IdTrack = } {CurTrk  = }')
        rpn(f'[red1]{traceback.format_exc()}')
    return res
#--------------------------------------------------------------------------------------------------------------------------------------------
def FirstFreeList(FF:int, FFStp:int) ->int:#, dbg:bool = False
    res = 0
    fi = len(ListTrack) + 1
    for k in range(FF, fi, FFStp ):
        if ListTrack[k] == 0:
            res = k
            break
    else:
        rpn(f'FirstFreeList [yellow] {FF = } {FFStp = } {fi = }')
    # print(f'{FF = } {FFStp = } {res = }')
    return res
##############################################################################################################################################################
if __name__ == '__main__':
    debug = False
    rpn(f'[cyan1]Сортировка Музыкальных сборников ver.[green1]{__version__} SQL Lite [green1]{sqlite3.sqlite_version}')
    if debug:rpn(f'[orchid]Режим отладки {debug}')
    try:
        with sqlite3.connect(SQLiteBase) as MusBase:
            cursor1 = MusBase.cursor() # основной и 1-го курсор
            SQLTxt = "SELECT distinct AllCount, EnRuCount FROM CurPlaylist order by Locale "
            cursor1.execute(SQLTxt)
            crsr = cursor1.fetchall()
        if  debug:rpn(f'[yellow]{crsr = }')
        AllCount = crsr[0][0]# общее количество треков
        ListTrack = dict((x,0) for x in range(1, AllCount + 1)) # Список для проверки трек занят/свободен
        EnCount = crsr[0][1]# En количество треков
        RuCount = crsr[1][1]# Ru количество треков
                            # шаг групп треков = 4?
        GroupStep = int(round(EnCount/RuCount,0)) + 1 if EnCount/RuCount > 1 else int(round(RuCount/EnCount,0)) + 1
        GroupCount = int(round(AllCount/GroupStep,0))# количество групп треков
        FirsTrack  = GroupStep # Текущий новый номер трека, начальное значение AND Artist = 'Fancy'
        rpn(f'{EnCount = } {EnCount = } {RuCount = } {GroupCount = } {GroupStep = } {AllCount = }')
        SQLTxt = "SELECT Distinct ArtSort, ArtCount FROM CurPlaylist Where Locale = 'En' ORDER BY ArtCount;"# Desc
        CounTrc = 0
        NewTtack = 0
        CurrenTrack = 0
        # sys.exit(0)
# ***************** первый шаг по автору en ********************************************
        for row in cursor1.execute(SQLTxt):
            if debug:rpn(f'[yellow]{row}')
            Artist = row[0]
            ArtStep = int(round(AllCount/(GroupStep * row[1]),0))
            if  debug:rpn(f'[yellow]{Artist = }  {ArtStep = }')
            SQLTxt2 = "SELECT Id_DP, Title, ArtCount  FROM CurPlaylist Where (Locale = 'En') AND (ArtSort = '" + Artist + "') ORDER by Id_DP"
            cursor2 = MusBase.cursor()
            cursor2.execute(SQLTxt2)
            one_res = cursor2.fetchone()
            Id_DP = one_res[0] #ID трека
            Title = one_res[1] # Название трека
            ArtCount = one_res[2] # Шаг номера трека в группах ( *4)
            FirsTrack = FirstFreeList(FirsTrack, GroupStep )
            NewTtack = NewStep(Id_DP, FirsTrack, 0, GroupStep)
            rpn(f'1:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
            if NewTtack:
                SQLiteWrite(Id_DP,NewTtack)
                CounTrc += 1
            else:
                rpn(Id_DP,' = ',Artist,' = ', ArtStep,' = ', Title, ' = ',ArtCount, ' = ',NewTtack )
                rpn('Ай, ай, авария 1')
                sys.exit(1)
 # **************************************************** шаги по кругу по автору en ****************************
            for row2 in cursor2:
                Id_DP = row2[0] #ID трека
                Title = row2[1] # Название трека
                ArtCount = row2[2] # Шаг номера трека в группах ( *4)
                NewTtack = NewStep(Id_DP, NewTtack, ArtStep, GroupStep) # шаги от последнего значения
                rpn(f'2:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
                if NewTtack:
                    SQLiteWrite(Id_DP,NewTtack)
                    CounTrc += 1
                else:
                    FirsTrack = FirstFreeList(FirsTrack, GroupStep)
                    NewTtack = NewStep(Id_DP, FirsTrack, ArtStep, GroupStep) # повторим тоже самое от первого значения
                    rpn(f'3:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
                    if NewTtack:
                        SQLiteWrite(Id_DP,NewTtack)
                        CounTrc += 1
                    else:
                        rpn()
                        rpn(str(Id_DP).rjust(5),' = ',Artist,' = ', ArtStep,' = ', Title, ' = ',ArtCount, ' = ',NewTtack )
                        rpn('Ай, ай, авария 2')
                        sys.exit(1)
# ****************************************************************************************************
        #raise ('отладка')
        SQLTxt = "SELECT Distinct ArtSort, ArtCount FROM CurPlaylist Where Locale = 'Ru' ORDER BY ArtCount;"# Desc
        NewTtack = 0
        CurrenTrack = 1
        FirsTrack = 1
        for row in cursor1.execute(SQLTxt):
            if debug:rpn(f'[yellow]{row}')
            if debug:input('Дальше? :-> ')
            Artist = row[0]
            ArtStep = int(round(AllCount/(GroupStep * row[1]),0))# Шаг номера автора в ГРУППАХ
            SQLTxt2 = "SELECT Id_DP, Title, ArtCount  FROM CurPlaylist Where (Locale = 'Ru') and (ArtSort = '" + Artist + "') "
            cursor2 = MusBase.cursor()
            cursor2.execute(SQLTxt2)
            one_res = cursor2.fetchone()
            Id_DP = one_res[0] #ID трека
            Title = one_res[1] # Название трека
            ArtCount = one_res[2] # Шаг номера трека в группах ( *4) нет такого
            FirsTrack = FirstFreeList(FirsTrack, 1) # Текущий новый номер трека, начальное значение
            NewTtack = NewStep(Id_DP, FirsTrack, 0, 1)
            rpn(f'4:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
            if NewTtack:
                SQLiteWrite(Id_DP,NewTtack)
                CounTrc += 1
            else:
                FirsTrack = FirstFreeList(FirsTrack,1)
                NewTtack = NewStep(Id_DP, FirsTrack, ArtStep,1)
                rpn('Ай, ай, авария 3')
                rpn(f'5:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
                rpn(Id_DP,' = ',Artist,' = ', ArtStep,' = ', Title, ' = ',ArtCount, ' = ',NewTtack )
                rpn('FirsTrack = ',FirsTrack,'CurrenTrack = ',CurrenTrack,'NewTtack = ', NewTtack )
                for i,j in ListTrack.items():
                    rpn(str(i).rjust(4),str(j).rjust(4))
                sys.exit(1)
            for row2 in cursor2:
                Id_DP = row2[0] #ID трека
                Title = row2[1] # Название трека
                ArtCount = row2[2] # Шаг номера трека в группах ( *4)
                NewTtack = NewStep(Id_DP, NewTtack, ArtStep, GroupStep)
                rpn(f'6:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
                if  NewTtack:
                    SQLiteWrite(Id_DP,NewTtack)
                    CounTrc += 1
                else:
                    FirsTrack = FirstFreeList(FirsTrack, 1)
                    NewTtack = NewStep(Id_DP, FirsTrack, ArtStep, GroupStep) # повторим тоже самое от первого значения
                    rpn(f'7:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
                    if NewTtack:
                        SQLiteWrite(Id_DP,NewTtack)
                        CounTrc += 1
                    else:
                        NewStep(Id_DP, FirsTrack, ArtStep, GroupStep)
                        NewTtack = NewStep(Id_DP, FirsTrack, 0, 0)
                        rpn(f'8:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
                        if NewTtack:
                            SQLiteWrite(Id_DP,NewTtack)
                            break
                        rpn(Id_DP,' = ',Artist,' = ', ArtStep,' = ', Title, ' = ',ArtCount, ' = ',NewTtack )
                        rpn('FirsTrack = ',FirsTrack,'CurrenTrack = ',CurrenTrack,'NewTtack = ', NewTtack )
                        rpn('Ай, ай, авария 4')
                        for i,j in ListTrack.items():
                            rpn(str(i).rjust(4),str(j).rjust(4))
                        break
    except sqlite3.Warning as Warn:
        rpn(f'[khaki1]{Warn}')
    except sqlite3.Error as DErr:
        rpn(f'[red1]{DErr}')
        rpn(f'[red1]{traceback.format_exc()}')
    except Exception as ErrMs:
        rpn(f'[red1]EO:{str(ErrMs)}')
        rpn(f'[red1]{traceback.format_exc()}')
        rpn(f'[red1]{NewTtack}')
        rpn(f'[red1]EO:{GroupStep * ArtStep:5}')
        rpn(f'[red1]EO:{Artist = }')
        rpn(f'[red1]EO:{Title = }')
    finally:
        MusBase.commit()
        MusBase.close()
    rpn()
#-----------------------------------------------------------------
    input('Выход:-> ')
    sys.exit(0)
