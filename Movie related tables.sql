CREATE TABLE genre_ref (
genre_id SERIAL PRIMARY KEY,
genre VARCHAR(255),
);

CREATE TABLE Director_REF (
director_id SERIAL PRIMARY KEY, 
first_name VARCHAR(100), 
middle_name VARCHAR(100), 
last_name VARCHAR(100)
);

CREATE TABLE Actor_Ref (
actor_id SERIAL PRIMARY KEY, 
first_name VARCHAR(100),
middle_name VARCHAR(100), 
last_name VARCHAR(100)
);

CREATE TABLE Movie_Genre(
    movie_id INT, 
    genre_id VARCHAR(255), 
    PRIMARY KEY (movie_id), 
    FOREIGN KEY (genre_id) REFERENCES genre_ref(genre_id)
    CONSTRAINT fk_genre_ref_movie_genre
FOREIGN KEY (genre_id)
REFERENCES genre_ref(genre_id) ON DELETE CASCADE
);

CREATE TABLE Movie_Director(
    movie_id INT,
    director_id INT, 
    PRIMARY KEY (movie_id),
    FOREIGN KEY (director_id) REFERENCES director_ref(director_id)
    CONSTRAINT fk_directir_ref_movie_director
    FOREIGN KEY (directir_id)
    REFERENCES director_ref(director_id) ON DELETE CASCADE
);

CREATE TABLE Movie_Actor(
movie_id INT,
actor_id INT,
PRIMARY KEY (movie_id),
FOREIGN KEY (actor_id) REFERENCES actor_ref(actor_id),
CONSTRAINT fk_actor_ref_movie_actor
FOREIGN KEY (actor_id)
REFERENCES actor_ref(actor_id) ON DELETE CASCADE
);