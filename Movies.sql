CREATE DATABASE Movies;

CREATE SCHEMA movies;

CREATE TABLE movies.movies (
    movie_id SERIAL PRIMARY KEY,
    movie_title VARCHAR(400),
    movie_description VARCHAR(1000), 
    release_year VARCHAR(4),
    runtime_minutes VARCHAR(3),
    rating FLOAT, 
    votes INT,
    revenue_millions FLOAT,
    metascore INT 
);

CREATE TABLE movies.actor_ref (
    actor_id SERIAL PRIMARY KEY, 
    first_name VARCHAR(100),
    middle_name VARCHAR(100), 
    last_name VARCHAR(100)
);

CREATE TABLE movies.genre_ref (
    genre_id SERIAL PRIMARY KEY,
    genre VARCHAR(255)
);

CREATE TABLE movies.director_ref (
    director_id SERIAL PRIMARY KEY, 
    first_name VARCHAR(100), 
    middle_name VARCHAR(100), 
    last_name VARCHAR(100)
);

CREATE TABLE movies.movie_actor (
    movie_id INT,
    actor_id INT,
    PRIMARY KEY (movie_id, actor_id),
    CONSTRAINT fk_movie_actor_movie
        FOREIGN KEY (movie_id) 
        REFERENCES movies.movies(movie_id),
    CONSTRAINT fk_movie_actor_actor
        FOREIGN KEY (actor_id)
        REFERENCES movies.actor_ref(actor_id)
);

CREATE TABLE movies.movie_genre (
    movie_id INT, 
    genre_id INT, 
    PRIMARY KEY (movie_id, genre_id), 
    CONSTRAINT fk_movie_genre_movie
        FOREIGN KEY (movie_id)
        REFERENCES movies.movies(movie_id),
    CONSTRAINT fk_movie_genre_genre
        FOREIGN KEY (genre_id)
        REFERENCES movies.genre_ref(genre_id) 
);

CREATE TABLE movies.movie_director (
    movie_id INT, 
    director_id INT, 
    PRIMARY KEY (movie_id, director_id), 
    CONSTRAINT fk_movie_director_movie
        FOREIGN KEY (movie_id)
        REFERENCES movies.movies(movie_id),
    CONSTRAINT fk_movie_director_director
        FOREIGN KEY (director_id)
        REFERENCES movies.director_ref(director_id)
);
