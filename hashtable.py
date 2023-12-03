class KeyValuePair:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class Hashtable:
    def __init__(self, num_buckets = 9):
        self.alpha = 3
        self.num_buckets = num_buckets
        self.num_elements = 0
        self.buckets = [[] for value in range(self.num_buckets)] ## List of lists

    def put(self, key, value):
        pass

    def get(self, key: str):
        pass

    def load_factor(self):
        pass

    def resize(self):
        ## If the load factor is > threshold
        ## Create a new hashtable
        ## Take elements out of this hashtable and put them in the new hashtable
        ## Set self equal to the new hashtable
        self.__dict__.update(new_hashtable.__dict__) ## <----
        pass



    ## This is a helpful helper function
    def num_elems(self):
        num_elems = 0
        for bucket in self.buckets:
            num_elems += len(bucket)
        return num_elems

    def remove(self, key) -> KeyValuePair:
        pass

    def __iter__(self):
        return HashtableIterator(self)


class HashtableIterator:
    def __init__(self, hashtable):
        self.bucket_iterator = hashtable.buckets.__iter__()
        self.list_iterator = self.bucket_iterator.__next__().__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.list_iterator.__next__()
        except StopIteration:
            ## No more elements in this bucket; go to the next one
            try:
                self.list_iterator = self.bucket_iterator.__next__().__iter__()
                return self.__next__() ## Recursive call so we can move on from an empty bucket
            except StopIteration:
                ## No more buckets left to visit
                raise StopIteration
