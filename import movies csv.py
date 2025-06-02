import csv
import psycopg2

# Database connection setup
try:
    # Establish a connection to the database
    connection = psycopg2.connect(
        host="192.168.1.203",
        database="Movies",
        user="postgres",
        password="password",
        port="5432"
    )

    # Create a cursor object
    cursor = connection.cursor()
    
    # Execute a query (optional)
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print(f"Connected to: {db_version}")

    # Ensure the table exists
    
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS movies (
        id SERIAL PRIMARY KEY,
        movie_title VARCHAR(255),
        movie_description VARCHAR(1000), 
        release_year INT, 
        runtime_minutes INT,
        rating FLOAT,
        votes INT,
        revenue_millions FLOAT, 
        metascore INT
    );
    '''
    cursor.execute(create_table_query)
    connection.commit()

    # Open the CSV file and read rows
    with open('movies.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            try:
                movie_title = row['Title']
                movie_description = row.get('Description', '')  # Default to empty string if not found
                release_year = int(row.get('Release Year', 0))
                runtime_minutes = int(row.get('Runtime(Minutes)', 0))
                rating = float(row.get('Rating', 0.0))
                votes = int(row.get('Votes', 0))
                revenue_millions = float(row.get('Revenue Millions', 0.0))
                metascore = int(row.get('Metascore', 0))

                # Insert data into the database
                insert_query = '''
                INSERT INTO movies (movie_title, movie_description, release_year, runtime_minutes, rating, votes, revenue_millions, metascore) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                '''
                cursor.execute(insert_query, (movie_title, movie_description, release_year, runtime_minutes, rating, votes, revenue_millions, metascore))

            except ValueError as ve:
                print(f"Error parsing row {row}: {ve}")
        
        connection.commit()  # Commit all inserts at once

except Exception as error:
    print(f"Error: {error}")

finally:
    # Close the cursor and connection if open
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'connection' in locals() and connection:
        connection.close()