from hashtable import Hashtable, KeyValuePair
import csv

class MovieCorpus(list):
    def __init__(self):
        super()

class FileParser:
    def __init__(self):
        pass

    def read_file(self, filename: str, corpus: MovieCorpus):
        # method to read file and populate corpus
        
        # the first row of the csv file is the header, so skip it
        # open the file
        with open(filename, 'r') as file:
            # create a csv reader
            reader = csv.reader(file)
            # skip the header
            next(reader)
            # loop through the rows
            for row in reader:
                # create a movie object
                movie = Movie()
                # populate the movie object from the csv row
                movie.populate_from_csv_array(row)
                # add the movie to the corpus
                corpus.append(movie)
                
        return corpus
        
class Movie:
    def __init__(self, datarow: str = ""):
        # method to initialize movie object
        self.title = ""
        self.star_rating = 0.0
        self.content_rating = ""
        self.genre = ""
        self.duration = 0
        self.actors = []
        self.num_actors = 0
        if datarow != "":
            self.parse_row(datarow)

    ## "7.4,My Sister's Keeper,PG-13,Drama,109,['Cameron Diaz', u'Abigail Breslin', u'Alec Baldwin']"
    ## star_rating,title,content_rating,genre,duration,actors_list
    def parse_row(self, datarow):
        # method to parse row and populate movie with all the attributes
        
        # first divide the datarow into the first 5 attributes and the actors list
        datarow, actors_list = datarow.split('[',1)
        datarow = datarow.split(',')
        self.star_rating = datarow[0]
        self.title = datarow[1]
        self.content_rating = datarow[2]
        self.genre = datarow[3]
        self.duration = datarow[4]
        # clean up the actors list
        actors_list = actors_list.replace(']','')
        actors_list = actors_list.replace('\'','')
        actors_list = actors_list.replace('u','')
        self.actors = [actor.strip() for actor in actors_list.split(',')]
        self.num_actors = len(self.actors)

    def populate_from_csv_array(self, csv_dict):
        # turn the csv row from list into a string
        self.star_rating = csv_dict[0]
        self.title = csv_dict[1]
        self.content_rating = csv_dict[2]
        self.genre = csv_dict[3]
        self.duration = csv_dict[4]
        actors_list = csv_dict[5]
        actors_list = actors_list.replace(']','')
        actors_list = actors_list.replace('\'','')
        actors_list = actors_list.replace('u','')
        self.actors = [actor.strip() for actor in actors_list.split(',')]
        self.num_actors = len(self.actors)

    ## This allows a Movie to be printed via `print(movie)`
    def __str__(self):
        return f"{self.title}"


"""A Hashtable, with a KVP where the Key is a word and the value is a MovieSet"""
class MovieIndex(Hashtable):
    def __init__(self):
        super().__init__(5)

    def add(self, movie: Movie):
        ## Get the movieset associated with the given word
        ## Add the movie to the set (if it's not already there)
    
        # get the key
        key = self.compute_key(movie)
        # the value will be the moveie set
        value = self.get(key)
        # if the value is None, create a new MovieSet
        if value == None:
            value = MovieSet(key)
        # add the movie to the set
        value.add_movie_to_set(movie)
        # add the key value pair to the hashtable
        self.put(key, value)
        
    def index(self, corpus: MovieCorpus):
        ## Iterate through the corpus, adding each movie to the index
        for movie in corpus:
            self.add(movie)

    def get_movie_set(self, term: str):
        ## Returns the MovieSet associated with the given term
        ## If the term is not in the index, returns None
        
        # get the value
        value = self.get(term)
        # return the value
        return value

    ## Returns a list of keys for this movie
    ## This is usually just a single entry, but sometimes multiple (e.g. Actors)
    def compute_key(self, movie: Movie):        
        # get the key
        key = movie.title
        # return the key
        return key
    
    def print(self):
        for index, item in enumerate(self):
            print(f"Key: {item.key}")
            movie_set = item.value
            movie_set.print()


class StarRatingIndex(MovieIndex):
    def __init__(self):
        super().__init__()
            
    def compute_key(self, movie: Movie):
        # method to compute key for a given movie
        # returns a list of keys for this movie
        # override the compute_key method from MovieIndex
        
        # get the key
        key = movie.star_rating
        # return the key
        return key

class ActorIndex(MovieIndex):
    def __init__(self):
        super().__init__()

    def add(self, movie: Movie):
        # I need to override the add method because I need to add the movie to the hashtable multiple times
        
        # get the actors
        keys = self.compute_key(movie)
        # loop through the actors
        for actor in keys:
            # get the value
            value = self.get(actor)
            # if the value is None, create a new MovieSet
            if value == None:
                value = MovieSet(actor)
            # add the movie to the set
            value.add_movie_to_set(movie)
            # add the key value pair to the hashtable
            self.put(actor, value)    

    def compute_key(self, movie: Movie):
        # method to compute key for a given movie
        # returns a list of keys for this movie
        # returns multiple entries, one for each actor
        # override the compute_key method from MovieIndex
        
        # get the key
        keys = movie.actors
        # return the key
        return keys

