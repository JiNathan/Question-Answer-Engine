import nltk
import math
import spacy
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
nlp = spacy.load("en_core_web_sm")
# syns = wn.synsets("program")
# # # word1 = wn.synset('bad.n.01')
# # # word2 = wn.synset('good.n.01')
# # # print(word1.wup_similarity(word2))
# # # print(word1.path_similarity(word2))
# # i = ['president obama', 'accepted', 'the nobel peace prize']
# # i[0] = WordNetLemmatizer().lemmatize(i[0],'n')
# # i[1] = WordNetLemmatizer().lemmatize(i[1],'v')
# # i[2] = WordNetLemmatizer().lemmatize(i[2],'n')
# #
# # print(i)
# #
# # def contains(a, b):
# #     #checks substrings as well
# #     a = a.lower()
# #     b = b.lower()
# #     if a == b:
# #         return True
# #     else:
# #         if a in b or b in a:
# #             return True
# #     return False
# #
# # print(contains('the coronavirus', 'coronavirus antibodies'))
#
# # About 21 percent, test, coronavirus antibodies
# # What percent, has, the coronavirus
#
# # 1 3 1   # 2 2 2
# def wordweight(text):
#     text = text.lower()
#     text = text.split()
#     wordweightdict = {}
#     for i in text:
#         i = i.replace('.', '')
#         i = i.replace(',', '')
#         i = i.replace('!', '')
#         i = i.replace('?', '')
#         if i in wordweightdict:
#             wordweightdict[i] += 1
#         else:
#             wordweightdict[i] = 1
#     return wordweightdict
#
# def returnWeight(word, wordweightdict):
#     if ' ' in word:
#         word = word.split()
#         highesti = 0
#         for j in word:
#             i = wordweightdict[j]
#             if i == 1:
#                 i = (1)
#             if i == 2 or i == 3:
#                 i = (0.9)
#             if i in [4, 5, 6]:
#                 i = (0.75)
#             if i in [7, 8, 9, 10]:
#                 i = (0.5)
#             if i > 10:
#                 i = (3/i)
#             if i > highesti:
#                 highesti = i
#         return highesti
#     else:
#         i = wordweightdict[word]
#         if i == 1:
#             i = (1)
#         if i == 2 or i == 3:
#             i = (0.9)
#         if i in [4, 5, 6]:
#             i = (0.75)
#         if i in [7, 8, 9, 10]:
#             i = (0.5)
#         if i > 10:
#             i = (3 / i)
#         return i
#
# p = returnWeight('the war', wordweight('the war was not very cool. in fact, the war was not cool at all. the war. the war'))
# print(wordweight('the war was not very cool. in fact, the war was not cool at all. the war. the war'))
# print(p)

def matchingAlg2(a, b):
    a.lower()
    b.lower()
    return max(matchingSubAlg(a, b), matchingSubAlg(b, a))
def matchingSubAlg(a, b):
    a = simplify(a)
    b = simplify(b)
    print(a,b)
    if len(b) <= 1:
        if a == b:
            return 1
        return 0
    for i in createSubString(a):
        if i == b:
            return(len(i)/len(a))
    return 0

def simplify(a):
    if len(a.split()) > 1:
        tempa = nlp(a)
        newa = []
        for tok in tempa:
            if tok.dep_ != 'compound' and tok.dep_ != 'det':
                newa.append(tok)
    else:
        return a
    a = ''
    for i in newa:
        i = str(i)
        a = a + i
    a.replace(' ', '')
    return a
#
# def countOcc(a,b):
#     #a is string b is char:
#     counter = 0
#     for i in a:
#         if a == b:
#             counter += 1
#     return counter

def createSubString(a):
    a.replace(' ','')
    substrings = []
    for i in range(len(a)):
        substrings.append(a[i:])
    return substrings



