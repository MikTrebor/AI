# 1: loop over all columns + pick best one (freq counts, entropy)
# 2: extract (ds, col, val)
#     returns new DS = {DS | col == val}

# ---------------------------------------------------------------
# make_tree(DS, level):
#     best_col = best col in DS using entropy
#     print("---" * level, best, "?")
#     for val in best_col:
#         new_ds = extract(ds, best_col, valu)
#         if new_ds is ALL the same answer:
#             print("---" * level + ">", val, answer)
#         else:
#             print("---" * level + ">" + "...")
#             make_tree(new_ds, level+1)

import csv
import math

def entropies(data):
    elist = []

    for i in range(0, len(data[0])):
        etemp = 0.0
        f = freq_list(data)[i]
        for freq in f.values():
            etemp += (-freq/len(data)) * math.log(freq/len(data), 2)
        elist.append(etemp)
    return elist

def csv_to_list(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        temp_list = list(reader)
    return temp_list

def freq_list(data):
    flist = []
    for i in range(0, len(data[0])):
        freqs = {}
        # Calculate the frequency of each of the values in the target attr
        for record in data:
            if (record[i] in freqs):
                freqs[record[i]] += 1.0
            else:
                freqs[record[i]]  = 1.0
        flist.append(freqs)
    return flist

def best_info_gain(data):
     return entropies(data).index(min(entropies(data)))

def main():
    myList = csv_to_list("tennis_tree.csv")
    cats = len(myList[0])-1
    days = len(myList)-1
    myList.pop(0)
    for day in myList:
        day.pop(0)

    print(myList, cats, " ", days)
    print(entropies(myList))
    print("lowest" + (str(best_info_gain(myList))))


if __name__ == "__main__":
    main()