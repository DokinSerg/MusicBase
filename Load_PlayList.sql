--Загрузка плейлиста 2023-12-13
Update PlaylistUpdatable 
Set tracknumber = (Select NewTrack From CurPlaylist Where tracknumber = CurPlaylist.Id_DP) 
Where (playlist_name = 'Dokin');
