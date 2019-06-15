# Python3 program to demonstrate auto-complete  
# feature using Trie data structure. 
# Note: This is a basic implementation of Trie 
# and not the most optimized one. 

import re


# def h1(s,m): # funcao de hash 1
#     ret = 0
#     for i in range(len(s)):
#         ret += ord(s[i])**2 % m
#     ret %= m
#     return ret
class movieInfo(object):
    def __init__(self, movieID, movieName, movieGenres):
        self.movieID = movieID
        self.movieName = movieName
        self.movieGenres = movieGenres
        self.movieRateSum = 0
        self.movieCount = 0
        self.movieRate = 0
        

class H1LinProb(object):
    """ Busca Linear | h1 """
    def __init__(self,size):
        self.size = size
        self.map = [None] * self.size
        self.used = [False] * self.size

    # def hf(self,key):
    #     return h1(key,self.size)

    def insere(self,key, movieInfo):
        key_hash = key
        h = key_hash
        collisions = 0
        while self.map[h] is not None:
            h = (h+1) % self.size
            collisions += 1
            if h == key_hash:
                print("\nHash Full\n")
                return -1
        #self.map[h] = [key,movieInfo]
        self.map[h] = movieInfo
        self.used[h] = True
        return collisions

    def pesquisa(self,key):
        key_hash = key
        h = key_hash
        acessos = 0

        while self.used[h] == True:
            acessos += 1
            if self.map[h][0] == key:
                return acessos
            h = (h+1) % self.size
            if h == key_hash:
                return self.map[key]
        return self.map[key]

class TrieNode(): 
    def __init__(self): 
          
        # Initialising one node for trie 
        self.children = {} 
        self.last = False
        self.movieID = 0

class Trie(): 
    def __init__(self): 
          
        # Initialising the trie structure. 
        self.root = TrieNode() 
        self.word_list = [] 
  
    def formTrie(self, moviesHashTable): 
          
        # Forms a trie structure with the given set of strings 
        # if it does not exists already else it merges the key 
        # into it by extending the structure as required 
        reader = open("movie.csv", "r")
        reader.readline()
        for line in reader:
            #stringLine = line.split(',(')
            #stringLine = re.findall(r"[\w']+", line)
            stringLine = re.split(r',(?=")', line)
            movieID = stringLine[0]
            intMovieID = int(movieID)
            movieName = stringLine[1]
            movieName = movieName[1:]
            movieName = movieName[:-1]
            movieGenre = stringLine[2]
            movieGenre = movieGenre[:-3]
            movieGenre = movieGenre[1:]

            actualMovieInfo = movieInfo(movieID, movieName, movieGenre)
            self.insert(movieName,movieID)
            moviesHashTable.insere(intMovieID, actualMovieInfo)
        reader.close()

        reader = open("rating.csv", "r")
        reader.readline()
        for line in reader:
            stringLine = line.split(',')
            movieID = int(stringLine[1])
            userRate = float(stringLine[2])
            moviesHashTable.map[movieID].movieRateSum += userRate
            moviesHashTable.map[movieID].movieCount += 1
            moviesHashTable.map[movieID].movieRate = moviesHashTable.map[movieID].movieRateSum / moviesHashTable.map[movieID].movieCount
        reader.close()


        # for key in keys: 
        #     self.insert(key) # inserting one key to the trie. 
  
    def insert(self, key, movieID): 
          
        # Inserts a key into trie if it does not exist already. 
        # And if the key is a prefix of the trie node, just  
        # marks it as leaf node. 
        node = self.root 
        #print(list(key))
        for a in list(key): 
            if not node.children.get(a): 
                node.children[a] = TrieNode() 
  
            node = node.children[a] 
  
        node.last = True
        node.movieID = movieID

    def search(self, key): 
          
        # Searches the given key in trie for a full match 
        # and returns True on success else returns False. 
        node = self.root 
        found = True
  
        for a in list(key): 
            if not node.children.get(a): 
                found = False
                break
  
            node = node.children[a] 
  
        return node and node.last and found 
  
    def suggestionsRec(self, node, word): 
          
        # Method to recursively traverse the trie 
        # and return a whole word.  
        if node.last: 
            self.word_list.append(node.movieID) 
  
        for a,n in node.children.items(): 
            self.suggestionsRec(n, word + a) 
  
    def printAutoSuggestions(self, key): 
          
        # Returns all the words in the trie whose common 
        # prefix is the given key thus listing out all  
        # the suggestions for autocomplete. 
        node = self.root 
        not_found = False
        temp_word = '' 
        printedMovie = False

        for a in list(key): 
            if not node.children.get(a): 
                not_found = True
                break
  
            temp_word += a 
            node = node.children[a] 
  
        if not_found: 
            return 0
        elif node.last and not node.children: 
            printedMovie = True

        if printedMovie == False:
           self.suggestionsRec(node, temp_word) 
  
        #    for s in self.word_list: 
        #        print(s) 

        return 1

