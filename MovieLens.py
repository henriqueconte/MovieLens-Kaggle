import re

def hashConflictNumber(key):
    hashvalue = key % 27799
    return hashvalue

def hashConflictString(key):
    hashValue = 0
    for i in range(len(key)):
        hashValue += (ord(key[i]) * (31**i)) % 27799
        hashValue %= 27799
    return hashValue

class movieInfo(object):
    def __init__(self, movieID, movieName, movieGenres):
        self.movieID = movieID
        self.movieName = movieName
        self.movieGenres = movieGenres
        self.movieRateSum = 0
        self.movieCount = 0
        self.movieRate = 0
        self.movieTags = []
        
class userMovieInfo(object):
    def __init__(self, userRating, movieName, movieCount, movieRate):
        self.userRating = userRating
        self.movieName = movieName
        self.movieCount = movieCount
        self.movieRate = movieRate

class userInfo(object):
    def __init__(self, userID):
        self.userID = userID
        self.userRatedMovies = []
        self.h = []

class MovieHashTable(object):
    """ Busca Linear | h1 """
    def __init__(self,size):
        self.size = size
        self.map = [None] * self.size
        self.used = [False] * self.size

    def insere(self,key, movieInfo):

        if self.map[key] is None:
            self.map[key] = movieInfo
            self.used[key] = True
        else:
            hashValue = hashConflictNumber(key)
            keyValue = [key, movieInfo]
            self.map[h].append(keyValue)

    def pesquisa(self,key):
        keyHash = hashConflictNumber(key)
        if self.map[key] is not None:
            return self.map[key]
            for element in self.map[key].movieTags:
                if keyHash == element:
                    return None
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

class UserHashTable(object):
    """ Busca Linear | h1 """
    def __init__(self,size):
        self.size = size
        self.map = [None] * self.size
        self.used = [False] * self.size

    def insere(self,key, userInfo):
        if self.map[key] is None:
            self.map[key] = userInfo
            self.used[key] = True
        else:
            hashValue = hashConflictNumber(key)
            keyValue = [key, userInfo]
            self.map[h].append(keyValue)

    def pesquisa(self,key):
        return self.map[key]
        keyHash = hashConflictNumber(key)
        if self.map[key] is not None:
            return self.map[key]
            for element in self.map[key].h:
                if keyHash == element:
                    return None
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

    def buildUserHashTable(self):
        reader = open("rating.csv", "r")
        reader.readline()
        for line in reader:
            stringLine = line.split(',')
            userID = int(stringLine[0])
            movieID = int(stringLine[1])
            userRating = float(stringLine[2])
            movie = getMovieById(movieID)
            actualMovieInfo = userMovieInfo(userRating, movie.movieName, movie.movieCount, movie.movieRate)
            actualUserInfo = userInfo(userID)
            if self.map[userID] is not None:
                self.map[userID].userRatedMovies.append(actualMovieInfo)
            else:
                self.insere(userID, actualUserInfo)
                self.map[userID].userRatedMovies.append(actualMovieInfo)
        reader.close()

class TrieNode(): 
    def __init__(self): 
          
        self.children = [None] * 330 
        self.leaf = False
        self.movieID = 0

class Trie(): 
    def __init__(self): 
        self.root = TrieNode() 
        self.movieIDList = [] 
  
    def buildTrie(self, moviesHashTable): 
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
        node = self.root 
        for letter in list(movieName): 
            if not node.children[ord(letter)]: 
                node.children[ord(letter)] = TrieNode() 
  
            node = node.children[ord(letter)] 
  
        node.leaf = True
        node.movieID = movieID

    def search(self, movieName): 
          
        node = self.root 
        found = True
  
        for letter in list(movieName): 
            if not node.children[ord(letter)]: 
                found = False
                break
  
            node = node.children[ord(letter)] 

        return node 
  
    def moviesRecorded(self, node): 

        if node == None:
            return
        
        if node.movieID != 0:
            self.movieIDList.append(node.movieID)
        
        for element in node.children:
            self.moviesRecorded(element)

            
  
    def printPrefixMovies(self, movieName): 
          
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
           self.moviesRecorded(node)  


def mergeSort(moviesID): 
    if len(moviesID) >1: 
        middle = len(moviesID)//2 
        left = moviesID[:middle]
        right = moviesID[middle:]
  
        mergeSort(left)
        mergeSort(right)
  
        leftCount = 0
        rightCount = 0
        middleCount = 0

        while leftCount < len(left) and rightCount < len(right): 
            if left[leftCount].movieRate > right[rightCount].movieRate: 
                moviesID[middleCount] = left[leftCount] 
                leftCount+=1
            else: 
                moviesID[middleCount] = right[rightCount] 
                rightCount+=1
            middleCount+=1
          
        while leftCount < len(left): 
            moviesID[middleCount] = left[leftCount] 
            leftCount+=1
            middleCount+=1
          
        while rightCount < len(right): 
            moviesID[middleCount] = right[rightCount] 
            rightCount+=1
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

def getMovieById(movieId):
    return moviesHashTable.pesquisa(movieId)

def printUserMovies(userID):
    userMoviesNode = usersHashTable.pesquisa(userID)
    userRatedMovies = userMoviesNode.userRatedMovies
    if userMoviesNode is not None:
        for i in range(len(userRatedMovies)):
            print("User: " + str(userID),
                "User rating: " + str(userRatedMovies[i].userRating),
                "Title: " + userRatedMovies[i].movieName,
                "Rating: " + str(userRatedMovies[i].movieRate),
                "Count: " + str(userRatedMovies[i].movieCount))

moviesTrieTree = Trie() 
moviesHashTable = MovieHashTable(131381) 
usersHashTable = UserHashTable(150000)

moviesTrieTree.buildTrie(moviesHashTable) 
usersHashTable.buildUserHashTable()

userInput = "default"

while userInput != "exit":
    print("Search movies by typing movie, user, top, or tags")
    userInput = raw_input()
    if "movie " in userInput:
        moviesTrieTree.printPrefixMovies(userInput[6:])
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
    elif "user" in userInput:
        userInput = userInput.split(' ')
        userId = int(userInput[1])
        print(userId)
        printUserMovies(userId)