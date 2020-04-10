import re
import string
import nltk
import spacy
import pandas as pd
import numpy as np
import math
from tqdm import tqdm
from spacy.pipeline import merge_entities
from spacy.matcher import Matcher
from spacy.tokens import Span
from spacy import displacy
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

def svoMatcher(doc):
    svopairs = []
    possiblepairs = []
    for tok in doc:
       if (tok.dep_ == 'nsubj' or tok.dep_ == 'nsubjpass') and len(possiblepairs) == 0:
           possiblepairs.append(tok.text)
       if (tok.pos_ == 'VERB' or tok.pos_ == 'AUX' or tok.pos_ == 'AUXPASS') and len(possiblepairs) == 1:
           possiblepairs.append(tok.text)
       if (tok.dep_ == 'dobj' or tok.dep_ == 'pobj' or tok.dep_ == 'attr' or tok.dep_ == 'acomp') and len(possiblepairs) == 2:
           possiblepairs.append(tok.text)
       if len(possiblepairs) == 3:
           svopairs.append(possiblepairs)
           possiblepairs =[]
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

def giveAnswer(svo_list, questiondoc):
   questionsvo = questionAnalysis(questiondoc)
   matches = {}
   for i in svo_list:
       matchrating = 0
       possiblematch = []
       for j in questionsvo:
           if j[0] == i[0]:
               matchrating += 1
               if j[1] == i[1] or j[2] == i[2]:
                   matchrating += 1
                   if j[1] == i[1] and j[2] == i[2]:
                       matchrating += 1
                       possiblematch.append(j)
                   else:
                       possiblematch.append(j)
               else:
                   possiblematch.append(j)
       matches[matchrating] = possiblematch
   highestmatch = 0
   for k in matches:
       if k >= highestmatch:
           highestmatch = k
   return highestmatch

def giveAnswerTwo(svo_list, questiondoc):
    questionsvo = questionAnalysis(questiondoc)
    matches = {}
    for i in svo_list:
        matchrating = 0
        possiblematch = []
        for j in questionsvo:
            if i[0] in j:
                matchrating += 1
            if i[1] in j:
                matchrating += 1
            if i[2] in j:
                matchrating += 1
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

#input
# text = ''
# question = ''
# # doc = nlp(text)
# questiondoc = nlp(question)
def returnresult(text, question):
    questiondoc = nlp(question)
    sen_map = {}
    sentences = nltk.tokenize.sent_tokenize(text)
    for i in range(len(sentences)):
       tokened = nlp(sentences[i])
       sen_map[i] = svoMatcher(tokened)
    question_svo = questionAnalysis(questiondoc)
    highest_score = 0
    highest_key = -1
    for k in sen_map:
       h = giveAnswer(sen_map[k], questiondoc)
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
