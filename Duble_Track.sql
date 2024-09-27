Select tracknumber, artist, locale, title , Count(*) as cct
from PlaylistUpdatable 
Where playlist_name = 'Dokin' 
group by tracknumber 
having (cct != 1)
order by tracknumber
;

