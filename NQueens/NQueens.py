# Name: Robert Kim
# Block: 4
# Email: 2018rkim@tjhsst.edu
#temp

import time
import random
import csv

class NQueens:
    def __init__(self, state=None, choices=None, n=8, parent=None):
        self.state = state
        self.choices = choices
        self.n = n
        self.parent = parent

    def assign(self, var, value):
        if var >= self.n:
            return False
        if var < 0:
            return False
        self.state[var] = value
        # remove value from all other columns' choices
        for col in range(self.n):
            if value in self.choices[col]:
                self.choices[col].remove(value)
        # remove all choices for this column
        self.choices[var] = set()
        temp = self.n-1 - var
        if temp >=0:
            for num in range(temp):
                cur = num+1
                # remove diagonally, right and down
                if value+cur in self.choices[var+cur]:
                    self.choices[var+cur].remove(value+cur)
            for num in range(temp):
                cur = num+1
                # remove diagonally, right and up
                if value-cur in self.choices[var+cur]:
                    self.choices[var+cur].remove(value-cur)

        temp = var
        for num in range(temp):
            cur = num+1
            if value+cur < self.n:
                # remove diagonally, left and down
                if value+cur in self.choices[var-cur]:
                    self.choices[var-cur].remove(value+cur)
        for num in range(temp):
            cur = num+1
            if value-cur > -1:
                # remove diagonally, left and up
                if value-cur in self.choices[var-cur]:
                    self.choices[var-cur].remove(value-cur)
        return True

    def goal_test(self):
        inBounds = True
        temp = set()
        for num in range(self.n):
            temp.add(num)
        for num in self.state:
            if not num in temp:
                inBounds = False
            if num >= self.n:
                inBounds = False
            if num < 0:
                inBounds = False
        return inBounds

    def get_next_var(self):
        # Plain: Choose leftmost column
        for col in range(len(self.state)):
            # queen at this col in unasssigned
            if self.state[col] == self.n:
                return col

        # HEURISTIC 1: Random col
        #col = random.randint(0, self.n-1)
        #while True:
        #    if self.state[col] == self.n:
        #        return col
        #    else:
        #        col = random.randint(0, self.n-1)

        # HEURISTIC 2: Col with fewest choices (tiebreaker: random)
        #smallests = set()
        #for num in range(self.n):
        #    for col in range(len(self.state)):
                 # queen there is unassigned
        #        if self.state[col] == self.n:
        #            if len(self.choices[col]) == num+1:
        #                smallests.add(col)
        #    if len(smallests) > 0:
        #        return smallests.pop()

        # HEURISTIC 3: Col with fewest choices (tiebreaker: furthest left)
        #for num in range(self.n):
        #    for col in range(len(self.state)):
                 # queen there is unassigned
        #        if self.state[col] == self.n:
        #            if len(self.choices[col]) == num+1:
        #                return col


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
                    child = NQueens(list(current.state), list(set(x) for x in current.choices), current.n, current)
                    nodescreated = nodescreated + 1
                    if child.assign(var, value):
                        fringe.append(child)

    def __str__(self):
        matrix = [["[ ]" for col in range(self.n)] for row in range(self.n)]
        for col in range(self.n):
            if self.state[col] < self.n:
                matrix[self.state[col]][col] = "[Q]"
            else:
                matrix[self.state[col]][col] = "[O]"
        return str('\n'.join([''.join(['{:3}'.format(item) for item in row]) for row in matrix]))


def setup_board(size):
    state = list()
    for ind in range(size):
        state.append(size)
    choices = list(set())
    temp = set()
    for ind in range(size):
        temp.add(ind)
    for ind in range(size):
        choices.append(temp.copy())
    return state, choices

num = input("Size: ")
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
        start = NQueens(myState, myChoices, temp)
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
        myWriter.writerow(line)

