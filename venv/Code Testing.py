import nltk
import math
import spacy
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
nlp = spacy.load("en_core_web_sm")
syns = wn.synsets("program")
# # word1 = wn.synset('bad.n.01')
# # word2 = wn.synset('good.n.01')
# # print(word1.wup_similarity(word2))
# # print(word1.path_similarity(word2))
# i = ['president obama', 'accepted', 'the nobel peace prize']
# i[0] = WordNetLemmatizer().lemmatize(i[0],'n')
# i[1] = WordNetLemmatizer().lemmatize(i[1],'v')
# i[2] = WordNetLemmatizer().lemmatize(i[2],'n')
#
# print(i)
#
# def contains(a, b):
#     #checks substrings as well
#     a = a.lower()
#     b = b.lower()
#     if a == b:
#         return True
#     else:
#         if a in b or b in a:
#             return True
#     return False
#
# print(contains('the coronavirus', 'coronavirus antibodies'))

# About 21 percent, test, coronavirus antibodies
# What percent, has, the coronavirus

# 1 3 1   # 2 2 2
def wordweight(text):
    text = text.lower()
    text = text.split()
    wordweightdict = {}
    for i in text:
        i = i.replace('.', '')
        i = i.replace(',', '')
        i = i.replace('!', '')
        i = i.replace('?', '')
        if i in wordweightdict:
            wordweightdict[i] += 1
        else:
            wordweightdict[i] = 1
    return wordweightdict

def returnWeight(word, wordweightdict):
    if ' ' in word:
        word = word.split()
        highesti = 0
        for j in word:
            i = wordweightdict[j]
            if i == 1:
                i = (1)
            if i == 2 or i == 3:
                i = (0.9)
            if i in [4, 5, 6]:
                i = (0.75)
            if i in [7, 8, 9, 10]:
                i = (0.5)
            if i > 10:
                i = (3/i)
            if i > highesti:
                highesti = i
        return highesti
    else:
        i = wordweightdict[word]
        if i == 1:
            i = (1)
        if i == 2 or i == 3:
            i = (0.9)
        if i in [4, 5, 6]:
            i = (0.75)
        if i in [7, 8, 9, 10]:
            i = (0.5)
        if i > 10:
            i = (3 / i)
        return i

p = returnWeight('the war', wordweight('the war was not very cool. in fact, the war was not cool at all. the war. the war'))
print(wordweight('the war was not very cool. in fact, the war was not cool at all. the war. the war'))
print(p)