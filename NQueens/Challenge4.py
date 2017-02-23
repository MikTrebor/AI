# Name: Robert Kim
# Block: 4
# Email: 2018rkim@tjhsst.edu


import time
import random
import csv
size = 9

class Sudoku:
    def __init__(self, state=None, choices=None, n=81):
        self.state = state
        self.choices = choices
        self.n = n

    def findbox(self, index):
        for box in boxlist:
            if index in box:
                return box

    def assign(self, var, value):
        if var >= self.n * self.n: # too big
            return False
        if var < 0: # too small
            return False
        self.state[var] = value
        tempRow = 0
        # remove from row
        for start in colStarts:
            if start <= var:
                tempRow = start
        for rowIndex in range(tempRow, tempRow+self.n): # for indices in row
            if value in self.choices[rowIndex]:
                self.choices[rowIndex].remove(value)
        # remove from col
        for row in range(1, self.n): # goes up
            multiplier = row*self.n
            if var-multiplier >= 0:
                if value in self.choices[var-multiplier]:
                    self.choices[var-multiplier].remove(value)

        for row in range(1, self.n): # goes down
            multiplier = row*self.n
            if var+multiplier < self.n*self.n:
                if value in self.choices[var+multiplier]:
                    self.choices[var+multiplier].remove(value)

        #remove from box
        for index in self.findbox(var):
            if value in self.choices[index]:
                self.choices[index].remove(value)
        return True

    def goal_test(self):
        #print("goaling")
        #print(self)
        for spot in self.state:
            if spot == 0:
                return False

        return True

    def get_next_var(self):
        # Plain: Choose leftmost column
        #for col in range(len(self.state)):
        #    if len(self.choices[col]) > 0:
        #        return col

        # HEURISTIC 1: Random col
        #col = random.randint(0, self.n-1)
        #while True:
        #    if self.state[col] == self.n:
        #        return col
        #    else:
        #        col = random.randint(0, self.n-1)

        # HEURISTIC 2: Col with fewest choices (tiebreaker: random)
        #smallests = set()\
        #for num in range(self.n):
        #    for col in range(len(self.state)):
                 # queen there is unassigned
        #        if self.state[col] == self.n:
        #            if len(self.choices[col]) == num+1:
        #                smallests.add(col)
        #    if len(smallests) > 0:
        #        return smallests.pop()

        # HEURISTIC 3: Col with fewest choices (tiebreaker: furthest left)
        for num in range(self.n):
            for col in range(len(self.state)):
                 # queen there is unassigned
                if self.state[col] == 0:
                    if len(self.choices[col]) == num+1:
                        return col


        # no choices anywhere (Safety)
        return -1

    def get_value(self, var):
        return self.choices[var]

    def dfs_search(self):
        fringe = [self]
        nodescreated = 0
        goalchecks = 0
        while True:
            if len(fringe) == 0:
                return False
            current = fringe.pop()
            goalchecks = goalchecks+1
            if current.goal_test():
                return current, nodescreated, goalchecks
            var = current.get_next_var()
            if var >= 0:
                myChoices = current.get_value(var)
                for value in myChoices:
                    child = Sudoku(list(current.state), list(set(x) for x in current.choices), current.n)
                    nodescreated = nodescreated + 1
                    if child.assign(var, value):
                        fringe.append(child)

    def __str__(self):
        c = 0
        string = "- - - - - - - - - - - - -\n"
        for i in range(self.n):
            string = string + "| "
            for j in range(self.n):
                string = string + str(self.state[c]) + " "
                if c % 3 == 2:
                    string = string + "| "
                c += 1
            string = string + "\n"
            if i % 3 == 2:
                string = string + "- - - - - - - - - - - - -\n"
        return string



def setup_board(size, puzzle):
    state = list(puzzle)
    #    state.append(".")
    choices = list(set())
    temp = set()
    for ind in range(size):
        temp.add(ind+1)
    for ind in range(size*size):
        choices.append(temp.copy())
    #print(str(state), str(choices))
    # state = [ 6 , ".", ".", ".",  2 , ".", ".", ".",  9 ",
    #         ".",  1 , ".",  3 , ".",  7 , ".",  5 , ".",
    #         ".", ".",  3 , ".", ".", ".",  1 , ".", ".",
    #         ".",  9 , ".", ".", ".", ".", ".",  2 , ".",
    #          2 , ".", ".",  8 ,  7 ,  5 , ".", ".",  3 ,
    #         ".", ".",  5 , ".",  1 , ".",  4 , ".", ".",
    #         ".",  7 , ".", ".",  8 , ".", ".",  9 , ".",
    #         ".", ".",  1 , ".",  4 , ".",  8 , ".", ".",
    #         ".", ".", ".",  2 ,  5 ,  9 , ".", ".", "."]

    # choices = [set() for i in range(size * size)]
    return state, choices

boxlist = [{ 0,  1,  2,  9, 10, 11, 18, 19, 20},{ 3,  4,  5, 12, 13, 14, 21, 22, 23},{ 6,  7,  8, 15, 16, 17, 24, 25, 26},
           {27, 28, 29, 36, 37, 38, 45, 46, 47},{30, 31, 32, 39, 40, 41, 48, 49, 50},{33, 34, 35, 42, 43, 44, 51, 52, 53},
           {54, 55, 56, 63, 64, 65, 72, 73, 74},{57, 58, 59, 66, 67, 68, 75, 76, 77},{60, 61, 62, 69, 70, 71, 78, 79, 80}]

colStarts = [0, 9, 18, 27, 36, 45, 54, 63, 72]
board = "................................................................................."
myState, myChoices = setup_board(size, board)
start = Sudoku(myState, myChoices, size)
newBoard = input("Enter board: ")
#newBoard = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
for index in range(len(list(newBoard))):
    if newBoard[index] == ".":
        start.assign(index, 0)
    else:
        start.assign(index, int(newBoard[index]))


begin = time.clock()
solution, nodesused, goals = start.dfs_search()
end = time.clock()
#print(start)
#print(start.choices)
#print(start.state)
print("duration: " + str(round(end-begin, 5)))
print(solution)

"""num = input("Size: ")
num = int(num)
multiplier = input("Multiplier: ")
multiplier = int(multiplier)
start = int(input("Start: "))
output = input("Output Name: ")
with open(output, 'w', newline='') as csvfile:
    myWriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    myWriter.writerow(["Nodes", "Goals", "Nodes Created", "Time"])
    lines = list()
    for var in range(start, num):
        temp = var*multiplier
        print(str(temp))
        myState, myChoices = setup_board(temp)
        start = Sudoku(myState, myChoices, temp)
        begin = time.clock()
        solution, nodesused, goals = start.dfs_search()
        end = time.clock()
        duration = end-begin
        print("goal checks: " + str(goals))
        print("nodes created: " + str(nodesused))
        print("duration: " + str(round(duration, 5)))
        print()
        lines.append([str(temp), str(goals), str(nodesused), str(round(duration, 5))])
    for line in lines:
        print(line)
        myWriter.writerow(line)"""

