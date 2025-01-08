-- Выгрузка данных плейлиста в таблицу  Dokin_Playlist  вер.2025-01-08 
DROP TABLE IF EXISTS CurPlaylist;
CREATE TABLE CurPlaylist(Id_DP INTEGER PRIMARY KEY ASC UNIQUE NOT NULL, Artist TEXT, Locale TEXT, Title TEXT, ArtSort TEXT, ArtCount INTEGER , AllCount INTEGER,
 EnRuCount INTEGER, NewTrack INTEGER , RealTime DATETIME  NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M', 'NOW', 'localtime')));
Insert Into CurPlaylist(Id_DP, Artist, Locale, Title, ArtSort, AllCount, EnRuCount, ArtCount)
Select tracknumber, artist, locale, title, IFNULL(Genre, Artist), Count(*) Over(), Count(*) over(partition by Locale), Count(*) over(partition by IFNULL(Genre, Artist))
from PlaylistUpdatable Where playlist_name = 'Dokin';
Select * from CurPlaylist

