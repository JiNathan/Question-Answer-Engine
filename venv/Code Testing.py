import nltk
import math
import spacy
nlp = spacy.load('en_core_web_sm')
from nltk.corpus import wordnet as wn
merge_nps = nlp.create_pipe("merge_noun_chunks")
merge_ents = nlp.create_pipe("merge_entities")
merge_subtok = nlp.create_pipe("merge_subtokens")
nlp.add_pipe(merge_nps)
nlp.add_pipe(merge_ents)
nlp.add_pipe(merge_subtok)
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()


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


#correct Matches:

# 'about 21 percent', 'tested', 'coronavirus antibodies'] ['what percent', 'has', 'the coronavirus']
# Question 2 has No Question SVO
#'who', 'is', 'new york city top official'] ['dr. demetre c. daskalakis', 'wrote', 'an email alert']

#['president obama', 'accepted', 'the nobel peace prize']['obama', 'receive', 'the nobel peace prize']
#['obama', 'justify', 'the wars'] ['war', 'justified', 'self-defense']
#['justifiable', 'according', 'obama'] ['war', 'justified', 'self-defense']
#
# def questionAnalysis(questiondoc):
#     subject = ['nsubj','nsubjpass' ]
#     verb = ['VERB', 'AUX', 'AUXPASS']
#     object= ['dobj', 'pobj', 'attr', 'acomp']
#     svopairs = []
#     pending = {}
#     numpending = 0
#     for tok in questiondoc:
#         if tok.dep_ in subject:
#             flag = True
#             for i in range(numpending):
#                 if len(pending) == 0:
#                     break
#                 if flag:
#                     if len(pending[i]) == 2:
#                         flag = False
#                         pending[i].append(tok.text)
#         if tok.pos_ in verb:
#             flag = True
#             for i in range(numpending):
#                 if len(pending) == 0:
#                     break
#                 if flag:
#                     if len(pending[i]) == 1:
#                         flag = False
#                         pending[i].append(tok.text)
#         if tok.dep_ in object:
#             pending[numpending] = [tok.text]
#             numpending += 1
#         remove = ''
#         for i in pending:
#             for i in range(numpending):
#                 if len(pending[i]) == 3:
#                     svopairs.append(pending[i])
#                     numpending -= 1
#                     remove = i
#         if remove != '':
#             pending.pop(remove)
#         remove = ''
#     pending = {}
#     for tok in questiondoc:
#         if tok.dep_ in subject:
#             pending[numpending] = [tok.text]
#             numpending += 1
#         if tok.pos_ in verb:
#             flag = True
#             for i in range(numpending):
#                 if len(pending) == 0:
#                     break
#                 if flag:
#                     if len(pending[i]) == 1:
#                         flag = False
#                         pending[i].append(tok.text)
#         if tok.dep_ in object:
#             flag = True
#             for i in range(numpending):
#                 if len(pending) == 0:
#                     break
#                 if flag:
#                     if len(pending[i]) == 2:
#                         flag = False
#                         pending[i].append(tok.text)
#         remove = ''
#         for i in pending:
#             for i in range(numpending):
#                 if len(pending[i]) == 3:
#                     svopairs.append(pending[i])
#                     numpending -= 1
#                     remove = i
#         if remove != '':
#             pending.pop(remove)
#         remove = ''
#     return svopairs
# questionDoc = nlp('What kind of testing does New York City use?')
# questionAnalysis(questionDoc)


# def matchingAlg(a, b):
#     a.lower()
#     b.lower()
#     return max(matchingSubAlg(a, b), matchingSubAlg(b, a))
# def matchingSubAlg(a, b):
#     a = simplify(a)
#     b = simplify(b)
#     if len(b) <= 1:
#         if a == b:
#             return 1
#         return 0
#     if b in a:
#         return len(b)/len(a)
#     for i in createSubString(a):
#         if i == b:
#             return(len(i)/len(a))
#     return 0
#
# def simplify(a):
#     if len(a.split()) > 1:
#         useless = ['a', 'the', 'an']
#         newa = []
#         for i in (a.split()):
#             if i not in useless:
#                 newa.append(i)
#         returnvalue = ''
#         for i in newa:
#             returnvalue += i
#         return returnvalue
#     else:
#         return a
#
# def createSubString(a):
#     a.replace(' ','')
#     substrings = []
#     for i in range(len(a)):
#         substrings.append(a[i:])
#         substrings.append(a[:i])
#     return substrings
#
#
# def spacyMatching(a, b):
#     words = a + ' ' + b
#     tokens = nlp(words)
#     token1, token2= tokens[0], tokens[1]
#     return token1.similarity(token2)
#
# print(spacyMatching('the wars', 'war'))
# print(matchingAlg('the wars', 'war'))


# 'about 21 percent', 'tested', 'coronavirus antibodies'] ['what percent', 'has', 'the coronavirus']
# Question 2 has No Question SVO
#'who', 'is', 'new york city top official'] ['dr. demetre c. daskalakis', 'wrote', 'an email alert']

#['president obama', 'accepted', 'the nobel peace prize']['obama', 'receive', 'the nobel peace prize']
#['obama', 'justify', 'the wars'] ['war', 'justified', 'self-defense']
#['justifiable', 'according', 'obama'] ['war', 'justified', 'self-defense']
text = 'What kind of testing does New York City use?'
doc = nlp(text)
for tok in doc.noun_chunks:
    print(tok.text, tok.root.pos_, tok.root.dep_, ' ------------- ', tok.root.head.text)