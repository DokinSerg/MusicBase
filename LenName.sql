-- Выгрузка данных плейлиста в таблицу  Playlist_EveningBell  вер.2024-12-29 
Select tracknumber,artist,title,filename
--,*,album
from PlaylistUpdatable 
Where playlist_name = 'dokin' and length(filename) >50
;


