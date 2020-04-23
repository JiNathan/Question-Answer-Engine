import nltk
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

def contains(a, b):
    #checks substrings as well
    a = a.lower()
    b = b.lower()
    if a == b:
        return True
    else:
        if a in b or b in a:
            return True
    return False

print(contains('president Obama', 'obama'))


# 1 3 1   # 2 2 2