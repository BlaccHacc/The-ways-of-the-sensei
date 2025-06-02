import csv

# Path to your CSV file
csv_file = 'movies.csv'

# Open the CSV file
with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
    # Create a CSV reader object
    reader = csv.DictReader(file)
    
    # Iterate through the rows in the CSV file
    for row in reader:
        # Access the columns by their header names
        movie_title = row['movie_title']
        release_year = row['release_year']
        actors = row['actors']
        
        # Print out the movie information
        print(f"Movie Title: {movie_title}")
        print(f"Release Year: {release_year}")
        print(f"Actors: {actors}")
        print("-" * 40)  # Divider for clarity
