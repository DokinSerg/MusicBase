import os, sys
from rich import print
import traceback
import sqlite3

author = 't.me/dokin_sergey'
version = '1.4.3'
verdate = '2023-12-23 22:54:05'

# global SQLiteBase #Путь к базе данных
# global ListTrack # Список свободных/занятых треков
# global FirsTrack # ТЕКУЩИЙ номер первого трека current
# global AllCount # общее количество треков
# global MyDeb # Отладка
SQLiteBase = f"{os.environ['APPDATA']}\\foobar2000-v2\\configuration\\foo_sqlite.user.db"
#"""C:/Users/dokin/AppData/Roaming/foobar2000/configuration/foo_sqlite.user.db"""
print(f'{SQLiteBase = }')
def SQLiteWrite(IdTrack: int, NewNumTrakc: int) ->str :
    sql = ''
    try:
        conn = sqlite3.connect( SQLiteBase )
        conn.execute("Update CurPlaylist Set NewTrack = ? Where Id_DP = ? ;", (NewNumTrakc, IdTrack))
        conn.commit()
    except sqlite3.Warning as Warn:
        IB = Warn
    except sqlite3.Error as DErr:
        IB = DErr
    else:
        conn.commit()
        conn.close()
        sql = 'Ok'
    # finally:
        # print (Warn)
    return sql
#***************************************
def NewStep (IdTrack: int, OldStp: int, ArtStp: int, GrStp: int) ->int:
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
                # print(f'Не нашли Но пробуем {CurTrk = } {ns = } {ListTrack[CurTrk] =}')
                while CurTrk <= AllCount :
                    if ListTrack[CurTrk] == 0:
                        ListTrack[CurTrk] = IdTrack
                        res = CurTrk
                        break
                    CurTrk += GrStp * ns //2
                if res: break
    except Exception as ErrMs:
        print ('except:', str(ErrMs), IdTrack, CurTrk )
        print(traceback.format_exc())
    return res
#***************************************
def FirstFreeList(FF:int, FFStp:int) ->int:
    res = 0
    fi = len(ListTrack) + 1
    for k in range(FF, fi, FFStp ):
        if ListTrack[k] == 0:
            res = k
            break
    else:
        print('FirstFreeList',FF, FFStp, fi)
    # print(f'{FF = } {FFStp = } {res = }')
    return res
 #***************************************
# def TrackPrint():
    # print(str(Id_DP).rjust(4),'=',str(ArtCount).rjust(2),'=',str(ArtStep).rjust(3),'=', str(FirsTrack).rjust(4),\
    # '=', str(NewTtack).rjust(5),'=', Artist,'=', Title)
    # return 1
#**************************************************************************************************************************
if __name__ == '__main__':
    print ("Тест модуля работы SQL Lite ", version) # print (SQLiteBase)
    try:
        with sqlite3.connect(SQLiteBase) as MusBase:
        #MusBase = sqlite3.connect(SQLiteBase)
            cursor1 = MusBase.cursor() # основной и 1-го курсор
            SQLTxt = "SELECT distinct AllCount, EnRuCount, GroupCount, GroupStep FROM CurPlaylist order by Locale "
            cursor1.execute(SQLTxt)
            crsr = cursor1.fetchall()
        AllCount = crsr[0][0]   # общее количество треков
        ListTrack = dict((x,0) for x in range(1, AllCount + 1)) # Список для проверки трек занят/свободен
        EnCount = crsr[0][1]    # En количество треков
        RuCount = crsr[1][1]    # Ru количество треков
        GroupCount = crsr[0][2] # количество групп треков
        GroupStep  = crsr[0][3] # шаг групп треков = 4?
        FirsTrack  = GroupStep # Текущий новый номер трека, начальное значение AND Artist = 'Fancy'
        print(f'{EnCount =} {EnCount = } {RuCount =} {GroupCount =} {GroupStep  =} {AllCount = }')
        SQLTxt = "SELECT Distinct ArtSort, ArtStep FROM CurPlaylist Where Locale = 'En' ORDER BY ArtStep;"# Desc;"
        CounTrc = 0
        NewTtack = 0
        CurrenTrack = 0
        # sys.exit(0)
