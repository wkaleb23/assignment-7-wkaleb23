# Assignment 7: Movie Indexing and Querying

UW, EE 590a
Fall 2023

## Objectives

* Implement a simple hashtable
* Use the hashtable to do a simple indexing of data
* Write a query processor to allow a user to interact with the program and query the data

## How to Run the Project
1. Clone the Repository

Open a terminal and navigate to the directory where you want to clone this repository. Then, clone this repository using the git clone command. 

```shell
git clone https://github.com/wkaleb23/assignment-7-wkaleb23.git
```

2. Navigate to the Project Directory

Still in the terminal, navigate to the directory where you just cloned your repo. For example:

```shell
cd path
```

3. Run the File

Run the a7.py file using the Python command:

```shell
python3 a7.py
```

Now you can start searching! Answer the questions to get your movies.

## Write Up

### Hashtable.py

To implement this portion, I mainly followed thr provided outline. The most challenging section for me what figuring out the resizing. I kept running into some really weird errors, until I realized that when I was creating a new Hashtable and adding all the existing elements, I was resizing again! In order to fix that, I divided the method into 2 separate functionalities:
- One that does the actual inserting of the element (put_one: to use in teh resizing)
- Another to do the full thing: add an element, calculate the load, and resize if needed.

I found the num_elems function to be really useful for calculating this number in the resizing.

The key here was to draw out the process and work through a few examples.

### a7.py

This was a really interesting assignment. i felt that it forced me to deep-dive into inheritance and how to really consider all possible edge cases when creating a system that interacts with a user. Here are some of the challenges/ interesting elements that I ran into:

1. **Movie**

This was the first portion that I implemented. the hardest piece here was figuring out how to handle the string, since I has to parse the list of actors. In order to do this I first split the string into 2: getting all the rest of the attributes and then the list of actors. I divide the original string by looking for "[". Once I figured that piece out, the rest of this was easy.

2. **MovieIndex**

I expected this section to be more difficualt, but I felt like I understood this implementation relatively easily. The key here was understanding the differnce between add, index and get. I originally tried implementing this before other classes, and quickly realized it was very hard if I didn't implement MovieSet first.

3. **StartRatingIndex, ActorIndex, GenreIndex, TitleIndex**

At first i struggled in deciding which methods I needed to override. It felt unnatural to not add all the functions. The majority where straighforward, the peculiar one is Actors. For this one, the key is overriding the add method. We need to do this since in compute_key we get a list of actors. Therefore, when we index, we need to add the movie more than once in the actors index, once for each actor.

4. **MovieSet**

In this class I added an attribute called chosen_filters. I did this in order to be able to print out the movies in a neater way. With this list, I keep track of the filter(s) from which a given set was created. For example (look at my implementation of main for this example to make sense):

User searches on Genre (comedy), which created a MovieSet of all the comedy movies with chosen_filters = ['genre']. If then (in the same search) the user chooses to search Rating (7.7), then we will have a new MovieSet which is the union of the previous one and the new one. Resulting in a movieSet with chosen_filters = ['genre', 'rating'].

When we print the movie set, we loop through each element of a MovieSet, and then for each filter in the chosen_filters, we add the specific value or values of the chosen. For example if a user searches:

- genre :  ['Comedy']
- rating :  ['7.7']

they would get results of this type:

- Movie 225: Adaptation. (Comedy, 7.7)
- Movie 226: Zodiac (Crime, 7.7)
- Movie 227: Stalag 17 (Comedy, 8.1)

Note: this chosen_filter gets added when a union happens. This means union has an extra parameter.

5. **QueryProcessor**

This class was straighforward, we create each index, and then index each one based on the given corpus. The "big" change I made here was adding a parameter to the MovieSet.union function that takes in the chosen filter as explained above.

6. **main**

Here is the logic I used:
- I welcome the user to the Movie Database Search System.
- I create a MovieCorpus object to hold the movie data.
- I create a FileParser object to read movie data from a CSV file and populate the MovieCorpus object.
- I create a QueryProcessor object, passing the MovieCorpus object to it for processing queries.
- I enter a loop to interact with the user until the user decides to quit. In each iteration of the loop:
    - I prompt the user to enter a field and values to search for in the movie database.
    - I process the user's query using the QueryProcessor object and store the results.
    - I ask the user if they want to add more values to the current field or add a different field to the search. If the user wants to add more values or a different field, I repeat the process of getting input from the user and processing the query.
    - Once the user is done with the search, I print the search parameters and the results. If no results were found, I apologize to the user.
    - I ask the user if they want to search again. If the user wants to search again, I repeat the whole process. If not, I break the loop.
