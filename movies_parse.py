import psycopg2
from config import config

def connect():
    connection = None
    try:
        params = config()
        print('Connecting to the postgresql database...')
        connection = psycopg2.connect(**params)

        #create a cursor
        crsr = connection.cursor()
        print('PostgreSQL database version: ')
        crsr.execute('SELECT version()')
        db_version = crsr.fetchone()
        print(db_version)
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None: 
            connection.close()
            print('Database connection terminated')
if __name__ == "__main__":
    connect()

def create_table():
#Create a table in the PostgreSQL database """
    commands = (
        """
        CREATE TABLE movies_table (
            movie_id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            release_year INT,
            genre VARCHAR(50),
            director VARCHAR(255)
        )
        """,)
    conn = None
    try:
        # Read connection parameters
        params = config()

        # Connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # Create a cursor
        cur = conn.cursor()

        # Create table one by one‹
        for command in commands:
            cur.execute(command)

        # Close communication with the PostgreSQL database server
        cur.close()

        # Commit the changes
        conn.commit()

        print('Table created successfully.')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

            

if __name__ == '__main__':
    create_table()