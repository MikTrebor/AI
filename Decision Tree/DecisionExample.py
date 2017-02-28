import math

def entropy(freq_list):
    tot_sum= 0
    output = 0
    for i in freq_list:
        tot_sum+=i
    for x in freq_list:
        weight = x/tot_sum
        output+= (weight*math.log(weight,2))
        return output

def remainder(list_list):
    output = 0
    tot_sum=0
    for ind in list_list:
        tot_sum += sum(ind)

    for ind in list_list:
        output += ((sum(ind)/tot_sum)*entropy(ind))
    return output
