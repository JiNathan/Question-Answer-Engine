import re
import string
import nltk
from nltk.stem import WordNetLemmatizer
import spacy
import pandas as pd
import numpy as np
import math
from tqdm import tqdm
from spacy.pipeline import merge_entities
from spacy.matcher import Matcher
from spacy.tokens import Span
from spacy import displacy
lemmatizer = WordNetLemmatizer()
nltk.download('punkt')
pd.set_option('display.max_colwidth', 200)
nlp = spacy.load("en_core_web_sm")
merge_nps = nlp.create_pipe("merge_noun_chunks")
merge_ents = nlp.create_pipe("merge_entities")
merge_subtok = nlp.create_pipe("merge_subtokens")
nlp.add_pipe(merge_nps)
nlp.add_pipe(merge_ents)
nlp.add_pipe(merge_subtok)
# doc = nlp(text2)
quotetext = """President Obama accepted the Nobel Peace Prize during a ceremony Thursday in Norway, acknowledging the paradox of receiving the award as the U.S. is embroiled in two wars, while maintaining that instruments of war have a role in preserving peace. In his acceptance speech, Obama told Nobel Committee members and guests in Oslo that achieving peace must begin with the recognition that the use of force is sometimes morally justified. Make no mistake: Evil does exist in the world. A nonviolent movement could not have halted Hitler's armies. Negotiations cannot convince al-Qaida's leaders to lay down their arms," he told the crowd. It was just nine days ago that Obama announced he is sending an additional 30,000 U.S. troops to Afghanistan in an effort to step up training of Afghan security forces and root out insurgents operating on the border with Pakistan."""
question = 'Where did obama accepted the Nobel Peace Prize'
# questiondoc = nlp(question)
# nlp.add_pipe(merge_entities)
# print token, dependency, POS tag
# for tok in doc:
#   print(tok.text, "-->",tok.dep_,"-->", tok.pos_)


def pending(possiblepairs):
    if len(possiblepairs[0]) > 0 and len(possiblepairs[1]) > 0:
        return 2
    elif len(possiblepairs[0]) > 0 or len(possiblepairs[1]) > 0:
        return 1
    else:
        return 0

def findnextitem(tok, possiblepairs, a):
    if (tok.dep_ == 'nsubj' or tok.dep_ == 'nsubjpass') and len(possiblepairs[a]) == 0:
        return(tok.text)
    if (tok.pos_ == 'VERB' or tok.pos_ == 'AUX') and len(possiblepairs[a]) == 1 and tok.dep_ != 'aux' and tok.dep_ !='auxpass':
        return(tok.text)
    if (tok.dep_ == 'dobj' or tok.dep_ == 'pobj' or tok.dep_ == 'attr' or tok.dep_ == 'acomp') and len(
            possiblepairs[a]) == 2:
        return(tok.text)
    return 'none'
def contains(a, b):
    #returns boolean value
    a = a.lower()
    b = b.lower()
    if a == b:
        return True
    if a in b or b in a:
        return True
    words = a.split()
    for i in (b.split()):
        words.append(i)
    wordtest = set(words)
    if len(wordtest) != len(words):
        return True
    return False

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
        if i == b:
            return(len(i)/len(a))
    return 0

def simplify(a):
    if len(a.split()) > 1:
        tempa = nlp(a)
        newa = []
        for token in tempa:
            if token.dep_ != 'det' and token.dep_ != 'nummod' and token.dep_ != 'advmod':
                newa.append(token)
    else:
        return a
    a = ''
    for i in newa:
        i = str(i)
        a = a + i
    a.replace(' ', '')
    return a

print(simplify('president obama'))

def createSubString(a):
    a.replace(' ','')
    substrings = []
    for i in range(len(a)):
        substrings.append(a[i:])
        substrings.append(a[:i])
    return substrings




def svoMatcher(doc):
    svopairs = []
    possiblepairs = [[],[]]
    pendingpairs = 1
    for tok in doc:
        if findnextitem(tok, possiblepairs, 0) != 'none':
            possiblepairs[0].append(findnextitem(tok, possiblepairs, 0))
        else:
            if findnextitem(tok, possiblepairs, 1) != 'none':
                possiblepairs[1].append(findnextitem(tok, possiblepairs, 1))
        if len(possiblepairs[0]) == 3:
            svopairs.append(possiblepairs[0])
            possiblepairs[0] = []
            pendingpairs = pending(possiblepairs)
        elif len(possiblepairs[1]) == 3:
           svopairs.append(possiblepairs[1])
           possiblepairs[1] =[]
           pendingpairs = pending(possiblepairs)
    return svopairs