#cornercase 3: tuciko nuioioae and uioioae
#
# def matchingAlg(a, b):
#     #returnsnumericvalue
#     a.lower()
#     b.lower()
#     return max(matchingSubAlg(a,b), matchingSubAlg(b,a))
#
# def matchingSubAlg(a,b):
#     # tempnewa = []
#     # if len(a.split()) > 1:
#     #     tempa = nlp(a)
#     #     for i in tempa:
#     #         if i.dep_ != 'compound':
#     #             tempnewa.append(i)
#     # newa = ''
#     # for i in tempnewa:
#     #     i = str(i)
#     #     newa = newa + i
#     a = a.replace(' ','')
#     b = b.replace(' ', '')
#     if len(b) <= 1:
#         if a == b:
#             return 1
#         return 0
#     stopindex = len(b) - 1
#     abcharmatch = []
#     counter = 0
#     pendingindex = 0
#     for i in a:
#         if counter >= 1:
#             pendingindex += 1
#             if pendingindex == stopindex:
#                 abcharmatch.append(counter)
#                 counter = 0
#                 pendingindex = 0
#             if i == b[pendingindex]:
#                 counter += 1
#             else:
#                 abcharmatch.append(counter)
#                 counter = 0
#                 pendingindex = 0
#         elif i in b:
#             counter += 1
#             pendingindex = b.find(i)
#             if pendingindex == stopindex:
#                 pendingindex = 0
#         else:
#             abcharmatch.append(counter)
#             counter = 0
#             pendingindex = 0
#     abcharmatch.append(counter)
#     highestabmatch = 0
#     for i in abcharmatch:
#         if i/len(a) > highestabmatch:
#             highestabmatch = i/len(a)
#     #checks compound (president obama) - (obama)
#     # checka = newa.replace(' ', '')
#     # if checka != a:
#     #     if matchingAlg(newa, b) > highestabmatch:
#     #         return matchingAlg(newa, b)
#     return highestabmatch
def matchingAlg(a, b):
    a.lower()
    b.lower()
    return max(matchingSubAlg(a, b), matchingSubAlg(b, a))
def matchingSubAlg(a, b):
    a = simplify(a)
    b = simplify(b)
    if len(b) <= 1:
        if a == b:
            return 1
        return 0
    for i in createSubString(a):
        print(i)
        if i == b:
            return(len(i)/len(a))
    return 0

def simplify(a):
    if len(a.split()) > 1:
        tempa = nlp(a)
        newa = []
        for token in tempa:
            if token.dep_ != 'nummod' and token.dep_ != 'advmod':
                newa.append(token)
    else:
        return a
    a = ''
    for i in newa:
        i = str(i)
        a = a + i
    a.replace(' ', '')
    return a

def createSubString(a):
    a.replace(' ','')
    substrings = []
    for i in range(len(a)):
        substrings.append(a[i:])
        substrings.append(a[:i])
    return substrings
#correct Matches:

# 'about 21 percent', 'tested', 'coronavirus antibodies'] ['what percent', 'has', 'the coronavirus']
# Question 2 has No Question SVO
#'who', 'is', 'new york city top official'] ['dr. demetre c. daskalakis', 'wrote', 'an email alert']

#['president obama', 'accepted', 'the nobel peace prize']['obama', 'receive', 'the nobel peace prize']
#['obama', 'justify', 'the wars'] ['war', 'justified', 'self-defense']
#['justifiable', 'according', 'obama'] ['war', 'justified', 'self-defense']

def questionAnalysis(questiondoc):
    svopairs = []
    possiblepairs = []
    for tok in questiondoc:
       print(tok, ' -> ', tok.dep_, ' -> ',tok.pos_)
       if (tok.dep_ == 'nsubj' or tok.dep_ == 'nsubjpass') and len(possiblepairs) == 0:
           possiblepairs.append(tok.text)
       if (tok.pos_ == 'VERB' or tok.pos_ == 'AUX' or tok.pos_ == 'AUXPASS') and len(possiblepairs) == 1:
           possiblepairs.append(tok.text)
       if (tok.dep_ == 'dobj' or tok.dep_ == 'pobj' or tok.dep_ == 'attr' or tok.dep_ == 'acomp') and len(
               possiblepairs) == 2:
           possiblepairs.append(tok.text)
       if len(possiblepairs) == 3:
           svopairs.append(possiblepairs)
           possiblepairs = []
    possiblepairs = []
    for tok in questiondoc:
       if (tok.dep_ == 'nsubj' or tok.dep_ == 'nsubjpass') and len(possiblepairs) == 2:
           possiblepairs.append(tok.text)
       if (tok.pos_ == 'VERB' or tok.pos_ == 'AUX' or tok.pos_ == 'AUXPASS') and len(possiblepairs) == 1:
           possiblepairs.append(tok.text)
       if (tok.dep_ == 'dobj' or tok.dep_ == 'pobj' or tok.dep_ == 'attr' or tok.dep_ == 'acomp') and len(
               possiblepairs) == 0:
           possiblepairs.append(tok.text)
       if len(possiblepairs) == 3:
           svopairs.append(possiblepairs)
           possiblepairs = []
    return svopairs
questionDoc = nlp('What kind of testing does New York City use?')
questionAnalysis(questionDoc)