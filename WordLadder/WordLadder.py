import time

dictionary = dict()#adjacencies
textFile = set()#text file
alphabet = "abcdefghijklmnopqrstuvwxyz"

def processWord(entry):  #returns one textFile entry (word + its neighbors) and adds the entry to dictionary  
    for x in range(len(entry)):
        addNeighbors(entry, x, len(entry))

def addNeighbors(word, index, length): #returns variations of a word, changing the letters at index index
    for letter in alphabet: #tries each letter at index index
        newWord = word[0:index]+letter+word[index+1:]
        if inTextFile(newWord):#word exists
            if(not word == newWord):#word is not same as previous
                if word in dictionary: #original word is already in dictionary
                    dictionary[word].add(newWord)
                else:
                    dictionary[word] = {newWord} #create new dictionary entry
            
def inTextFile(word): #checks if the new word is in the list of words
    return word in textFile

def processFile(inputFile):    
    return set(line.strip() for line in open(inputFile))

class Node():
    word = None
    neighbors = None
    parent = None
    depth = None
    def __init__(self, word, neighbors = None, parent = None, depth = 0):
        self.word = word
        self.neighbors = neighbors
        self.parent = parent
        self.depth = depth
    def getParent(self):
        return self.parent
    def getWord(self):
        return self.word
    def isSolution(self, other):
        return other==self.getWord()
    def getNeighbors(self):
        return self.neighbors
    def incrementDepth(self):
        self.depth = self.depth+1
    def getDepth(self):
        return self.depth
    def hasParent(self):
        return not self.parent == None


def diagnostic(node):#omit
    print("Word: " + node.getWord() + " Neighbors: " + str(node.getNeighbors()))#omit

def findPath(start, end):
    fringe = [Node(start, dictionary[start])]
    tried = set([start])
    while len(fringe) > 0:

        nodeCurrent = fringe.pop(0)
        if nodeCurrent.isSolution(end):
            nodeCurrent.incrementDepth()
            return nodeCurrent.getDepth()
        temp = nodeCurrent.getNeighbors()
        print(end)
        print(len(fringe))
        for item in temp:
            ableToAdd = True
            if item in tried:
                ableToAdd = False
            if len(fringe) > 0:
                for word in fringe:
                    if word.getWord() == item:
                        ableToAdd = False
            if ableToAdd:
                fringe = fringe + [Node(item, dictionary[item], nodeCurrent, nodeCurrent.getDepth()+1)]
                tried.add(item)
    return "-"

def calculateWord(start, end):
    startTime = time.clock()
    depth = findPath(start, end)
    endTime = time.clock()
    if depth < 10:
        depth = " " + str(depth)
    length = round((endTime-startTime), 5)
    if length < 10:
        length = " " + str(length)
    #print(start, end, depth, length)
    steps = int(depth)-1
    newLine = start + " " + end + " " + str(steps) + " " + str(length)
    output.write(newLine + "\n")

textFile = processFile("words.txt")
for word in textFile:
    processWord(word)

input = open("puzzlesA.txt", "r")
output = open("solutions.txt", "w")
#startWord = input("Start word? ")
#endWord = input("Target word? ")
for line in input:
    pair = line[:13].split(' ')
    calculateWord(pair.pop(0), pair.pop(0))
print("Done!")



    
