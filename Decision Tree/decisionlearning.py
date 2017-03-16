import csv
import math
import random
from random import shuffle

CLASS_idx = 0 # index of the answer column after reading CSV file
node_count = 0
def get_data(file):
    global CLASS_idx
    with open(file) as csvfile:
        """ Read data in from a csv file
            stores the index of the classification column
            in a global variable
        """
        ds = {}
        test = {}
        reader = csv.reader(csvfile)
        headers = next(reader)[1:]
        for row in reader:
            if "?" not in set(row):
                ds[row[0]] = row[1:]
            elif "?" in set(row):
                test[row[0]] = row[1:]
        # ds = {row[0]: row[1:] for row in reader if "?" not in set(row)}
        # test = {row[0]: row[1:] for row in reader if "?" in set(row)}
        csvfile.close()
    CLASS_idx = len(headers) - 1
    return ds, test, headers

def rand_dataset(r,c):
    """ create a random binary dataset of size r x c
    """
    return {i: [random.randrange(2) for i in range(c)] for i in range(r)}

def val_list(data, column):
    """ return a list of all values contained in the domain
        of the parameter 'column'
    """
    return [val[column] for val in data.values()]

def val_set(data, column):
    """ return the set of all values contained in the domain
        of the parameter 'column'
    """
    return set(val_list(data, column))

def restrict(data, column, value): # aka extract
    """ return a dictionary corresponding to the rows in
        data in which parameter 'column' == value
    """
    return {a:data[a] for a in data if data[a][column]==value}

def freq_dist(data_dict):
    """ returns a dict where the keys are unique
        elements in the final column and the values are the
        frequency counts of those elements in data_dict.
    """
    vals = val_list(data_dict, CLASS_idx)
    return {a: vals.count(a) for a in set(vals)}

def freq_entropy(freq_dict):
    """ returns the entropy of the frequency distribution
        passed in as a dict: {(x = freq(x))}
    """
    f = list(freq_dict.values())
    s = sum(f)
    p = [i / s for i in f]
    return (-sum([i * math.log(i, 2) for i in p if i > 0]))

def parameter_entropy(data, col):
    """ returns the average entropy associated
        with the parameter in column 'col'
        in the dictionary 'data'
    """
    length = len(data)
    total = 0
    for v in val_set(data, col):
        ds = restrict(data, col, v)
        l = len(ds)
        e = freq_entropy(freq_dist(ds))
        total += l / length * e
    return total

def make_tree(ds, level, head):
    """ makes tree of Nodes, recursive
    """
    global node_count
    initial_h = freq_entropy(freq_dist(ds))
    best = max((initial_h - parameter_entropy(ds, i), i) for i in range(CLASS_idx))
    p = best[1]
    ## print("---" * level, headers[p], "(initial = %3.3f, gain=%3.3f)"%(initial_h, best[0]), "?")
    head = Node(int(headers[p][1:]))
    # print("---" * level, headers[p], "?")
    for v in val_set(ds, p):
        new_ds = restrict(ds, p, v)
        freqs = freq_dist(new_ds)
        if freq_entropy(freqs) < 0.001: # leaf
            ## print("---" * level + ">", headers[p], "=", v, freqs)
            # print("---" * level + ">", v, freqs)
            if v == 'y':
                head.yes = Node(list(freqs.keys())[0])
            if v == 'n':
                head.no = Node(list(freqs.keys())[0])

        elif freq_entropy(freqs) < .15: # low entropy
            #chose value with higher freq and make that heads value
            dfreq = freqs[list(freqs.keys())[0]]
            rfreq = freqs[list(freqs.keys())[1]]
            greater = ""
            if dfreq > rfreq:
                greater = list(freqs.keys())[0]
            else:
                greater = list(freqs.keys())[1]
            # print(greater)
            head.yes = Node(greater)
            # print(list(freqs.keys())[0])
            head.no = Node(greater)


        else: # more children
            node_count+=1

            ## print("---" * level + ">", headers[p], "=", v, "...", freqs)
            # print("---" * level + ">", v, freqs)
            if v == 'y':
                head.yes = make_tree(new_ds, level + 1, head.yes)
            if v == 'n':
                head.no = make_tree(new_ds, level + 1, head.no)
    return head

