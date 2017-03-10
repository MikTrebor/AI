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
import copy

def entropies(data): #takes lists of lists with header no answers
    elist = []
    for i in range(0, len(data[0])):
        etemp = 0.0
        f = freq_list(data)[i]
        for freq in f.values():
            ptemp = freq/len(data)
            etemp += ptemp * math.log(ptemp,2)
        elist.append(-etemp)
    # print(freq_list(data)[0])
    # print(elist)
    return elist

def csv_to_list(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        temp_list = list(reader)
    return temp_list

def freq_list(data): #takes lists of lists without header+ answer
    flist = []
    if len(data) > 0:
        for i in range(0, len(data[0])):
            freqs = {}
            for val in data:
                if (val[i] in freqs):
                    freqs[val[i]] += 1
                else:
                    freqs[val[i]]  = 1
            flist.append(freqs)
    return flist

def all_same(data): #takes list of lists with header with answers
    if len(data)==1:
        return False
    dtemp = data[1][len(data[1])-1]
    for d in data[1:]:
        if (not(d[len(data[1])-1]==dtemp)):
            return False
    return True

def extract(ds, col, val):#data set, col number, value search
    # print("\nexttract " + val + " from col " + str(col))
    # print(ds)
    temp = []
    for d in ds:
        if d[col] == val:
            temp.append(d)
        d.pop(col)

    # print("\n\nextracted " +str(temp) +"\n")
    return temp

def best_info_gain(data): #takes list of lists with answers + header
    dtemp = []
    for row in data:
        dtemp.append(row[1:])
    return entropies(dtemp).index(min(entropies(dtemp)))

def make_tree(DS, level):
    temp = copy.deepcopy(DS)
    best_col_num = best_info_gain(DS)
    best_col = temp[0][best_col_num]
    print("---" * level, best_col, "?")
    # print("best_col", best_col)
    # print("slice" + str(freq_list(DS[1:])))
    for val in freq_list(DS[1:])[best_col_num]:

        # print("\n ds" + val)
        # print(temp)
        # print("\n original" + str(DS))
        new_ds = extract(temp[1:], best_col_num, val)
        header = temp[0]
        header.pop(best_col_num)
        new_ds.insert(0, header)
        if all_same(new_ds):
            print("---" * level + ">", val, "...", freq_list(new_ds[1:])[len(new_ds[1])-1])
        else:
            if len(new_ds)>1:
                print("---" * level + ">", val, "...", freq_list(new_ds[1:])[len(new_ds[1])-1])
            else:
                make_tree(new_ds, level+1)

def main():
    myList = csv_to_list("tennis_tree.csv")
    for d in myList:
        d.pop(0)
    make_tree(myList, 1)


if __name__ == "__main__":
    main()