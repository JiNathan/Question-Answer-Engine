import nltk
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('wordnet')

words = ['justify', 'justified', 'justifiable']
for word in words:
    print (word + "-->" + WordNetLemmatizer().lemmatize(word,'v'))