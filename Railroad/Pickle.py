import pickle

coordsDict = dict(tuple())
graphDict = dict(list())
namesDict = dict()
idDict = dict()

def processFiles(file1 = "rrNodes.txt", file2 = "rrEdges.txt", file3 = "rrNodeCity.txt"):
    coordsTemp = set(line.strip() for line in open(file1))
    graphTemp = set(line.strip() for line in open(file2))
    #namesTemp = set(line.strip() for line in open(file3))
    infile = open("rrNodeCity.txt","r")
    for line in infile.readlines():
        line = line.strip("\n")
        (id, *name) = line.split(" ")
        cityName = (" ".join(name))
        namesDict[id] = cityName
        idDict[cityName] = id
    # do something with cityName and ID!
    infile.close()

    #idTemp = set(line.strip() for line in open(file3))
    for item in coordsTemp:
        temp = item.split(" ")
        coordsDict[temp[0]] = (temp[1], temp[2])
    for item in graphTemp:
        temp = item.split(" ")
        u = temp[0]
        v = temp[1]
        if u in graphDict:
            graphDict[u].append(v)
        else:
            graphDict[u] = [v]
        if v in graphDict:
            graphDict[v].append(u)
        else:
            graphDict[v] = [u]

processFiles()
pickle.dump(coordsDict, open("coords.txt","wb"))
pickle.dump(graphDict, open("graph.txt","wb"))
pickle.dump(namesDict, open("names.txt","wb"))
pickle.dump(idDict, open("id.txt","wb"))
