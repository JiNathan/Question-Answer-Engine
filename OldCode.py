# nlp = en_core_web_sm.load()
#
# #initalization
# wv = api.load('word2vec-google-news-300')
# lemmatizer = WordNetLemmatizer()
# nltk.download('punkt')
# pd.set_option('display.max_colwidth', 200)
# # nlp = spacy.load("en_core_web_sm")
# merge_nps = nlp.create_pipe("merge_noun_chunks")
# merge_ents = nlp.create_pipe("merge_entities")
# merge_subtok = nlp.create_pipe("merge_subtokens")
# nlp.add_pipe(merge_nps)
# nlp.add_pipe(merge_ents)
# nlp.add_pipe(merge_subtok)
# # nlp.add_pipe(merge_entities)
# # print token, dependency, POS tag
# subjects = ("nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl")
# objects = ("dobj", "dative", "attr", "oprd", "pobj", "acomp")

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

#First Version of Return Result
# def returnresult(text, question, numofanswers):
#     question = question.lower()
#     text = text.lower()
#     # quotelesstext = text.replace('“', "").replace('”',"")
#     wordweightdict = wordweight(text)
#     questiondoc = nlp(question)
#     sen_map = {}
#     doc = nlp(text)
#     sentences = [sent.string.strip() for sent in doc.sents]
#     for i in range(len(sentences)):
#        # tokened = nlp(sentences[i])
#        sen_map[i] = svoMatcher(sentences[i])
#     question_svo = questionAnalysis(questiondoc, subjects, objects)
#     highest_score = 0
#     highest_key = -1
#     svo_average = 0
#     scores = {}
#     for k in sen_map:
#        h = giveAnswerTwo(sen_map[k], questiondoc, text)
#        scores[k] = h
#        if h >= highest_score:
#            highest_score = h
#            highest_key = k
#     displayResults(highest_key, highest_score, sen_map, sentences)
#     print(question_svo)
#     sort_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
#
#     if highest_score == 0:
#         return 'There was no match'
#     else:
#         returnlist = []
#         for i in range(numofanswers):
#             returnlist.append(sentences[sort_scores[i][0]])
#         print('1st: ', sort_scores[0], sentences[sort_scores[0][0]])
#         print('2nd: ', sort_scores[1], sentences[sort_scores[1][0]])
#         print('3rd: ', sort_scores[2], sentences[sort_scores[2][0]])
#         returnlist.append(sentences[sort_scores[i][0]])
#     return returnlist

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
#         average = []
#         for j in word:
#             if j not in wordweightdict:
#                 i = 1
#             else:
#                 i = wordweightdict[j]
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
#             if len(word) > 1:
#                 average.append(i)
#             else:
#                 return i
#         lowest = 0
#         sum=0
#         for i in average:
#             if i < lowest:
#                 lowest = i
#             sum += i
#         sum -= lowest
#         return (sum/(len(average) - 1))
#
#
#     else:
#         i = wordweightdict[word]
#         if i == 1:
#             i = (1)
#         if i == 2 or i == 3:
#             i = (0.75)
#         if i in [4, 5, 6]:
#             i = (0.6)
#         if i in [7, 8, 9, 10]:
#             i = (0.5)
#         if i > 10:
#             i = (3 / i)
#         return i
# def giveAnswerTwo(svo_list, questiondoc, text):
#     wordweightdict = wordweight(text)
#     questionsvo = questionAnalysis(questiondoc, subjects, objects)
#     matches = {}
#     for i in svo_list:
#         temp0 = i[0]
#         temp1 = i[1]
#         temp2 = i[2]
#         i[0] = WordNetLemmatizer().lemmatize(i[0],'n')
#         i[1] = WordNetLemmatizer().lemmatize(i[1],'v')
#         i[2] = WordNetLemmatizer().lemmatize(i[2],'n')
#         matchrating = 0
#         possiblematch = []
#         for j in questionsvo:
#             j[0] = WordNetLemmatizer().lemmatize(j[0], 'n')
#             j[1] = WordNetLemmatizer().lemmatize(j[1], 'v')
#             j[2] = WordNetLemmatizer().lemmatize(j[2], 'n')
#             flaga = True
#             flagb = True
#             flagc = True
#             for p in j:
#                 if contains(i[0], p) and flaga:
#                     matchrating += ((spacyMatching.matching(i[0], p, wv) * 2) + (returnWeight(temp0, wordweightdict)))/3
#                     flaga = False
#                 if contains(i[1], p) and flagb:
#                     matchrating += ((spacyMatching.matching(i[1], p, wv) * 2) + (returnWeight(temp1, wordweightdict)))/3
#                     flagb = False
#                 if contains(i[2], p) and flagc:
#                     matchrating += ((spacyMatching.matching(i[2], p, wv) * 2) + (returnWeight(temp2, wordweightdict)))/3
#                     flagc = False
#                 possiblematch.append(j)
#         matches[matchrating] = possiblematch
#     highestmatch = 0
#     for k in matches:
#         if k >= highestmatch:
#             highestmatch = k
#     return highestmatch
#
# def questionAnalysis(questiondoc, subjects, objects):
#     svopairs = []
#     possiblepairs = []
#     for tok in questiondoc:
#        if (tok.dep_ in subjects) and len(possiblepairs) == 0:
#            possiblepairs.append(tok.text)
#        if (tok.pos_ == 'VERB' or tok.pos_ == 'AUX' or tok.pos_ == 'AUXPASS') and len(possiblepairs) == 1:
#            possiblepairs.append(tok.text)
#        if (tok.dep_ in objects) and len(possiblepairs) == 2:
#            possiblepairs.append(tok.text)
#        if len(possiblepairs) == 3:
#            svopairs.append(possiblepairs)
#            possiblepairs = []
#     possiblepairs = []
#     for tok in questiondoc:
#        if (tok.dep_ == 'nsubj' or tok.dep_ == 'nsubjpass') and len(possiblepairs) == 2:
#            possiblepairs.append(tok.text)
#        if (tok.pos_ == 'VERB' or tok.pos_ == 'AUX' or tok.pos_ == 'AUXPASS') and len(possiblepairs) == 1:
#            possiblepairs.append(tok.text)
#        if (tok.dep_ == 'dobj' or tok.dep_ == 'pobj' or tok.dep_ == 'attr' or tok.dep_ == 'acomp') and len(
#                possiblepairs) == 0:
#            possiblepairs.append(tok.text)
#        if len(possiblepairs) == 3:
#            svopairs.append(possiblepairs)
#            possiblepairs = []
#     return svopairs
#
#
# def pending(possiblepairs):
#     if len(possiblepairs[0]) > 0 and len(possiblepairs[1]) > 0:
#         return 2
#     elif len(possiblepairs[0]) > 0 or len(possiblepairs[1]) > 0:
#         return 1
#     else:
#         return 0
#
# def findnextitem(tok, possiblepairs, a):
#     if (tok.dep_ == 'nsubj' or tok.dep_ == 'nsubjpass') and len(possiblepairs[a]) == 0:
#         return(tok.text)
#     if (tok.pos_ == 'VERB' or tok.pos_ == 'AUX') and len(possiblepairs[a]) == 1 and tok.dep_ != 'aux' and tok.dep_ !='auxpass':
#         return(tok.text)
#     if (tok.dep_ == 'dobj' or tok.dep_ == 'pobj' or tok.dep_ == 'attr' or tok.dep_ == 'acomp') and len(
#             possiblepairs[a]) == 2:
#         return(tok.text)
#     return 'none'
# def contains(a, b):
#     #returns boolean value
#     a = a.lower()
#     b = b.lower()
#     if a == b:
#         return True
#     if a in b or b in a:
#         return True
#     words = a.split()
#     for i in (b.split()):
#         words.append(i)
#     wordtest = set(words)
#     if len(wordtest) != len(words):
#         return True
#     return False
#
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
# def findSVOind(doc):
#     subjects = ("nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl")
#     objects = ("dobj", "dative", "attr", "oprd", "pobj", "acomp")
#     verbs = ("VERB", "AUX", "AUXPASS")
#     sub = {}
#     verb = {}
#     obj = {}
#     counter = -1
#     for tok in doc:
#         counter += 1
#         if tok.dep_ in subjects:
#             sub[tok.text] = counter
#         if tok.dep_ in objects:
#             obj[tok.text] = counter
#         if tok.pos_ in verbs:
#             verb[tok.text] = counter
#     return [sub, verb, obj, counter]
#
# def findSVOinpoints(point1, point2, sub, verb, obj):
#     pairs = []
#     for i in range(point1, point2):
#         possiblepair = [list(sub.keys())[list(sub.values()).index(point1)]]
#         if i in verb.values():
#             possiblepair.append(list(verb.keys())[list(verb.values()).index(i)])
#             for j in range(i, point2):
#                 if j in obj.values():
#                     possiblepair.append(list(obj.keys())[list(obj.values()).index(j)])
#                 if len(possiblepair) == 3:
#                     if possiblepair not in pairs:
#                         copypossible = possiblepair.copy()
#                         pairs.append(copypossible)
#                         possiblepair.pop(2)
#     return pairs
#
# def svoMatcher(doc):
#     doc = nlp(doc)
#     temp = findSVOind(doc)
#     sub, verb, obj, length = temp[0], temp[1], temp[2], temp[3]
#     svopairs = []
#     flag = False
#     #find first two points
#     if len(sub) == 0:
#         #return something here
#         return []
#     point1 = list(sub.values())[0]
#     if len(sub) == 1:
#         point2 = length + 1
#         flag = True
#     else:
#         point2 = list(sub.values())[1]
#     for i in sub:
#         if i != point1:
#             if i == point2 or flag:
#                 flag = False
#                 #run procedure for 2 given points
#                 if len(findSVOinpoints(point1, point2, sub,verb,obj)) > 0:
#                     for j in findSVOinpoints(point1, point2, sub,verb,obj):
#                         svopairs.append(j)
#             else:
#                 #run procedure for adjusting point 2 to point 1 and making a new point 2
#                 temp = point2
#                 point1 = temp
#                 point2 = sub[i]
#                 if len(findSVOinpoints(point1, point2, sub,verb,obj)) > 0:
#                     for j in findSVOinpoints(point1, point2, sub,verb,obj):
#                         svopairs.append(j)
#     return svopairs
#
#
# def remove_dot_acronym(s):
#     m = re.search('(.*?)(([a-zA-Z]\.){2,})(.*)', s)
#     if m:
#         replacement = ''.join(m.group(2).split('.'))
#         s = m.group(1) + replacement + m.group(4)
#         return s
#     else:
#         return m
#
# def remove_abbrev(text):
#     temp = remove_dot_acronym(text)
#     while temp != None:
#         text = temp
#
#         temp = remove_dot_acronym(text)
#
#     text = re.sub(r"(?<= [.(a-zA-Z)]{3})\.(?!=(\n))", '', text)
#     text = re.sub(r"(?<= [a-zA-Z]{2})\.(?!=(\n))", '', text)
#
#     return text
#
# def displayResults(highest_key, highest_score, sen_map, sentences):
#     print('Sentence key: ',highest_key,' Sentence score: ', highest_score)
#     print(sen_map[highest_key])
#     print(sen_map)
#     print('------------------------------------')
#
# # print(returnresult(text2, question))
# def returnresult(text, question, numofanswers):
#     question = question.lower()
#     text = text.lower()
#
#     questiondoc = nlp(question)
#
#     text = remove_abbrev(text)
#
#     doc = nlp(text)
#     sentences = [sent.string.strip() for sent in doc.sents]
#     print(sentences)
#     scores = {}
#     for sentence in sentences:
#         scores[sentence.lower()] = spacyMatching.matching(question, sentence, wv)
#
#     sort_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
#
#     if sort_scores[0][1] <= 0.5 or math.isnan(sort_scores[0][1]):
#         return scores, ['there was no match']
#     else:
#         returnlist = []
#         for i in range(numofanswers):
#             returnlist.append(sort_scores[i][0])
#
#         print('1st: ', sort_scores[0])
#         print('2nd: ', sort_scores[1])
#         print('3rd: ', sort_scores[2])
#     return scores, returnlist