class GenreIndex(MovieIndex):
    def __init__(self):
        super().__init__()
            
    def compute_key(self, movie: Movie):
        # method to compute key for a given movie
        # returns a list of keys for this movie
        # override the compute_key method from MovieIndex
        
        # get the key
        key = movie.genre
        # return the key
        return key

class TitleIndex(MovieIndex):
    def __init__(self):
        super().__init__()
        
    def compute_key(self, movie: Movie):
        # method to compute key for a given movie
        # returns a list of keys for this movie
        # override the compute_key method from MovieIndex
        
        # get the key
        key = movie.title
        # return the key
        return key

class MovieSet:
    def __init__(self, description = ""):
        # I saved chosen_filters as a list because I want to be able to add multiple filters to a set
        # for example, if the user searches for a movie by actor and genre, I want to be able to add both of those filters to the set
        self.description = description
        self.movies = set()
        self.chosen_filters = []

    def add_movie_to_set(self, movie: Movie):
        ## Adds a movie to the set
        self.movies.add(movie)

    def union(self, movie_set, filter = None):
        """Creates a new MovieSet, which is a union of this MovieSet and the given movie_set"""
        ## Returns the new unioned set
        ## Does not modify this set or the given set
        # first check if the movie_set is None, if it is, return self
        if movie_set == None:
            return self
        new_set = MovieSet(self.description + movie_set.description)
        new_set.movies = self.movies.union(movie_set.movies)
        new_set.chosen_filters = self.chosen_filters + [filter]
        return new_set

    def num_elems(self):
        ## Returns the number of movies in this set
        return len(self.movies)

    def print(self):
        # This will print out the movies in the set nicely
        # If there are filters, it will print out the filters as well
        for index, item in enumerate(self.movies):
            out_message = f"Movie {index}: {item}"
            if len(self.chosen_filters) != 0:
                out_message += " ("
                for filter in self.chosen_filters:
                    if filter == "rating":
                        out_message += f"{item.star_rating}"
                    elif filter == "actor":
                        out_message += f"{item.actors}"
                    elif filter == "genre":
                        out_message += f"{item.genre}"
                    elif filter == "title":
                        out_message += f"{item.title}"
                    # if it's the last filter, don't add a comma
                    if filter == self.chosen_filters[-1]:
                        out_message += ")"
                    else:
                        out_message += ", "
            print(out_message)

## This helps pring out an entire MovieIndex
## Feel free to change/tweak it to print nicely
class MovieReport:
    def __init__(self):
        self.iterator = None
        
    def print_report_new(self, index):
        for key in index:
            print(f"Key: {key}")
            values = index.get_movie_set(key)
            for value in values:
                print(f"\tValue: {value}")

    def print_report(self, index: MovieIndex):
        self.iterator = index.__iter__()
        while(self.iterator.__next__ != None):
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
        
        # create star rating index
        self.star_index = StarRatingIndex()   
        # populate star rating index from corpus
        self.star_index.index(corpus)
        
        # create actor index
        self.actor_index = ActorIndex()
        # populate actor index from corpus
        self.actor_index.index(corpus)
        
        # create genre index
        self.genre_index = GenreIndex()
        # populate genre index from corpus
        self.genre_index.index(corpus)
        
        # create title index
        self.title_index = TitleIndex()
        # populate title index from corpus
        self.title_index.index(corpus)
        
        

    def query(self, field: str, vals: list):
        ## Returns a MovieSet of movies matching the given query
        ## If the field is invalid, returns None
        ## If the field is valid, but there are no matches, returns an empty MovieSet
        result_set = MovieSet("Empty Set")
        for val in vals:
            if field == "rating":
                result_set = result_set.union(self.star_index.get_movie_set(val), "rating")
            elif field == "actor":
                result_set = result_set.union(self.actor_index.get_movie_set(val), "actor")
            elif field == "genre":
                result_set = result_set.union(self.genre_index.get_movie_set(val), "genre")
            elif field == "title":
                result_set = result_set.union(self.title_index.get_movie_set(val), "title")
        return result_set
    