def choose_reps(dictionary, amount):
    """ returns training data set of size amount, along
        with a testing set of size len(dictionary) -
        training data size
    """
    data = dict()
    test = dict()
    count = 0
    keys = list(dictionary.keys())
    shuffle(keys)
    for i in keys:
        if count < amount:
            data[i] = dictionary[i]
        else:
            test[i] = dictionary[i]
        count += 1
    return data, test

def run_trees(data, size):
    """ returns testing set along with decision
        tree of Nodes for size size
    """
    data_set, test_set = choose_reps(data, size)
    head = Node(None)
    head = make_tree(data_set, 1, [0])
    return head, test_set

def question_guess(repid, head):
    guess_party(repid, head.yes) == guess_party(repid, head.no)
    if guess_party(repid, head.yes) == guess_party(repid, head.no):
        return guess_party(repid, head.yes)
    else: #werent equal
        if random.randint(0, 1) == 0:
            return guess_party(repid, head.yes)
        else:
            return guess_party(repid, head.no)

def guess_party(repid, head):
    """ guesses the party of representative at 'repid'
        based on decision tree with head 'head', recursive
    """
    if head.value == "democrat" or head.value == "republican":
        return head.value
    else:
        # print("vote", test_set[repid][head.value-1])
        if test_set[repid][head.value-1] == 'y':
            return guess_party(repid, head.yes)
        elif test_set[repid][head.value-1]== '?':
            return question_guess(repid, head)
        else:
            return guess_party(repid, head.no)

def actual_party(repid):
    """ returns party of representative at 'repid'
        based on last column of data set
    """
    # has_question = False
    # for answer in test_set[repid]:
    #     if answer == "?":
    #         has_question = True

    # if not has_question:
    return(test_set[repid][len(test_set[repid])-1])
    # else:
    #     return "question"

def correct_guess(repid, head):
    """ returns true if decision tree at 'head' correctly
        guesses party of representative at 'repid'
    """
    return guess_party(repid, head)==actual_party(repid)

class Node:
    """ Node class to store decision tree,
        has value which can be 'y', 'n', 'republican',
        or 'democrat'. Also stores references to
        child if yes, and child if no
    """
    def __init__(self, value="blank"):
        self.value = value
        self.no = None
        self.yes = None
        self.parent = None

DS, qs, headers = get_data("house-votes-84.csv")
head_list = {}
print("len", "percent", "nodes")
with open('output.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(['Size of Training Set', 'Accuracy', 'Number of Internal Nodes'])

    for length in range(190, 201):
        sum_percents = 0
        sum_nodes = 0
        # length = num*10
        for repeat in range(100):
            node_count = 1
            num_correct = 0
            num_incorrect = 0
            head_list[length], test_set = run_trees(DS, length)
            test_set.update(qs)
            # print(len(test_set), length, len(test_set) + length) #always equal 435
            test_reps = list(test_set.keys())
            for rep in range(len(test_reps)):
                if correct_guess(test_reps[rep], head_list[length]):
                    num_correct += 1
                else:
                    num_incorrect += 1

            sum_percents += num_correct/(num_correct+num_incorrect)*100
            sum_nodes += node_count
        print(length, round(sum_percents/100, 2), sum_nodes/100)
        csvwriter.writerow([str(length), str(round(sum_percents/100, 2)), str(sum_nodes/100)])


    # print("repid", test_reps[0])
    # print("votes", test_set[test_reps[0]])
    # print(correct_guess(test_reps[0], head_list[num]))
    # print()
    # print("head", head_list[num].value)
    # print("yes", head_list[num].yes.value)
    # print("no", head_list[num].no.value)
    # print()
