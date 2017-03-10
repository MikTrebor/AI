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
            ptemp = freq/len(data)
            etemp += ptemp * math.log(ptemp,2)
        elist.append(-etemp)
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
        for record in data:
            if (record[i] in freqs):
                freqs[record[i]] += 1.0
            else:
                freqs[record[i]]  = 1.0
        flist.append(freqs)
    return flist

def all_same(data):
    print(data)
    dtemp = data[0]
    for d in data:
        if (not(d==dtemp)):
            return False
    return True

def extract(ds, col, val):#data set, col number, value search
    temp = []
    print("colnum" +str(col))
    print("val" +val)
    for d in ds:
        # print(d[col])
        if d[col] == val:
            temp.append(d)
    return temp

def best_info_gain(data):
    dtemp = []
    for row in data:
        dtemp.append(row[1:len(data[0])-1])
    return entropies(dtemp).index(min(entropies(dtemp)))

def make_tree(DS, level):
    best_col_num = best_info_gain(DS)
    best_col = DS[0][best_col_num]
    print("---" * level, best_col, "?")
    print(best_col_num)
    print("data" + str(DS[best_col_num]))
    for val in r:
        # print(DS[best_col_num])
        new_ds = extract(DS, best_col_num, val)

        # print(new_ds)
    #     if all_same(new_ds):
    #         print("---" * level + ">", val, new_ds[0][len(new_ds[0])])
    #     else:
    #         print("---" * level + ">" + "...")
    #         make_tree(new_ds, level+1)

def main():
    myList = csv_to_list("tennis_tree.csv")
    cats = len(myList[0])-1
    days = len(myList)-1
    # myList.pop(0)
    # for day in myList:
    #     day.pop(0)

    # print(myList, cats, " ", days)
    # print(entropies(myList))
    make_tree(myList, 0)
    # print(best_info_gain(myList))


if __name__ == "__main__":
    main()