# Python program for insert and search 
# operation in a Trie 
  
class TrieNode: 
      
    # Trie node class 
    def __init__(self): 
        self.children = [None]*220

        # isEndOfWord is True if node represent the end of the word 
        self.isEndOfWord = False
        self.movieID = 0
  
class Trie: 
      
    # Trie data structure class 
    def __init__(self): 
        self.root = self.getNode() 
  
    def getNode(self): 
      
        # Returns new trie node (initialized to NULLs) 
        return TrieNode() 
  
    def _charToIndex(self,ch): 
          
        # private helper function 
        # Converts key current character into index 
        # use only 'a' through 'z' and lower case 
        #print(ord(ch))
        #print(ord(ch) - ord(' '))
        return ord(ch)-ord(' ') 
  
  
    def insert(self,key,movieID): 
          
        # If not present, inserts key into trie 
        # If the key is prefix of trie node,  
        # just marks leaf node 
        pCrawl = self.root 
        length = len(key) 
        for level in range(length): 
            index = self._charToIndex(key[level]) 
  
            # if current character is not present 
            if not pCrawl.children[index]:
                pCrawl.children[index] = self.getNode()
                print(pCrawl.children[index])  
            pCrawl = pCrawl.children[index] 
  
        # mark last node as leaf 
        pCrawl.isEndOfWord = True
        pCrawl.movieID = movieID

    def search(self, key): 
          
        # Search key in the trie 
        # Returns true if key presents  
        # in trie, else false 
        pCrawl = self.root 
        length = len(key) 
        for level in range(length): 
            index = self._charToIndex(key[level]) 
            if not pCrawl.children[index]: 
                return False
            pCrawl = pCrawl.children[index] 
  
        return pCrawl != None and pCrawl.isEndOfWord 

def saveTrieNodes(trieTree):
    reader = open("movie.csv", "r")
    reader.readline()
    i = 0
    for line in reader:
        stringLine = line.split(',')
        trieTree.insert(stringLine[1],stringLine[0])
        i += 1

# driver function 
def main(): 
  
    # # Input keys (use only 'a' through 'z' and lower case) 
    # keys = ["the","a","there","anaswe","any", 
    #         "by","their"] 
    output = ["Not present in trie", 
               "Present in trie"] 
  
    # # Trie object 
    # t = Trie() 
    trieTree = Trie()
    saveTrieNodes(trieTree)
    # # Construct trie 
    # for key in keys: 
    #     t.insert(key) 
    
    # # Search for different keys 
    print("{} ---- {}".format("Petals on the",output[trieTree.search("(2014)")])) 
    # print("{} ---- {}".format("these",output[t.search("these")])) 
    # print("{} ---- {}".format("their",output[t.search("their")])) 
    # print("{} ---- {}".format("thaw",output[t.search("thaw")])) 

  
if __name__ == '__main__': 
    main() 