def get_field_input():
    # Helper function to get the field input from the user
    print("What would you like to search by? [G]enre, [R]ating, [T]itle or [A]ctors. If you are done, choose [Q]uit.")
    field_input = input()
    field_input = field_input.strip()
    if field_input == 'Q' or field_input.lower() == 'quit':
        field = 'quit'
        field_text = 'quit'
    elif field_input == 'G' or field_input.lower() == 'genre':
        field = 'genre'
        field_text = 'Genre'
    elif field_input == 'R' or field_input.lower() == 'rating':
        field = 'rating'
        field_text = 'Rating'
    elif field_input == 'T' or field_input.lower() == 'title':
        field = 'title'
        field_text = 'Title'
    elif field_input == 'A' or field_input.lower() == 'actors':
        field = 'actor'
        field_text = 'Actor'
    else:
        print("Sorry, I don't understand that. Please try again.")
        field, field_text = get_field_input()
    
    return field, field_text
    
def get_val_input(field_input, field_text):
    # Helper function to get the value input from the user
    print("Great! What ", field_text, " would you like to search for? Please enter a comma separated list of values. If you are done, choose [Q]uit.")
    val_input = input()
    
    val_input = val_input.strip()
    if field_input == 'Q' or field_input.lower() == 'quit':
        vals = ['quit']
        return vals
    else:
        vals = val_input.split(',')
        vals = [val.strip() for val in vals]
        vals = [val.lower() for val in vals]
        # capitalize the first letter of each word
        vals = [val.title() for val in vals]
        return vals

# Defining main function
def main():
    print("Welcome to the Movie Database Search System!")
    print('Let\'s get started.')
    # Instantiate a MovieCorpus object
    corpus = MovieCorpus()

    # Instantiate a FileParser object
    parser = FileParser()

    # Use the read_file method of the FileParser object to read the movie data from a file and populate the MovieCorpus object
    # Replace 'movies.csv' with the path to your CSV file
    parser.read_file('assignment-7-wkaleb23-main\\imdb_1000.csv', corpus)

    # Instantiate a QueryProcessor object, passing the MovieCorpus object to it
    query_processor = QueryProcessor(corpus)
    
    # Interact with the user, passing queries to the QueryProcessor, until the user is done
    while True:
        print()
        print('---------------------------------------------------------')
        print("Let's search for some movies!")
        paramenters = {}
        
        # first get the field input from the user
        field, field_text = get_field_input()
        if field == 'quit':
            break
        
        # then get the value input from the user
        vals = get_val_input(field, field_text)
        if vals[0] == 'quit' or vals[0] == 'Q':
            break
        
        # I want to save the parameters so I can print them out later
        if paramenters.get(field) == None:
            paramenters[field] = vals
        else:
            paramenters[field].append(vals)
        
        result_set = query_processor.query(field, vals)
        
        # I want to continue asking the user if they want to continue checking other fields
        while True:
            # first check if they want to add more values to the field they chose
            print()
            print("Would you like to add more ", field_text, " to your search [Y]es or would you like to add a [D]ifferent field to continue your search?")
            print("If you are finished, choose [F]inished.")
            
            # get the input from the user
            cont_input = input()
            cont_input = cont_input.strip()
            if cont_input == 'F' or cont_input.lower() == 'finished':
                break
            
            # if they want to add more values to the field they chose, get the values, keep the field the same
            if cont_input == 'Y' or cont_input.lower() == 'yes':
                
                vals = get_val_input(field, field_text)
                if vals[0] == 'quit' or vals[0] == 'Q':
                    break
                
                # I don't want to save the parameters because I am adding more values to the same field
                result_set = result_set.union(query_processor.query(field, vals), field)
            
            # if they want to add a different field, get the field and values
            elif cont_input == 'D' or cont_input.lower() == 'different':
                
                field, field_text = get_field_input()
                if field == 'quit':
                    break
                
                vals = get_val_input(field, field_text)
                if vals[0] == 'quit' or vals[0] == 'Q':
                    break
                
                # I want to save the parameters so I can print them out later
                if paramenters.get(field) == None:
                    paramenters[field] = vals
                else:
                    paramenters[field].append(vals)
                
                result_set = result_set.union(query_processor.query(field, vals), field)
            else:
                # ask the user to try again
                print('Sorry, I don\'t understand that. Please try again.')
                
        # at this point, the user is done woth the search
        print("Here are the results of your search:")
        print("You searched for:")
        for field in paramenters:
            print(field, ": ", paramenters[field])
        
        # check if there are no results I want to apologize to the user
        if result_set.num_elems() == 0:
            print("Sorry, your search returned no results.")
        # if there are results, print them out nicely
        else:
            print("Your search returned ", result_set.num_elems(), " results.")
            result_set.print()  
            
        print() 
        # ask the user if they want to search again
        print("Would you like to search again? [Y]es or [N]o.")
        search_again = input()
        search_again = search_again.strip()
        if search_again == 'Y' or search_again.lower() == 'yes':
            continue
        else:
            break          

    print("Okay, all done.")

if __name__ == "__main__":
    main()


