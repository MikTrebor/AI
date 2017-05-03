import numpy as np
import random

def step(x):
    return 1 if x > 0 else 0

def classify(x, w):
    return step(np.dot(x,w))

def true_class(x):
    return x[1]

def accuracy_list(ts, w):
    return [abs(true_class(x) - classify(x[0], w)) for x in ts]

def accuracy_rate(ts, w):
    return accuracy_list(ts, w).count(0) / len(ts)

def learn_boolean_function(training_set, num_epochs, lrate = 1):
    weights = np.zeros(len(training_set[0][0]))
    while(accuracy_rate(training_set, weights) < .999 and num_epochs > 0):
        for x in training_set:
            f = classify(x[0], weights)
            weights = weights + x[0] * (true_class(x) - f) * lrate

            s += abs(x-classify(x[0], weights))
    acc = 1 - (s/len(training_set))
    return (f, weights, acc)







# from perceptron import *

def make_domain(n):
    return [ [(j>>b)&1 for b in range(n)] for j in range(2**n)]

def make_training_set(domain, b):
    return [ [np.array(domain[i]+[1]),(b>>i)&1] for i in range(len(domain))]

def main(NUM_VARS):
    miss_count = 0
    all_counts = []
    D = make_domain(NUM_VARS)
    r = 2 ** 2 ** NUM_VARS
    for x in range(r):
        TS = make_training_set(D, x)
        fcn_str = "".join([str(row[1]) for row in TS])
        (count, weights, acc) = learn_boolean_function(TS, num_epochs=200, lrate = 1)
        if (acc < 0.999): miss_count += 1
    print("Overall learnability: %i/%i = %4.2f" % (r - miss_count, r, (r - miss_count) / r))

main(int(input("Number of Vars")))