# ***************** первый шаг по автору en ********************************************
        for row in cursor1.execute(SQLTxt):
            Artist = row[0]
            ArtStep = row[1]
            SQLTxt2 = "SELECT Id_DP, Title, ArtCount  FROM CurPlaylist Where (Locale = 'En') AND (ArtSort = '" + Artist + "') ORDER by Id_DP"
            cursor2 = MusBase.cursor()
            cursor2.execute(SQLTxt2)
            one_res = cursor2.fetchone()
            Id_DP = one_res[0] #ID трека
            Title = one_res[1] # Название трека
            ArtCount = one_res[2] # Шаг номера трека в группах ( *4)
            FirsTrack = FirstFreeList(FirsTrack, GroupStep )
            NewTtack = NewStep(Id_DP, FirsTrack, 0, GroupStep)
            print(f'1:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
            if NewTtack:
                SQLiteWrite(Id_DP,NewTtack)
                CounTrc += 1
            else:
                print(Id_DP,' = ',Artist,' = ', ArtStep,' = ', Title, ' = ',ArtCount, ' = ',NewTtack )
                print('Ай, ай, авария 1')
                sys.exit(1)
 # **************************************************** шаги по кругу по автору en ****************************
            for row2 in cursor2:
                Id_DP = row2[0] #ID трека
                Title = row2[1] # Название трека
                ArtCount = row2[2] # Шаг номера трека в группах ( *4)
                NewTtack = NewStep(Id_DP, NewTtack, ArtStep, GroupStep) # шаги от последнего значения
                print(f'2:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
                if NewTtack:
                    SQLiteWrite(Id_DP,NewTtack)
                    CounTrc += 1
                else:
                    FirsTrack = FirstFreeList(FirsTrack, GroupStep)
                    NewTtack = NewStep(Id_DP, FirsTrack, ArtStep, GroupStep) # повторим тоже самое от первого значения
                    print(f'3:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
                    if NewTtack:
                        SQLiteWrite(Id_DP,NewTtack)
                        CounTrc += 1
                    else:
                        print()
                        print(str(Id_DP).rjust(5),' = ',Artist,' = ', ArtStep,' = ', Title, ' = ',ArtCount, ' = ',NewTtack )
                        print('Ай, ай, авария 2')
                        sys.exit(1)
# ****************************************************************************************************
        #raise ('отладка')
        SQLTxt = "SELECT Distinct ArtSort, ArtStep FROM CurPlaylist Where Locale = 'Ru' ORDER BY ArtStep;"  #
        NewTtack = 0
        CurrenTrack = 1
        FirsTrack = 1
        for row in cursor1.execute(SQLTxt):
            Artist = row[0]
            ArtStep = row[1] # Шаг номера автора в ГРУППАХ
            SQLTxt2 = "SELECT Id_DP, Title, ArtCount  FROM CurPlaylist Where (Locale = 'Ru') and (ArtSort = '" + Artist + "') "
            cursor2 = MusBase.cursor()
            cursor2.execute(SQLTxt2)
            one_res = cursor2.fetchone()
            Id_DP = one_res[0] #ID трека
            Title = one_res[1] # Название трека
            ArtCount = one_res[2] # Шаг номера трека в группах ( *4) нет такого
            FirsTrack = FirstFreeList(FirsTrack, 1) # Текущий новый номер трека, начальное значение
            NewTtack = NewStep(Id_DP, FirsTrack, 0, 1)
            print(f'4:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
            if NewTtack:
                SQLiteWrite(Id_DP,NewTtack)
                CounTrc += 1
            else:
                FirsTrack = FirstFreeList(FirsTrack,1)
                NewTtack = NewStep(Id_DP, FirsTrack, ArtStep,1)
                print('Ай, ай, авария 3')
                print(f'5:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
                print(Id_DP,' = ',Artist,' = ', ArtStep,' = ', Title, ' = ',ArtCount, ' = ',NewTtack )
                print('FirsTrack = ',FirsTrack,'CurrenTrack = ',CurrenTrack,'NewTtack = ', NewTtack )
                for i,j in ListTrack.items():
                    print(str(i).rjust(4),str(j).rjust(4))
                sys.exit(1)
            for row2 in cursor2:
                Id_DP = row2[0] #ID трека
                Title = row2[1] # Название трека
                ArtCount = row2[2] # Шаг номера трека в группах ( *4)
                NewTtack = NewStep(Id_DP, NewTtack, ArtStep, 1)
                print(f'6:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
                if  NewTtack:
                    SQLiteWrite(Id_DP,NewTtack)
                    CounTrc += 1
                else:
                    FirsTrack = FirstFreeList(FirsTrack, 1)
                    NewTtack = NewStep(Id_DP, FirsTrack, ArtStep, GroupStep) # повторим тоже самое от первого значения
                    print(f'7:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
                    if NewTtack:
                        SQLiteWrite(Id_DP,NewTtack)
                        CounTrc += 1
                    else:
                        NewStep(Id_DP, FirsTrack, ArtStep, GroupStep)
                        NewTtack = NewStep(Id_DP, FirsTrack, 0, 0)
                        print(f'8:{NewTtack:5}:{GroupStep * ArtStep:5}: {Artist = }:{Title = }')
                        if NewTtack:
                            SQLiteWrite(Id_DP,NewTtack)
                            break
                        print(Id_DP,' = ',Artist,' = ', ArtStep,' = ', Title, ' = ',ArtCount, ' = ',NewTtack )
                        print('FirsTrack = ',FirsTrack,'CurrenTrack = ',CurrenTrack,'NewTtack = ', NewTtack )
                        print('Ай, ай, авария 4')
                        for i,j in ListTrack.items():
                            print(str(i).rjust(4),str(j).rjust(4))
                        break
    except sqlite3.Warning as Warn:
        IB = Warn
    except sqlite3.Error as DErr:
        print(str(DErr))
        print(traceback.format_exc())
    except Exception as ErrMs:
        print(f'EO:{str(ErrMs)}')
        print(traceback.format_exc())
        print(NewTtack)
        print(f'EO:{GroupStep * ArtStep:5}')
        print(f'EO:{Artist = }')
        print(f'EO:{Title = }')
    finally:
        MusBase.commit()
        MusBase.close()
        IB = 'Ok'
    print()
    print(IB)
#-----------------------------------------------------------------
    input('Выход:-> ')
    os._exit(0)
