import csv

def load_data(filename):
    mylist = []
    with open (filename) as movies:
        movies_data = csv.reader(movies,delimiter=',' )
        next(movies_data) #skip the header
        for row in movies_data: 
            mylist.append(row[10])
            return mylist
        
