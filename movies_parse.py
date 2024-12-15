import psycopg2
import csv
from config import config  # Ensure config function is imported

# Function to connect to PostgreSQL
def connect():
    connection = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        # Create a cursor
        crsr = connection.cursor()
        print('PostgreSQL database version: ')
        crsr.execute('SELECT version()')
        db_version = crsr.fetchone()
        print(db_version)
        crsr.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated')

# Function to create tables
def create_table():
    """Create a table in the PostgreSQL database."""
    commands = (
        """
        CREATE TABLE movies_table (
            movie_id SERIAL PRIMARY KEY,
            movie_title VARCHAR(255) NOT NULL,
            movie_description VARCHAR (1000),
            release_year INT,
            runtime_minutes INT,
            rating FLOAT, 
            votes INT, 
            revenue_millions DECIMAL(10, 2), 
            metascore INT
        );

        CREATE TABLE director_ref (
            director_id SERIAL PRIMARY KEY, 
            first_name VARCHAR(100), 
            middle_name VARCHAR(100), 
            last_name VARCHAR(100)
        );

        CREATE TABLE actor_ref (
            actor_id SERIAL PRIMARY KEY,
            first_name VARCHAR (100),
            middle_name VARCHAR (100),
            last_name VARCHAR (100)
        );

        CREATE TABLE genre_ref (
            genre_id SERIAL PRIMARY KEY,
            genre VARCHAR (100)
        );

        CREATE TABLE movie_director(
            movie_id INT,
            director_id INT, 
            PRIMARY KEY (movie_id, director_id),
            FOREIGN KEY (director_id) REFERENCES director_ref(director_id) ON DELETE CASCADE
        );

        CREATE TABLE movie_actor (
            movie_id INT,
            actor_id INT,
            PRIMARY KEY (movie_id, actor_id),
            FOREIGN KEY (actor_id) REFERENCES actor_ref(actor_id) ON DELETE CASCADE
        );

        CREATE TABLE movie_genre(
            movie_id INT, 
            genre_id INT, 
            PRIMARY KEY (movie_id, genre_id), 
            FOREIGN KEY (genre_id) REFERENCES genre_ref(genre_id) ON DELETE CASCADE
        );
        """,
    )
    conn = None
    try:
        # Read connection parameters
        params = config()

        # Connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # Create a cursor
        cur = conn.cursor()

        # Execute commands one by one
        for command in commands:
            cur.execute(command)

        # Close communication with the PostgreSQL database server
        cur.close()

        # Commit the changes
        conn.commit()

        print('Tables created successfully.')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

# Function to insert data from CSV
def insert_data_from_csv(csv_file_path):
    """Insert data from a CSV file into the movies_table."""
    conn = None
    try:
        # Read connection parameters
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # Open the CSV file and read data
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Insert data into movies_table
                cur.execute("""
                    INSERT INTO movies_table (
                        movie_title, movie_description, release_year, runtime_minutes, rating, votes, revenue_millions, metascore
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    row['movie_title'],
                    row['movie_description'],
                    int(row['release_year']),
                    int(row['runtime_minutes']),
                    float(row['rating']),
                    int(row['votes']),
                    float(row['revenue_millions']),
                    int(row['metascore'])
                ))

        # Commit the changes
        conn.commit()
        print(f"Data from {csv_file_path} inserted successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

# Function to add actor data from the movies list
def actors_data_add(movies):
    all_actors = []

    for movie in movies:
        actors = movie.get('actors')
        if actors:
            movie_actors = actors.split(',')
            all_actors.extend(movie_actors)

    all_actors = list(set(all_actors))

    for actor in all_actors: 
        dir_list = actor.split(' ')
        count = len(dir_list)

        if count == 1:
            print('1', dir_list)
            sql = 'INSERT INTO actor_ref (first_name) VALUES (%s)'
            first_name = dir_list[0]
            params = [first_name]
            doQuery(sql, params)

        elif count == 2:
            print('2', dir_list)
            sql = 'INSERT INTO actor_ref (first_name, last_name) VALUES (%s, %s)'
            first_name, last_name = dir_list[0], dir_list[1]
            params = [first_name, last_name]
            doQuery(sql, params)

        elif count == 3:
            print('3', dir_list)
            sql = 'INSERT INTO actor_ref (first_name, middle_name, last_name) VALUES (%s, %s, %s)'
            first_name, middle_name, last_name = dir_list[0], dir_list[1], dir_list[2]
            params = [first_name, middle_name, last_name]
            doQuery(sql, params)

        else:
            print(f"Unexpected name format for actor: {actor}")

# Function to add director data from the movies list
def director_data_add(movies):
    all_directors = []  # Initialize as an empty list

    # Extract all directors from the movies list
    for movie in movies:
        directors = movie.get('directors')  # Safely get 'directors' key
        if directors:
            movie_directors = directors.split(',')  # Split multiple directors
            all_directors.extend(movie_directors)

    # Remove duplicates
    all_directors = list(set(all_directors))

    # Process each director
    for director in all_directors:
        dir_list = director.split(' ')
        count = len(dir_list)

        if count == 1:
            print('1', dir_list)
            sql = 'INSERT INTO director_ref (first_name) VALUES (%s)'
            first_name = dir_list[0]
            params = [first_name]
            doQuery(sql, params)

        elif count == 2:
            print('2', dir_list)
            sql = 'INSERT INTO director_ref (first_name, last_name) VALUES (%s, %s)'
            first_name, last_name = dir_list[0], dir_list[1]
            params = [first_name, last_name]
            doQuery(sql, params)

        elif count == 3:
            print('3', dir_list)
            sql = 'INSERT INTO director_ref (first_name, middle_name, last_name) VALUES (%s, %s, %s)'
            first_name, middle_name, last_name = dir_list[0], dir_list[1], dir_list[2]
            params = [first_name, middle_name, last_name]
            doQuery(sql, params)

        else:
            print(f"Unexpected name format for director: {director}")

# Placeholder function for query execution (implement the actual query execution)
def doQuery(sql, params):
    conn = None
    try:
        # Read connection parameters
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error executing query: {error}")
    finally:
        if conn is not None:
            conn.close()

# Main function to execute the script
if __name__ == '__main__':
    connect()
    # Uncomment to create tables
    # create_table()
    # Uncomment to insert data from CSV
    insert_data_from_csv('C:/maccdaddy/movies.csv')

            
