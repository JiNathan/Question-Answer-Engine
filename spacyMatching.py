import spacy
nlp = spacy.load('en_core_web_lg')
def matching(a, b):
    token1 = nlp(a)
    token2 = nlp(b)
    return token1.similarity(token2)

print(matching('president obama', 'obama'))


#['president obama', 'accepted', 'the nobel peace prize']['obama', 'receive', 'the nobel peace prize']
#['obama', 'justify', 'the wars'] ['war', 'justified', 'self-defense']
#['justifiable', 'according', 'obama'] ['war', 'justified', 'self-defense']

#old version: matchrating += (returnWeight(temp0, wordweightdict) + spacyMatching.matching(i[0], p) * 2)/3