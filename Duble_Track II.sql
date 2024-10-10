
Select tracknumber,  Count(*)as tr

from PlaylistUpdatable Where playlist_name = 'Dokin'
group by tracknumber 
HAVING tr >1;


