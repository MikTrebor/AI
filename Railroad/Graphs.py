import pickle
from math import pi, acos, sin, cos
import time
coords = dict(tuple()) # Id, Coords
graph = dict(list()) # ID, List of Neighbor IDs
names = dict() # ID, City
id = dict() # City, ID
closed = set()
#G = {None: None}

def calcd(t1, t2):
    (y1, x1) = t1
    (y2, x2) = t2
    if not type(y2) is str:
        return 0.0
    y1 = float(y1)
    x1 = float(x1)
    y2 = float(y2)
    x2 = float(x2)
    R = 3958.76 # miles = 6371 km
    y1 *= pi/180.0
    x1 *= pi/180.0
    y2 *= pi/180.0
    x2 *= pi/180.0
    return acos(sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1)) * R

class Node:
    city = None
    parent = None
    children = None
    id = None
    f = None
    g = None
    h = None
    goal = None

    def __init__(self, id=None, children=None, parent=None, goal=None):
        self.id = id
        self.children = children
        self.parent = parent
        self.goal = goal

    def edgeCost(self, state, other):
        # return G[state][other]
        return calcd(coords[state], coords[other])

    def heuristic(self, s, other):
        return calcd(coords[s], coords[other])

    def expand(self):
        successors = []
        for i in self.children:
            s = makeNode(i, self, self.goal)
            s.g = self.g + self.edgeCost(self.id, i)
            s.h = self.heuristic(s.id, id[self.goal])
            s.f = s.g + s.h
            #s.depth = self.depth + 1
            if i not in closed:
                successors.append(s)
        return successors

    def getParent(self):
        return self.parent

    def getCity(self):
        if self.id in names:
            return names[self.id]
        else:
            return "nocity"

    def getID(self):
        return self.id

    def startG(self):
        self.g = float(0.0)

def makeNode(id, parent=None, end=None):
    return Node(id, graph[id],parent,end)

def goalTest(n, end):
    return n.getID() == id[end]

def popMin(fringe):
    fringe.sort(key=lambda x: x.f, reverse=False) # pulled from online- alternative to heappq
    return fringe.pop()

def solution(node):
    return node.f

def graphSearch(start, end):
    closed = set() #<-should do this here, but it takes FOREVER to finish
    fringe = [makeNode(id[start], None, end)]
    fringe[0].startG()
    begin = time.time()
    while True:
        if len(fringe) == 0:
            return None
        n = popMin(fringe)
        if not n.getCity() == "nocity":
            print(n.getCity())
        if goalTest(n, end):
            finish = time.time()
            return (solution(n),finish-begin)
        if n.id not in closed:
            closed.add(n.id)
            fringe.extend(n.expand())

def work(infile, outfile):
    for line in infile:
        (u,v) = line.split(", ")
        start = u
        start = start.strip()
        end = v.rstrip("\n")
        #distance, time = graphSearch(start, end)
        #print("%20s %20s %8.3f %4.3f" % (start, end, distance, time), file=outfile)
        #print("%20s %20s %8.3f %4.3f" % (start, end, distance, time), file=outfile)
        outfile.write(str(start)+str(end)+str(graphSearch(start, end))+"\n")
        closed = set()

coords = pickle.load(open("coords.txt", "rb"))
graph = pickle.load(open("graph.txt", "rb"))
names = pickle.load(open("names.txt", "rb"))
id = pickle.load(open("id.txt", "rb"))

#for (u,v) in graph:
 #   G[u][v] = calcd(coords[u],coords[v])
infile = open("test.txt", "r")
outfile = open("solutions.txt", "w")
#graphSearch("Jacksonville", "Atlanta")
work(infile, outfile)

















