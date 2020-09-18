#Imports
import re
import string
import nltk
from nltk.stem import WordNetLemmatizer
import spacy
import pandas as pd
import spacyMatching
import numpy as np
import math

from tqdm import tqdm
from spacy.pipeline import merge_entities
from spacy.matcher import Matcher
from spacy.tokens import Span
from spacy import displacy
import gensim.downloader as api
import en_core_web_sm
#hello
class Engine:
    def __init__(self):
        self.wv = api.load('word2vec-google-news-300')
        self.nlp = en_core_web_sm.load()

        # merge_nps = self.nlp.create_pipe("merge_noun_chunks")
        # merge_ents = self.nlp.create_pipe("merge_entities")
        # merge_subtok = self.nlp.create_pipe("merge_subtokens")
        # self.nlp.add_pipe(merge_nps)
        # self.nlp.add_pipe(merge_ents)
        # self.nlp.add_pipe(merge_subtok)

    # def remove_dot_acronym(self,s):
    #     m = re.search('(.*?)(([a-zA-Z]\.){2,})(.*)', s)
    #     if m:
    #         replacement = ''.join(m.group(2).split('.'))
    #         s = m.group(1) + replacement + m.group(4)
    #         return s
    #     else:
    #         return m
    #
    # def remove_abbrev(self,text):
    #     temp = self.remove_dot_acronym(text)
    #     while temp != None:
    #         text = temp
    #
    #         temp = self.remove_dot_acronym(text)
    #
    #     text = re.sub(r"(?<= [.(a-zA-Z)]{3})\.(?!=(\n))", ' ', text)
    #     text = re.sub(r"(?<= [a-zA-Z]{2})\.(?!=(\n))", ' ', text)
    #
    #     return text

    # def matching_sentence(self, sentence_list, sentence, index_sentence):
    #     possible_sentence=''
    #     current_pos = 0
    #     temp_pos = 0
    #     for i in range (index_sentence, len(sentence_list)):
    #         for j in range (len(sentence_list[i])):
    #             if sentence[0] == sentence_list[i][j]:
    #                 temp_pos += 1
    #
    #             else:
    #                 break
    #
    #         if temp_pos != current_pos:
    #             possible_sentence = sentence_list[i]
    #             temp_pos+= 1
    #             current_pos = temp_pos
    #         if current_pos == len(sentence):
    #             break
    #
    #     return possible_sentence

    def returnresult(self,text, question, numofanswers):
        #cleans up text
        # sentence_list = text.split('.')
        # question = question.lower()
        # text = text.lower()
        #tokenizes text + cleans up text
        # questiondoc= self.nlp(question)


        # text = self.remove_abbrev(text)

        doc = self.nlp(text)
        #splits text into setences
        sentences = [sent.string.strip() for sent in doc.sents if len(sent) > 2]
        # print(sentences)
        #get scores for each sentences
        scores = {}
        for sentence in sentences:
            scores[sentence] = spacyMatching.matching(self.nlp(question), self.nlp(sentence), self.wv)
        #sort scores
        sort_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        #check for no match
        # if sort_scores[0][1] <= 0.5 or math.isnan(sort_scores[0][1]):
        if math.isnan(sort_scores[0][1]):
            return scores, ['there was no match']
        else:
            result_list = []
            for i in range(numofanswers):
                # sentence_index = sentences.index(sort_scores[i][0])
                result_list.append(sort_scores[i][0])

            # print('1st: ', sort_scores[0])
            # print('2nd: ', sort_scores[1])
            # print('3rd: ', sort_scores[2])
        #debugging/testing return
        return scores, result_list
        # return returnlist
        # returnfriendly = ''
        # for i in range(numofanswers):
        #     returnfriendly += str(i+1) + ': ' + sort_scores[i][0] + '\n'
        # return returnfriendly