# Python program for implementation of MergeSort 
def mergeSort(arr): 
    if len(arr) >1: 
        mid = len(arr)//2 #Finding the mid of the array 
        L = arr[:mid] # Dividing the array elements  
        R = arr[mid:] # into 2 halves 
  
        mergeSort(L) # Sorting the first half 
        mergeSort(R) # Sorting the second half 
  
        i = j = k = 0
          
        # Copy data to temp arrays L[] and R[] 
        while i < len(L) and j < len(R): 
            if L[i].movieRate > R[j].movieRate: 
                arr[k] = L[i] 
                i+=1
            else: 
                arr[k] = R[j] 
                j+=1
            k+=1
          
        # Checking if any element was left 
        while i < len(L): 
            arr[k] = L[i] 
            i+=1
            k+=1
          
        while j < len(R): 
            arr[k] = R[j] 
            j+=1
            k+=1

def filterByGenre(moviesHashTable, userGenre):
    topList = []
    for i in range(0, len(moviesHashTable.map)):
        if moviesHashTable.map[i] != None:
            if userGenre in moviesHashTable.map[i].movieGenres and moviesHashTable.map[i].movieCount > 999:
                topList.append(moviesHashTable.map[i])
    return topList

def printTopMovies(moviesHashTable, topNumber, userGenre):
    filteredMovies = filterByGenre(moviesHashTable, userGenre)
    mergeSort(filteredMovies)
    for i in range(0, int(topNumber)):
        print("Title: " + filteredMovies[i].movieName,
              "Genres: " + filteredMovies[i].movieGenres,
              "Rating: " + str(filteredMovies[i].movieRate),
              "Count: " + str(filteredMovies[i].movieCount))

t = Trie() 
moviesHashTable = H1LinProb(131381) 
# creating the trie structure with the  
# given set of strings. 
t.formTrie(moviesHashTable) 
  
# autocompleting the given key using  
# our trie structure. 



userInput = "default"

while userInput != "exit":
    print("Search movies by typing movie, user, top, or tags")
    userInput = raw_input()
    if "movie " in userInput:
        t.printAutoSuggestions(userInput[6:])
        for element in t.word_list:
            print(
            "ID: " + moviesHashTable.map[int(element)].movieID,
            "Title: " + moviesHashTable.map[int(element)].movieName,
            "Genres: " + moviesHashTable.map[int(element)].movieGenres, 
            "Rate: " + str(moviesHashTable.map[int(element)].movieRate),
            "Count: " + str(moviesHashTable.map[int(element)].movieCount)
            )
        t.word_list = []    
    elif "top " in userInput:
        userInput = userInput.split(' ')
        topNumber = userInput[1]
        userGenre = userInput[2]
        printTopMovies(moviesHashTable, topNumber, userGenre)

    