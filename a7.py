from hashtable import Hashtable, KeyValuePair
import csv

class MovieCorpus(list):
    def __init__(self):
        super()

class FileParser:
    def __init__(self):
        pass

    def read_file(self, filename: str, corpus: MovieCorpus):
        pass

class Movie:
    def __init__(self, datarow: str = ""):
        self.title = ""
        self.star_rating = 0
        self.content_rating = ""
        self.genre = ""
        self.duration = 0
        self.actors = []
        self.actors_list = "" ## TODO: Temp, just to help get started
        self.num_actors = 0
        if datarow != "":
            self.parse_row(datarow)

    ## "7.4,My Sister's Keeper,PG-13,Drama,109,['Cameron Diaz', u'Abigail Breslin', u'Alec Baldwin']"
    ## star_rating,title,content_rating,genre,duration,actors_list
    def parse_row(self, datarow):
        pass

    def populate_from_csv_array(self, csv_dict):
        pass

    ## This allows a Movie to be printed via `print(movie)`
    def __str__(self):
        return f"{self.title}"


"""A Hashtable, with a KVP where the Key is a word and the value is a MovieSet"""
class MovieIndex(Hashtable):
    def __init__(self):
        super().__init__(5)

    def add(self, movie: Movie):
        ## Get the movieset associated with the given word
        ## Add the movie to the set
        pass

    def index(self, corpus: MovieCorpus):
        pass

    def get_movie_set(self, term: str):
        pass

    ## Returns a list of keys for this movie
    ## This is usually just a single entry, but sometimes multiple (e.g. Actors)
    def compute_key(self, movie: Movie):
        pass

    def print(self):
        for index, item in enumerate(self):
            print(f"Key: {item.key}")
            movie_set = item.value
            movie_set.print()


class StarRatingIndex(MovieIndex):
    def compute_key(self, movie: Movie):
        pass

class ActorIndex(MovieIndex):
    def compute_key(self, movie: Movie):
        pass

class GenreIndex(MovieIndex):
    def compute_key(self, movie: Movie):
        pass

class TitleIndex(MovieIndex):
    def compute_key(self, movie: Movie):
        pass

class MovieSet:
    def __init__(self, description = ""):
        self.description = description
        self.movies = set()

    def add_movie_to_set(self, movie: Movie):
        pass

    def union(self, movie_set):
        """Creates a new MovieSet, which is a union of this MovieSet and the given movie_set"""
        ## Returns the new unioned set
        pass

    def num_elems(self):
        pass

    def print(self):
        print(f"MovieSet: {self.description} ({self.num_elems()} Movies)")
        for index, item in enumerate(self.movies):
            print(f"Movie{index}: {item}")

## This helps pring out an entire MovieIndex
## Feel free to change/tweak it to print nicely
class MovieReport:
    def __init__(self):
        pass

    def print_report(self, index: MovieIndex):
        while(self.iterator.next != None):
            self.output_movie_set(index)

    def output_movie_set(self, movieset: MovieSet):
        print(movieset.description)
        for movie in movieset.movies:
            print(movie)

    def output_report(self, index: MovieIndex):
        return self.print_report(index)

    def save_report(self, index: MovieIndex, filename:str):
        file = open(filename, 'w')
        file.write(self.output_report(index))
        return file

class QueryProcessor():
    def __init__(self, corpus: MovieCorpus):
        ## Create MovieIndexes
        ## Populate them from the corpus
        pass

    def query(self, field: str, vals: list):
        return MovieSet("Empty Set")

# Defining main function
def main():
    print("hey there")
    ## Create a MovieCorpus
    ## Use a FileProcessor to read in Movies and populate MovieCorpus
    ## Create a QueryProcessor, passing in the MovieCorpus

    ## Interact with the user, passing queries to the QueryProcessor, until we're done
    ## Print a message to the user giving guidance on how to query
    print("Go ahead, enter a query: ")
    ## Take the input and process the query
    ## Iterate until the user is done entering queries
    print("okay, all done")

if __name__ == "__main__":
    main()


