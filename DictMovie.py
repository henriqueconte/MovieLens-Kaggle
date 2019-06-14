# Python3 program to demonstrate auto-complete  
# feature using Trie data structure. 
# Note: This is a basic implementation of Trie 
# and not the most optimized one. 

import re

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
  
    def formTrie(self): 
          
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
            movieName = stringLine[1]
            movieName = movieName[1:]
            movieName = movieName[:-1]
            self.insert(movieName,movieID)

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
            print(key)
            printedMovie = True

        if printedMovie == False:
           self.suggestionsRec(node, temp_word) 
  
        #    for s in self.word_list: 
        #        print(s) 

        return 1

key = "Star"

# creating trie object 
t = Trie() 
  
# creating the trie structure with the  
# given set of strings. 
t.formTrie() 
  
# autocompleting the given key using  
# our trie structure. 
t.printAutoSuggestions(key)
