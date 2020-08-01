import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nlp = spacy.load('en_core_web_lg')
# def matching(a, b):
#     token1 = nlp(a)
#     token2 = nlp(b)
#     return token1.similarity(token2)
def matching(X, Y):
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
    return cosine
# print(matching('The United States Flag', 'what other kind'))
# a = [['flag', 'embody', 'common mission'], ['flag', 'embody', 'warrior'], ['mr. esper', 'say', 'his memo'], ['mr. esper', 'say', 'john paul stevens'], ['mr. esper', 'quote', 'john paul stevens'], ['mr. esper', 'john paul stevens', 'john paul stevens'], ['the united states flag', 'be', 'a symbol'], ['the united states flag', 'be', 'freedom'], ['the united states flag', 'be', 'equal opportunity'], ['the united states flag', 'be', 'religious tolerance'], ['the united states flag', 'be', 'good will'], ['the united states flag', 'be', 'other peoples']]
# b = ['what other kind', 'are', 'the new directive']
#
# for i in a:
#     sum = 0
#     print('----------------------------------')
#     print(i)
#     for j in range(3):
#         print(i[j], b[j], matching(i[j], b[j]))
#         sum += matching(i[j], b[j])
#     print(sum)


#['president obama', 'accepted', 'the nobel peace prize']['obama', 'receive', 'the nobel peace prize']
#['obama', 'justify', 'the wars'] ['war', 'justified', 'self-defense']
#['justifiable', 'according', 'obama'] ['war', 'justified', 'self-defense']

#old version: matchrating += (returnWeight(temp0, wordweightdict) + spacyMatching.matching(i[0], p) * 2)/3