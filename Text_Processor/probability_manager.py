import os.path
from pathlib import Path

from Text_Processor import TSV_classifier
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from collections import Counter
from itertools import tee, islice

english_stops = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
tokenizer = TweetTokenizer()

dir = os.path.dirname(__file__)
root_path = os.path.normpath(os.getcwd() + os.sep + os.pardir) + '/Resources'
os.chdir(root_path)

ham_file = Path(root_path+"/ham.txt")
spam_file = Path(root_path+"/spam.txt")
if ham_file.is_file() & spam_file.is_file():
    print("ham.txt and spam.txt are already there")
else:
    TSV_classifier.clasify_tsv()


hamTextOpen = os.path.join(root_path, "ham.txt")
spamTextOpen = os.path.join(root_path, "spam.txt")

hamText = open(hamTextOpen, 'r')
spamText = open(spamTextOpen, 'r')


def tokenize_text(text):
    message = text.read()
    tknzd_msg = tokenizer.tokenize(message)
    tokens = [token.lower() for token in tknzd_msg]
    return tokens


def drop_stopwords(tokens):
    sw_filter = [word for word in tokens if word not in english_stops]
    return sw_filter


def lemmatize_tokens(tokens):
    l_tokens = list(())
    for tks in tokens:
        lemma = lemmatizer.lemmatize(tks)
        l_tokens.append(lemma)
    return l_tokens


def calculate_bigrams(tokenlist):
    n = 2
    tlist = tokenlist
    while True:
        a, b = tee(tlist)
        l = tuple(islice(a, n))
        if len(l) == n:
            yield l
            next(b)
            tlist = b
        else:
            break


def activities():
    ham_tokens = tokenize_text(hamText)
    spam_tokens = tokenize_text(spamText)

    filtered_sw_ham = drop_stopwords(ham_tokens)
    filtered_sw_spam = drop_stopwords(spam_tokens)

    lemmatized_ham_tknz = lemmatize_tokens(
        ham_tokens)  # If we pass filtered_sw_ham, the Vocabulary value may change.
    lemmatized_spam_tknz = lemmatize_tokens(
        spam_tokens)  # If we pass filtered_sw_spam, the Vocabulary value may change.

    fdist_ham = FreqDist(ham_tokens)
    print(len(FreqDist(ham_tokens)), len(FreqDist(lemmatized_ham_tknz)))
    fdist_spam = FreqDist(spam_tokens)
    print(len(FreqDist(spam_tokens)), len(FreqDist(lemmatized_spam_tknz)))

    # print(fdist_ham.items())
    # print(len(set(lemmatized_ham_tknz)), len(fdist_ham))

    # print(fdist_spam.items())
    # print(len(set(lemmatized_spam_tknz)), len(fdist_spam))

    bigrams_ham = Counter(calculate_bigrams(ham_tokens))
    bigrams_spam = Counter(calculate_bigrams(spam_tokens))

    return fdist_ham, fdist_spam, bigrams_ham, bigrams_spam


if __name__ == '__main__':
    activities()
