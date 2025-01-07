Select Artist, genre, count(*), sum(count(*))over (partition by genre) as cnt
from PlaylistUpdatable 
Where playlist_name = 'Dokin'
group by genre,Artist
order by cnt desc
