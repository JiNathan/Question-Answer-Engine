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
text2 = 'President Obama accepted the Nobel Peace Prize during a ceremony Thursday in Norway, acknowledging the paradox of receiving the award as the US is embroiled in two wars, while maintaining that instruments of war have a role in preserving peace. In his acceptance speech, Obama told Nobel Committee members and guests in Oslo that achieving peace must begin with the recognition that the use of force is sometimes morally justified. Make no mistake: Evil does exist in the world. A nonviolent movement could not have halted Hitlers armies. Negotiations cannot convince al-Qaidas leaders to lay down their arms,"he told the crowd. It was just nine days ago that Obama announced he is sending an additional 30,000 U.S. troops to Afghanistan in an effort to step up training of Afghan security forces and root out insurgents operating on the border with Pakistan.'
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
    #checks substrings as well
    a = a.lower()
    b = b.lower()
    if a == b:
        return True
    else:
        if a in b or b in a:
            return True
    return False

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
    print(svopairs)
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

def giveAnswerTwo(svo_list, questiondoc):
    questionsvo = questionAnalysis(questiondoc)
    matches = {}
    for i in svo_list:
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
                    matchrating += 1
                    flaga = False
                if contains(i[1], p) and flagb:
                    matchrating += 1
                    flagb = False
                if contains(i[2], p) and flagc:
                    matchrating += 1
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

def returnresult(text, question):
    question = question.lower()
    text = text.lower()
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
    for k in sen_map:
       h = giveAnswerTwo(sen_map[k], questiondoc)
       if h >= highest_score:
           highest_score = h
           highest_key = k

#Printing Out Data:
    print(sen_map)
    print('Sentence Score: ', highest_score,'Sentence Key: ', highest_key)
    print(sentences)
    print(question_svo)
    if highest_score == 0:
        return 'There was no match'
    else:
        return sentences[highest_key]

# print(returnresult(text2, question))
