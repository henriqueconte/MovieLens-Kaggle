import re

class movieInfo(object):
    def __init__(self, movieID, movieName, movieGenres):
        self.movieID = movieID
        self.movieName = movieName
        self.movieGenres = movieGenres
        self.movieRateSum = 0
        self.movieCount = 0
        self.movieRate = 0
        self.movieTags = []
        

class MovieHashTable(object):
    """ Busca Linear | h1 """
    def __init__(self,size):
        self.size = size
        self.map = [None] * self.size
        self.used = [False] * self.size

    def insere(self,key, movieInfo):
        self.map[key] = movieInfo
        self.used[key] = True

    def pesquisa(self,key):
        return self.map[key]

    def remove(self,key):
        if self.map[key] is not None:
            for i in range(len(self.map[key])):
                if self.map[key][i][0] == key:
                    self.map[key].pop(i)
                    if len(self.map[key]) == 0:
                        self.map[key] = None
                    return True
        return False


class TrieNode(): 
    def __init__(self): 
          
        # Initialising one node for trie 
        self.children = [None] * 330 
        self.leaf = False
        self.movieID = 0

class Trie(): 
    def __init__(self): 
          
        # Initialising the trie structure. 
        self.root = TrieNode() 
        self.movieIDList = [] 
  
    def buildTrie(self, moviesHashTable): 
          
        # Forms a trie structure with the given set of strings 
        # if it does not exists already else it merges the key 
        # into it by extending the structure as required 
        reader = open("movie.csv", "r")
        reader.readline()
        for line in reader:
            stringLine = re.split(r',(?=")', line)
            movieID = stringLine[0]
            intMovieID = int(movieID)
            movieName = stringLine[1]
            movieName = movieName[1:-1]
            movieGenre = stringLine[2]
            movieGenre = movieGenre[1:-3]
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

        reader = open("tag.csv", "r")
        reader.readline()
        for line in reader:
            stringLine = line.split(',')
            movieID = int(stringLine[1])
            movieTag = stringLine[2]
            moviesHashTable.map[movieID].movieTags.append(movieTag)
        reader.close()
  
    def insert(self, movieName, movieID): 
          
        # Inserts a movieName into trie if it does not exist already. 
        # And if the movieName is a prefix of the trie node, just  
        # marks it as leaf node. 
        node = self.root 
        for letter in list(movieName): 
            if not node.children[ord(letter)]: 
                node.children[ord(letter)] = TrieNode() 
  
            node = node.children[ord(letter)] 
  
        node.leaf = True
        node.movieID = movieID

    def search(self, movieName): 
          
        # Searches the given movieName in trie for a full match 
        # and returns True on success else returns False. 
        node = self.root 
        found = True
  
        for letter in list(movieName): 
            if not node.children[ord(letter)]: 
                found = False
                break
  
            node = node.children[ord(letter)] 

        return node 
  
    def suggestionsRec(self, node): 
          
        # Method to recursively traverse the trie 
        # and return a whole word.

        if node == None:
            return
        
        if node.movieID != 0:
            self.movieIDList.append(node.movieID)
        
        for element in node.children:
            self.suggestionsRec(element)

            
  
    def printAutoSuggestions(self, movieName): 
          
        # Returns all the words in the trie whose common 
        # prefix is the given movieName thus listing out all  
        # the suggestions for autocomplete. 
        node = self.root 
        notFound = False
        printedMovie = False

        for letter in list(movieName): 
            if not node.children[ord(letter)]: 
                notFound = True
                break
  
            node = node.children[ord(letter)] 
  
        if notFound: 
            return 
        elif node.leaf and not node.children: 
            printedMovie = True

        if printedMovie == False:
           node = self.search(movieName)
           self.suggestionsRec(node)  

# Python program for implementation of MergeSort 
def mergeSort(moviesID): 
    if len(moviesID) >1: 
        middle = len(moviesID)//2 #Finding the middle of the moviesIDay 
        left = moviesID[:middle] # Dividing the moviesIDay elements  
        rigth = moviesID[middle:] # into 2 halves 
  
        mergeSort(left) # Sorting the first half 
        mergeSort(rigth) # Sorting the second half 
  
        leftCount = 0
        rigthCount = 0
        middleCount = 0
          
        # Copy data to temp moviesIDays L[] and R[] 
        while leftCount < len(left) and rigthCount < len(rigth): 
            if left[leftCount].movieRate > rigth[rigthCount].movieRate: 
                moviesID[middleCount] = left[leftCount] 
                leftCount+=1
            else: 
                moviesID[middleCount] = rigth[rigthCount] 
                rigthCount+=1
            middleCount+=1
          
        # Checking if any element was left 
        while leftCount < len(left): 
            moviesID[middleCount] = left[leftCount] 
            leftCount+=1
            middleCount+=1
          
        while rigthCount < len(rigth): 
            moviesID[middleCount] = rigth[rigthCount] 
            rigthCount+=1
            middleCount+=1

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


def filterByTag(moviesHashTable, tagList):
    taggedMovies = []
    hasAllTags = True
    for i in range(0, len(moviesHashTable.map)):
        if moviesHashTable.map[i] != None:
            for tag in tagList:
                tag = '"' + tag + '"'
                if not tag in moviesHashTable.map[i].movieTags:
                    hasAllTags = False
                    break
            if hasAllTags == True:
                taggedMovies.append(moviesHashTable.map[i])
            hasAllTags = True    
            
    return taggedMovies

def printTaggedMovies(moviesHashTable, tagList):
    taggedMovies = filterByTag(moviesHashTable, tagList)
    for i in range(0, len(taggedMovies)):
        print("Title: " + taggedMovies[i].movieName,
              "Genres: " + taggedMovies[i].movieGenres,
              "Rating: " + str(taggedMovies[i].movieRate),
              "Count: " + str(taggedMovies[i].movieCount))

moviesTrieTree = Trie() 
moviesHashTable = MovieHashTable(131381) 
# creating the trie structure with the  
# given set of strings. 
moviesTrieTree.buildTrie(moviesHashTable) 
  
# autocompleting the given movieName using  
# our trie structure. 



userInput = "default"

while userInput != "exit":
    print("Search movies by typing movie, user, top, or tags")
    userInput = raw_input()
    if "movie " in userInput:
        moviesTrieTree.printAutoSuggestions(userInput[6:])
        for element in moviesTrieTree.movieIDList:
            print(
            "ID: " + moviesHashTable.map[int(element)].movieID,
            "Title: " + moviesHashTable.map[int(element)].movieName,
            "Genres: " + moviesHashTable.map[int(element)].movieGenres, 
            "Rate: " + str(moviesHashTable.map[int(element)].movieRate),
            "Count: " + str(moviesHashTable.map[int(element)].movieCount)
            )
        moviesTrieTree.movieIDList = []    
    elif "top " in userInput:
        userInput = userInput.split(' ')
        topNumber = userInput[1]
        userGenre = userInput[2]
        printTopMovies(moviesHashTable, topNumber, userGenre)
    elif "tags " in userInput:
        userInput = userInput.split("'")
        tagList = userInput[1::2]
        printTaggedMovies(moviesHashTable, tagList)


    