-- Выгрузка данных плейлиста в таблицу  Playlist_EveningBell  вер.2024-12-29 
DROP TABLE IF EXISTS CurPlaylist;
CREATE TABLE CurPlaylist(Id_DP INTEGER PRIMARY KEY ASC UNIQUE NOT NULL, Artist TEXT, Locale TEXT, Title TEXT, ArtSort TEXT, ArtCount INTEGER , AllCount INTEGER, EnRuCount INTEGER
	, GroupCount INTEGER, GroupStep INTEGER, ArtStep  INTEGER, NewTrack INTEGER , RealTime DATETIME  NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M', 'NOW', 'localtime')));
Insert Into CurPlaylist(Id_DP, Artist, Locale, Title, ArtSort, AllCount, EnRuCount, ArtCount)
Select tracknumber, artist, locale, title, IFNULL(Genre, Artist), Count(*) Over(), Count(*) over(partition by Locale), Count(*) over(partition by IFNULL(Genre, Artist))
from PlaylistUpdatable Where playlist_name = 'EveningBell';
Update CurPlaylist Set GroupStep = ((Select Count(*) From CurPlaylist Where Locale = 'Ru')/(Select Count(*) FROM CurPlaylist Where Locale = 'En') + 1);
Update CurPlaylist Set GroupCount = AllCount/GroupStep,  ArtStep = AllCount/(GroupStep * ArtCount);
Select * from CurPlaylist

