print("#################################")
print("#                               #")
print("#     Robert Kim 4th Period     #")
print("#                               #")
print("#################################")

import random
import nltk
from nltk.book import *
from nltk.corpus import stopwords
from nltk.corpus import toolbox
from nltk.corpus import gutenberg
from nltk.corpus import cmudict
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
#nltk.download()
nltk.corpus.gutenberg.fileids()



def lexical_diversity(text):
    return len(set(text)) / len(text)
def percentage(count, total):
    return 100 * count / total

def exercise7(): ##
    text7.concordance("however")
def exercise9():
    fdist1 = FreqDist([a.lower() for a in text1 if len(a) > 10])
    fdist2 = FreqDist([b.lower() for b in text2 if len(b) > 10])
    print("########")
    print("#Text 1#")
    print("########")
    print(sorted(fdist1.items()))
    print("")
    print("########")
    print("#Text 2#")
    print("########")
    print(sorted(fdist2.items()))
def exercise12():
    words = [a for a, pronounciation in cmudict.entries()]
    distinct_words = set(words)
    percent = 1- (len(distinct_words) / len(words))
    print("distinct words = " + str(len(distinct_words)))
    print("percentage of words with more than one pronounciation: " + str(percent*100))
def exercise15():
    fdist = FreqDist(brown.words())
    print(sorted([a for a in set(fdist) if fdist[a] >= 3]))
def exercise18():
    return
def exercise23():
    return
def exercise27(): ##
    #nltk.app.wordnet()
    #print(str(len(wn.synsets('dog', 'n'))))
    #print(wn.synset('dog', 'n').lemmas)
    nouns = list()
    noun_lens = list()
    for i in wn.all_synsets('n'):
        noun_lens.append(len(wn.synsets(i.name())))
    tempsum = 0
    for length in noun_lens:
        tempsum += length
    nounavg = tempsum/len(noun_lens)
    print(str(nounavg))        

if __name__ == "__main__":
    print("")
    print("exercise7()")
    exercise7()
    print("")
    print("exercise9()")
    exercise9()
    print("")
    print("exercise12()")
    exercise12()
    print("")
    print("exercise15()")
    #exercise15()
    print("")
    print("exercise18()")
    exercise18()
    print("")
    print("exercise23()")
    exercise23()
    print("")
    print("exercise27()")
    exercise27()
