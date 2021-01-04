import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import scipy
import numpy as np
from scipy import spatial


def avg_feature_vector(sentence, model, num_features, index2word_set):
    stop_words = ['a', 'an', 'the']
    # words = sentence.split()
    feature_vec = np.zeros((num_features,), dtype='float32')
    n_words = 0
    words = [token.text for token in sentence if not token.is_stop]
    for word in words:
        # if word in index2word_set and not word in stop_words:
        if word in index2word_set:
            n_words += 1
            feature_vec = np.add(feature_vec, model[word])
    if (n_words > 0):
        feature_vec = np.divide(feature_vec, n_words)
    return feature_vec

def matching(a, b, word2vec):
    index2word_set = set(word2vec.wv.index2word)
    s1_afv = avg_feature_vector(a, model=word2vec, num_features=300, index2word_set=index2word_set)
    s2_afv = avg_feature_vector(b, model=word2vec, num_features=300, index2word_set=index2word_set)
    sim = 1 - spatial.distance.cosine(s1_afv, s2_afv)
    return sim
