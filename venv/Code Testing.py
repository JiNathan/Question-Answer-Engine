import nltk
from nltk.corpus import wordnet as wn
syns = wn.synsets("program")
word1 = wn.synset('people.n.01')
print(word1)
word2 = wn.synset('person.n.01')

print(word1.wup_similarity(word2))
print(word1.path_similarity(word2))