I print a message indicating that the search is done.

7. **NOTE**

I noticed a potential improvement for this project. The logic at the moment it that we create a UNION of searches. However, in most scenarios, we would find that users would want to look for and INTERSECTION instead. It would be interesting to expand this code and allow the user to explain if they are looking for one or the other. In this case I could not implement since it would mess with some of the provided tests, and I did not want to go down that rabit hole. But it was a thought I had that I wanted to share.

8. **EXAMPLE**

I have left here a small example of how one would interact with this tool (I deleted a lot of the movies for readability):

```shell
PS C:\Users\carmenp\PycharmProjects\Test> & C:/ProgramData/anaconda3/python.exe c:/Users/carmenp/PycharmProjects/Test/assignment-7-wkaleb23-main/a7.py
Welcome to the Movie Database Search System!
Let's get started.

---------------------------------------------------------
Let's search for some movies!
What would you like to search by? [G]enre, [R]ating, [T]itle or [A]ctors. If you are done, choose [Q]uit.
G
Great! What  Genre  would you like to search for? Please enter a comma separated list of values. If you are done, choose [Q]uit.
comedy

Would you like to add more  Genre  to your search [Y]es or would you like to add a [D]ifferent field to continue your search?
If you are finished, choose [F]inished.
F
Here are the results of your search:
You searched for:
genre :  ['Comedy']
Your search returned  156  results.
Movie 0: Relatos salvajes (Comedy)
Movie 1: Munna Bhai M.B.B.S. (Comedy)
.
.
.
Movie 154: (500) Days of Summer (Comedy)
Movie 155: Groundhog Day (Comedy)

Would you like to search again? [Y]es or [N]o.
Y

---------------------------------------------------------
Let's search for some movies!
What would you like to search by? [G]enre, [R]ating, [T]itle or [A]ctors. If you are done, choose [Q]uit.
G
Great! What  Genre  would you like to search for? Please enter a comma separated list of values. If you are done, choose [Q]uit.
comedy,drama

Would you like to add more  Genre  to your search [Y]es or would you like to add a [D]ifferent field to continue your search?
If you are finished, choose [F]inished.
D
What would you like to search by? [G]enre, [R]ating, [T]itle or [A]ctors. If you are done, choose [Q]uit.
R
Great! What  Rating  would you like to search for? Please enter a comma separated list of values. If you are done, choose [Q]uit.
7.7

Would you like to add more  Rating  to your search [Y]es or would you like to add a [D]ifferent field to continue your search?
If you are finished, choose [F]inished.
F
Here are the results of your search:
You searched for:
genre :  ['Comedy', 'Drama']
rating :  ['7.7']
Your search returned  493  results.
Movie 0: Crazy, Stupid, Love. (Comedy, Comedy, 7.4)
Movie 1: Apocalypse Now (Drama, Drama, 8.5)
.
.
.
Movie 491: MASH (Comedy, Comedy, 7.7)
Movie 492: Animal House (Comedy, Comedy, 7.6)

Would you like to search again? [Y]es or [N]o.
Y

---------------------------------------------------------
Let's search for some movies!
What would you like to search by? [G]enre, [R]ating, [T]itle or [A]ctors. If you are done, choose [Q]uit.
R
Great! What  Rating  would you like to search for? Please enter a comma separated list of values. If you are done, choose [Q]uit.
7.0

Would you like to add more  Rating  to your search [Y]es or would you like to add a [D]ifferent field to continue your search?
If you are finished, choose [F]inished.
F
Here are the results of your search:
You searched for:
rating :  ['7.0']
Sorry, your search returned no results.

Would you like to search again? [Y]es or [N]o.
Y

---------------------------------------------------------
Let's search for some movies!
What would you like to search by? [G]enre, [R]ating, [T]itle or [A]ctors. If you are done, choose [Q]uit.
Q
Okay, all done.
```