def questionAnalysis(questiondoc):
    svopairs = []
    possiblepairs = []
    for tok in questiondoc:
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

def giveAnswerTwo(svo_list, questiondoc, text):
    wordweightdict = wordweight(text)

    questionsvo = questionAnalysis(questiondoc)
    matches = {}
    for i in svo_list:
        temp0 = i[0]
        temp1 = i[1]
        temp2 = i[2]
        i[0] = WordNetLemmatizer().lemmatize(i[0],'n')
        i[1] = WordNetLemmatizer().lemmatize(i[1],'v')
        i[2] = WordNetLemmatizer().lemmatize(i[2],'n')
        matchrating = 0
        possiblematch = []
        for j in questionsvo:
            j[0] = WordNetLemmatizer().lemmatize(j[0], 'n')
            j[1] = WordNetLemmatizer().lemmatize(j[1], 'v')
            j[2] = WordNetLemmatizer().lemmatize(j[2], 'n')
            flaga = True
            flagb = True
            flagc = True
            for p in j:
                if contains(i[0], p) and flaga:
                    matchrating += (returnWeight(temp0, wordweightdict) + matchingAlg(temp0, p) * 2)/3
                    flaga = False
                if contains(i[1], p) and flagb:
                    matchrating += (returnWeight(temp1, wordweightdict) + matchingAlg(temp1, p)*2)/3
                    flagb = False
                if contains(i[2], p) and flagc:
                    matchrating += (returnWeight(temp2, wordweightdict) + matchingAlg(temp2, p)*2)/3
                    flagc = False
                possiblematch.append(j)
        matches[matchrating] = possiblematch
    highestmatch = 0
    for k in matches:
        if k >= highestmatch:
            highestmatch = k
    return highestmatch


# def giveAnswerWithMap(doc_map, questiondoc):
#    docsvo = svoMatcher(doc)
#    questionsvo = questionAnalysis(questiondoc)
#    matches = {}
#    for i in docsvo:
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
#        if k > highestmatch:
#            highestmatch = k
#    return highestmatch
   # return (matches[highestmatch], highestmatch)

#TieBreaker
def TieBreak():
    pass


#input
# text = ''
# question = ''
# # doc = nlp(text)
# questiondoc = nlp(question)
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
        average = []
        for j in word:
            if j not in wordweightdict:
                i = 1
            else:
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
            if len(word) > 1:
                average.append(i)
            else:
                return i
        lowest = 0
        sum=0
        for i in average:
            if i < lowest:
                lowest = i
            sum += i
        sum -= lowest
        return (sum/(len(average) - 1))


    else:
        i = wordweightdict[word]
        if i == 1:
            i = (1)
        if i == 2 or i == 3:
            i = (0.75)
        if i in [4, 5, 6]:
            i = (0.6)
        if i in [7, 8, 9, 10]:
            i = (0.5)
        if i > 10:
            i = (3 / i)
        return i

def displayResults(highest_key, highest_score, sen_map, sentences):
    print('Sentence key: ',highest_key,' Sentence score: ', highest_score)
    print(sen_map[highest_key])
    print(sen_map)
    print('------------------------------------')

def returnresult(text, question, numofanswers):
    question = question.lower()
    text = text.lower()
    wordweightdict = wordweight(text)
    questiondoc = nlp(question)
    sen_map = {}
    sentences = nltk.tokenize.sent_tokenize(text)
    for i in range(len(sentences)):
       tokened = nlp(sentences[i])
       sen_map[i] = svoMatcher(tokened)
    question_svo = questionAnalysis(questiondoc)
    highest_score = 0
    highest_key = -1
    svo_average = 0
    scores = {}
    for k in sen_map:
       h = giveAnswerTwo(sen_map[k], questiondoc, text)
       scores[k] = h
       if h >= highest_score:
           highest_score = h
           highest_key = k
    displayResults(highest_key, highest_score, sen_map, sentences)
    print(question_svo)
    sort_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    if highest_score == 0:
        return 'There was no match'
    else:
        returnlist = []
        for i in range(numofanswers):
            returnlist.append(sentences[sort_scores[i][0]])
        return returnlist

    print('1st: ', sort_scores[0], sentences[sort_scores[1][0]])
    print('2nd: ', sort_scores[1], sentences[sort_scores[1][0]])
    print('3rd: ', sort_scores[2], sentences[sort_scores[2][0]])

# print(returnresult(text2, question))
