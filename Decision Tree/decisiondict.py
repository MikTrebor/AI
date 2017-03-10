import random
import math
import csv

CLASS_idx = 0 # index of the answer column after reading CSV file

def get_data(file):
    global CLASS_idx
    with open(file) as csvfile:
        """ Read data in from a csv file
            stores the index of the classification column
            in a global variable
        """
        reader = csv.reader(csvfile)
        headers = next(reader)[1:]
        ds = {row[0]: row[1:] for row in reader}
        csvfile.close()
    CLASS_idx = len(headers) - 1
    return ds, headers

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

def make_tree(ds, level, parents):
    initial_h = freq_entropy(freq_dist(ds))
    best = max((initial_h - parameter_entropy(ds, i), i) for i in range(CLASS_idx))

    p = best[1]
    # print("---" * level, headers[p], "(initial = %3.3f, gain=%3.3f)"%(initial_h, best[0]), "?")
    print("---" * level, headers[p], "?")


    for v in val_set(ds, p):
        new_ds = restrict(ds, p, v)
        freqs = freq_dist(new_ds)
        if freq_entropy(freqs) < 0.001:
            # print("---" * level + ">", headers[p], "=", v, freqs)
            print("---" * level + ">", v, freqs)

        else:
            # print("---" * level + ">", headers[p], "=", v, "...", freqs)
            print("---" * level + ">", v, freqs)
            make_tree(new_ds, level + 1, parents + [p])

DS, headers = get_data("cook.csv")
make_tree(DS, 1, [0])