class KeyValuePair:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class Hashtable:
    def __init__(self, num_buckets = 9):
        # initialize hashtable with num_buckets number of buckets
        self.alpha = 3
        self.num_buckets = num_buckets
        self.num_elements = 0
        self.buckets = [[] for value in range(self.num_buckets)] ## List of lists

    def put_one(self, key, value):
        # helper method to put key value pair into hashtable
        # this is used in put and resize
        
        # find the bucket index for the key
        bucket_index = hash(key) % self.num_buckets
        # get the bucket at the bucket index
        bucket = self.buckets[bucket_index]
        # now we need to check if the key already exists in the bucket
        for kvp in bucket:
            if kvp.key == key:
                kvp.value = value
                return
        # if we get here, the key does not exist in the bucket, so we need to add it
        kvp = KeyValuePair(key, value)
        bucket.append(kvp)
        # increment num_elements
        self.num_elements += 1

    def put(self, key, value):
        # method to put key value pair into hashtable
        self.put_one(key, value)
        
        # resize if necessary
        if self.load_factor() >= self.alpha:
            self.resize()

    def get(self, key: str):
        # method to get value from hashtable
        # if key exists, return value
        # if key does not exist, return None
        bucket_index = hash(key) % self.num_buckets
        bucket = self.buckets[bucket_index]
        for kvp in bucket:
            if kvp.key == key:
                return kvp.value
        return None

    def load_factor(self):
        # method to calculate load factor
        return self.num_elements / self.num_buckets

    def resize(self):
        # method to resize hashtable
        # create a new hashtable with num_buckets*2+1 number of buckets
        # add all key value pairs from old hashtable to new hashtable
        # update num_buckets and buckets
        new_num_buckets = self.num_buckets * 2 + 1
        new_hashtable = Hashtable(new_num_buckets)
        for bucket in self.buckets:
            for kvp in bucket:
                # here I want to use put_one instead of put since put will resize again
                new_hashtable.put_one(kvp.key, kvp.value) 
        self.num_buckets = new_hashtable.num_buckets
        self.buckets = new_hashtable.buckets
        new_num_elements = new_hashtable.num_elems()
        self.num_elements = new_num_elements  # update num_elements
        

    ## This is a helpful helper function
    def num_elems(self):
        num_elems = 0
        for bucket in self.buckets:
            num_elems += len(bucket)
        return num_elems

    def remove(self, key) -> KeyValuePair:
        # method to remove key value pair from hashtable
        # if key exists, remove key value pair and return it
        # if key does not exist, raise NotImplementedError
        bucket_index = hash(key) % self.num_buckets
        bucket = self.buckets[bucket_index]
        # now we need to check if the key already exists in the bucket
        for index, kvp in enumerate(bucket):
            if kvp.key == key:
                self.num_elements -= 1  # decrement num_elements
                return bucket.pop(index)
        raise NotImplementedError
    
    def __iter__(self):
        return HashtableIterator(self)


class HashtableIterator:
    # This was provided
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
