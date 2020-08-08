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
import numpy

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
subjects = ("nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl")
objects = ("dobj", "dative", "attr", "oprd", "pobj", "acomp")
def findSVOind(doc):
    subjects = ("nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl")
    objects = ("dobj", "dative", "attr", "oprd", "pobj", "acomp")
    verbs = ("VERB", "AUX", "AUXPASS")
    sub = {}
    verb = {}
    obj = {}
    counter = -1
    for tok in doc:
        counter += 1
        if tok.dep_ in subjects:
            sub[tok.text] = counter
        if tok.dep_ in objects:
            obj[tok.text] = counter
        if tok.pos_ in verbs:
            verb[tok.text] = counter
    return [sub, verb, obj, counter]

def findSVOinpoints(point1, point2, sub, verb, obj):
    pairs = []
    print(point1, point2, sub,verb, obj)
    for i in range(point1, point2):
        print(i)
        possiblepair = [list(sub.keys())[point1]]
        if i in verb.values():
            print(list(verb.keys())[list(verb.values()).index(i)])
            possiblepair.append(list(verb.keys())[list(verb.values()).index(i)])
            for j in range(i, point2):
                print(j, 'j')
                if j in obj.values():
                    print(list(obj.keys())[list(obj.values()).index(j)])
                    possiblepair.append(list(obj.keys())[list(obj.values()).index(j)])
                if len(possiblepair) == 3:
                    if possiblepair not in pairs:
                        print(possiblepair)
                        copypossible = possiblepair.copy()
                        pairs.append(copypossible)
                        possiblepair.pop(2)
    print(pairs)
    return pairs

def svoMatcher(doc):
    temp = findSVOind(doc)
    sub, verb, obj, length = temp[0], temp[1], temp[2], temp[3]
    svopairs = []
    print(sub)
    flag = False
    #find first two points
    if len(sub) == 0:
        #return something here
        return 0
    point1 = list(sub.values())[0]
    if len(sub) == 1:
        point2 = length + 1
        flag = True
    else:
        point2 = list(sub.values())[1]
    for i in sub:
        if i != point1:
            if i == point2 or flag:
                print('here')
                flag = False
                #run procedure for 2 given points
                if len(findSVOinpoints(point1, point2, sub,verb,obj)) > 0:
                    for j in findSVOinpoints(point1, point2, sub,verb,obj):
                        svopairs.append(j)
            else:
                #run procedure for adjusting point 2 to point 1 and making a new point 2
                temp = point2
                point1 = temp
                point2 = sub[i]
                if len(findSVOinpoints(point1, point2, sub,verb,obj)) > 0:
                    for j in findSVOinpoints(point1, point2, sub,verb,obj):
                        svopairs.append(j)
    return svopairs
#I traveled and walked around the world (SVVO)
#I traveled to London and Avoided Paris (SVOVO)
# (SVOO)



# Program to measure the similarity between
# two sentences using cosine similarity.
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# X = input("Enter first string: ").lower()
# Y = input("Enter second string: ").lower()
X = "Flag"
Y = "Banner"
def match(X, Y):
    # tokenization
    X_list = word_tokenize(X)
    Y_list = word_tokenize(Y)

    # sw contains the list of stopwords
    sw = stopwords.words('english')
    l1 = [];
    l2 = []

    # remove stop words from the string
    X_set = {w for w in X_list if not w in sw}
    Y_set = {w for w in Y_list if not w in sw}

    # form a set containing keywords of both strings
    rvector = X_set.union(Y_set)
    for w in rvector:
        if w in X_set:
            l1.append(1)  # create a vector
        else:
            l1.append(0)
        if w in Y_set:
            l2.append(1)
        else:
            l2.append(0)
    c = 0

    # cosine formula
    for i in range(len(rvector)):
        c += l1[i] * l2[i]
    cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
    return("similarity: ", cosine)
#correctanswer: 0.1825741
import gensim
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec
import gensim.downloader as api
wv = api.load('word2vec-google-news-300')

def avg_sentence_vector(words, model, num_features, index2word_set):
    #function to average all words vectors in a given paragraph
    featureVec = numpy.zeros((num_features,), dtype="float32")
    nwords = 0

    for word in words:
        if word in index2word_set:
            nwords = nwords+1
            featureVec = numpy.add(featureVec, model[word])

    if nwords>0:
        featureVec = numpy.divide(featureVec, nwords)
    return featureVec

# print(model2.n_similarity('president obama', 'obama'))



# #get average vector for sentence 1
sentence_1 = "this is sentence number one"
sentence_1_avg_vector = avg_sentence_vector(sentence_1.split(), model=wv, num_features=100, index2word_set = wv.index2word)
# #get average vector for sentence 2
sentence_2 = "this is sentence number two"
sentence_2_avg_vector = avg_sentence_vector(sentence_2.split(), model=wv, num_features=100, index2word_set = wv.index2word)

sen1_sen2_similarity =  cosine_similarity(sentence_1_avg_vector,sentence_2_avg_vector)
print(sen1_sen2_similarity)


def questionWithoutSub(questiondoc):
    pass
# def giveAnswer(svo_list, questiondoc):
#    questionsvo = questionAnalysis(questiondoc)
#    matches = {}
#    for i in svo_list:
#        matchrating = 0
#        possiblematch = []
#        for j in questionsvo:
#            if j[0] == i[0]:
#                matchrating += 1
#                if j[1] == i[1] or j[2] == i[2]:
#                    matchrating += 1
#                    if j[1] == i[1] and j[2] == i[2]:
#                        matchrating += 1
#                        possiblematch.append(j)
#                    else:
#                        possiblematch.append(j)
#                else:
#                    possiblematch.append(j)
#        matches[matchrating] = possiblematch
#    highestmatch = 0
#    for k in matches:
#        if k >= highestmatch:
#            highestmatch = k
#    return highestmatch

# First Version of SVO Matcher
#
# def svoMatcher(doc):
#     svopairs = []
#     possiblepairs = [[],[]]
#     pendingpairs = 1
#     for tok in doc:
#         if findnextitem(tok, possiblepairs, 0) != 'none':
#             possiblepairs[0].append(findnextitem(tok, possiblepairs, 0))
#         else:
#             if findnextitem(tok, possiblepairs, 1) != 'none':
#                 possiblepairs[1].append(findnextitem(tok, possiblepairs, 1))
#         if len(possiblepairs[0]) == 3:
#             svopairs.append(possiblepairs[0])
#             if findnextitem(tok, possiblepairs, 0) != 'none':
#                 temp = possiblepairs[0]
#                 temp.remove(temp[0][2])
#                 temp[0].append(findnextitem(tok, temp, 0))
#                 if len(temp[0]) == 3:
#                     svopairs.append(temp)
#             possiblepairs[0] = []
#             pendingpairs = pending(possiblepairs)
#         elif len(possiblepairs[1]) == 3:
#            svopairs.append(possiblepairs[1])
#            if findnextitem(tok, possiblepairs, 0) != 'none':
#                temp = possiblepairs[1]
#                temp.remove(temp[1][2])
#                temp[1].append(findnextitem(tok, temp, 1))
#                if len(temp[1]) == 3:
#                    svopairs.append(temp)
#            possiblepairs[1] =[]
#            pendingpairs = pending(possiblepairs)
#     return svopairs