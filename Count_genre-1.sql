--2024-09-21
Select Artist, genre, count(*), sum(count(*))over (partition by genre) as cnt,sum(count(*))over (partition by locale) as lk, sum(count(*))over () as ali
from PlaylistUpdatable 
Where playlist_name = 'Dokin'
group by genre,Artist
order by cnt desc
