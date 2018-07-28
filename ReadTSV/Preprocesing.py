import os
# from nltk.tokenize import word_tokenize
from nltk import pr
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from collections import Counter
from itertools import tee, islice

english_stops = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
# tokenizer = RegexpTokenizer("[\w']+")
# tokenizer = RegexpTokenizer('\s+', gaps= True)
tokenizer = TweetTokenizer()

hamTextOpen = os.path.join(os.path.dirname(__file__), "ham.txt")
hamText = open(hamTextOpen, 'r')

spamTextOpen = os.path.join(os.path.dirname(__file__), "spam.txt")
spamText = open(spamTextOpen, 'r')

ham_massege = hamText.read()
# wt = word_tokenize(ham_massege)
rgxt1 = tokenizer.tokenize(ham_massege)
tokens = [token.lower() for token in rgxt1]

filtered_sw = [word for word in tokens if word not in english_stops]

lemmatized_tknz = list(())

# for ftk in filtered_sw:
for ftk in tokens:
    lemma = lemmatizer.lemmatize(ftk)
    lemmatized_tknz.append(lemma)

fdist = FreqDist(lemmatized_tknz)
print(fdist.items())
# print(fdist['to'])
# fdist.plot(50)
# fdist.plot(50, cumulative=True)

# print(len(rgxt1), len(filtered_sw), len(set(lemmatized_tknz)))
# print(wt)
# print("---------------------------------------------------------------------------")
# print(rgxt1)
# print(filtered_sw)
# print(lemmatized_tknz)

spam_massege = spamText.read()
# wt2 = word_tokenize(spam_massege)
rgxt2 = tokenizer.tokenize((spam_massege))

spam_tokens = [token.lower() for token in rgxt2]

filtered_spam_sw = [word for word in spam_tokens if word not in english_stops]

lemmatized_spam_tknz = list(())

# for ftk in filtered_spam_sw:
for ftk in spam_tokens:
    lemma = lemmatizer.lemmatize(ftk)
    lemmatized_spam_tknz.append(lemma)

fdist_spam = FreqDist(lemmatized_spam_tknz)
print(fdist_spam.items())
# fdist_spam.plot(50)
# fdist_spam.plot(50, cumulative=True)

print(len(rgxt2), len(lemmatized_spam_tknz), len(set(lemmatized_spam_tknz)))


def ngrams(lst, n):
    tlst = lst
    while True:
        a, b = tee(tlst)
        l = tuple(islice(a, n))
        if len(l) == n:
            yield l
            next(b)
            tlst = b
        else:
            break


bigrams_ham = Counter(ngrams(rgxt1, 2))
bigrams_spam = Counter(ngrams(rgxt2, 2))
# print(bigrams_ham)


for k, v in bigrams_ham.items():
    print(k, v)

Message1 = " Sorry, ..use your brain dear"
Message2 = " SIX chances to win CASH."

tokens_msg1 = tokenizer.tokenize(Message1)
print(tokens_msg1)
tokens_msg2 = tokenizer.tokenize(Message2)

bigrams_msg1 = Counter(ngrams(tokens_msg1, 2))

probability_values = list(())

for i, j in bigrams_msg1.items():
    a = i[0].lower()
    b = i[1].lower()
    print(a, b)
    uni_count = fdist_spam[a]
    bi_count = bigrams_spam[a, b]
    if uni_count != 0 :
        probability_values.append((uni_count, bi_count, bi_count / uni_count))

print(fdist[','])
print(bigrams_ham[',', '..'])
print(probability_values)
prob_ham = float(
    probability_values[0][2] * probability_values[1][2] * probability_values[2][2] * probability_values[3][2] *
    probability_values[4][2] * probability_values[5][2])
print(format(prob_ham, '.12g'))

print(probability_values[0][2])
print(probability_values[1][2])
print(probability_values[2][2])
