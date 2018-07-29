import os.path
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from collections import Counter
from itertools import tee, islice

english_stops = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
tokenizer = TweetTokenizer()

# root_path = os.path.normpath(os.getcwd() + os.sep + os.pardir) + '/Resources'
# os.chdir(root_path)
# hamTextOpen = os.path.join(root_path, "ham.txt")
# spamTextOpen = os.path.join(root_path, "spam.txt")

dir = os.path.dirname(__file__)
# print(dir)
root_path = os.path.normpath(os.getcwd() + os.sep + os.pardir) + '/HamSpam/Resources'
# print(root_path)
os.chdir(root_path)
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


def calculate_probabilities(new_tokens, fdist, bigrams):
    pv = list(())
    for t in new_tokens:
        a = t[0].lower()
        b = t[1].lower()
        uni_count = fdist[a]
        bi_count = bigrams[a, b]
        pv.append((uni_count, bi_count, (bi_count + 1) / (uni_count + len(fdist))))
    return pv


def find_bigrams(tklist):
    bg = list(())
    pr = None
    for tk in tklist:
        if pr is not None:
            bg.append((pr, tk))
        pr = tk
    return bg


def find_final_probability(pvalues):
    f = 1
    for p in pvalues:
        f *= p[2]
    return f


def activities():
    ham_tokens = tokenize_text(hamText)
    spam_tokens = tokenize_text(spamText)

    filtered_sw_ham = drop_stopwords(ham_tokens)
    filtered_sw_spam = drop_stopwords(spam_tokens)

    lemmatized_ham_tknz = lemmatize_tokens(
        ham_tokens)  # If we pass filtered_sw_ham, the Vocabulary value may change.
    lemmatized_spam_tknz = lemmatize_tokens(
        spam_tokens)  # If we pass filtered_sw_spam, the Vocabulary value may change.

    fdist_ham = FreqDist(lemmatized_ham_tknz)
    fdist_spam = FreqDist(lemmatized_spam_tknz)

    # print(fdist_ham.items())
    # print(len(set(lemmatized_ham_tknz)), len(fdist_ham))

    # print(fdist_spam.items())
    # print(len(set(lemmatized_spam_tknz)), len(fdist_spam))

    bigrams_ham = Counter(calculate_bigrams(ham_tokens))
    bigrams_spam = Counter(calculate_bigrams(spam_tokens))

    return fdist_ham, fdist_spam, bigrams_ham, bigrams_spam

    # msg = input()
    #
    # msg_tokens = tokenizer.tokenize(msg)
    #
    # bigrams_msg = find_bigrams(msg_tokens)
    #
    # probability_values_ham = calculate_probabilities(bigrams_msg, fdist_ham, bigrams_ham)
    # probability_values_spam = calculate_probabilities(bigrams_msg, fdist_spam, bigrams_spam)
    #
    # print(probability_values_ham)
    # print(probability_values_spam)
    #
    # final_prob_ham = find_final_probability(probability_values_ham)
    # final_prob_spam = find_final_probability(probability_values_spam)
    #
    # print(format(final_prob_ham, '.12g'))
    # print(final_prob_ham)
    #
    # print(format(final_prob_spam, '.12g'))
    # print(final_prob_spam)
    #
    # if final_prob_ham >= final_prob_spam:
    #     print("Ham")
    # else:
    #     print("Spam")


if __name__ == '__main__':
    activities()
