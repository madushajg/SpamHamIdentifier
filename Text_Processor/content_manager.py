import os.path
import csv
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from collections import Counter
from nltk import ngrams

english_stops = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
tokenizer = TweetTokenizer()

root_path = os.path.normpath(os.getcwd() + os.sep + os.pardir) + '/SpamHamIdentifier/Resources'
os.chdir(root_path)


def separate_content():
    tsvfile = open('SMSSpamCollection.tsv', "r")
    read = csv.reader(tsvfile)
    content = list(())
    for data in read:
        temp = ""
        for x in range(len(data)):
            if x == 0:
                temp = temp + (data[x])
            elif x > 0:
                temp = temp + ',' + data[x]
        label, body = temp.split('\t')
        content.append((label, body))

    return content


def tokenize_text(message):
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


def preprocessor():
    tokens = list(())
    sw_less_tokens = list(())
    lemmatized_tokens = list(())

    messages = separate_content()
    for msg in messages:
        l = msg[0]
        tkns = tokenize_text(msg[1])
        tokens.append((l, tkns))
        # sw_free_tkns = drop_stopwords(tkns)
        # sw_less_tokens.append((l,sw_free_tkns))
        lemmatized_tokens.append((l, lemmatize_tokens(tkns)))

    return tokens, sw_less_tokens, lemmatized_tokens


def find_unigrams(tknz):
    unigrams_ham = list(())
    unigrams_spam = list(())
    for data in tknz:
        label = data[0]
        body = data[1]
        if label == 'ham':
            for i in body:
                unigrams_ham.append(i)
        elif label == 'spam':
            for i in body:
                unigrams_spam.append(i)
    print(len(set(unigrams_ham)), len(set(unigrams_spam)))
    print(len(FreqDist(unigrams_ham)), len(FreqDist(unigrams_spam)))
    return unigrams_ham, unigrams_spam


def find_bigrams(tknz):
    n = 2
    bigrams_ham = list(())
    bigrams_spam = list(())
    for data in tknz:
        label = data[0]
        body = data[1]
        if label == 'ham':
            bi_h = ngrams(body, n)
            for bigrm in bi_h:
                bigrams_ham.append(bigrm)

        elif label == 'spam':
            bi_s = ngrams(body, n)
            for bigrm in bi_s:
                bigrams_spam.append(bigrm)

    return bigrams_ham, bigrams_spam


if __name__ == '__main__':
    tk, sw_tk, lm_tk = preprocessor()
    uni_ham, uni_spam = find_unigrams(lm_tk)
    # print(Counter(uni_spam))
    # print(FreqDist(uni_spam).items())
    bi_ham, bi_spam = find_bigrams(lm_tk)
    print(Counter(bi_spam))
