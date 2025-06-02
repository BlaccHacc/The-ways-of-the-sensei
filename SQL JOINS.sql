SELECT movie_id, first_name, middle_name, last_name
FROM movies.movie_actor
INNER JOIN movies.actor_ref
ON movies.movie_actor.actor_id = movies.actor_ref.actor_id;

SELECT movie_id, genre
FROM movies.movie_genre
INNER JOIN movies.genre_ref
ON movies.movie_genre.genre_id = movies.genre_ref.genre_id;

SELECT movie_id, first_name, middle_name, last_name
FROM movies.movie_director
INNER JOIN movies.director_ref
ON movies.movie_director.director_id = movies.director_ref.director_id;