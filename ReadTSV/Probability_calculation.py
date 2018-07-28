import os
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from collections import Counter
from itertools import tee, islice

english_stops = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
tokenizer = TweetTokenizer()

hamTextOpen = os.path.join(os.path.dirname(__file__), "ham.txt")
hamText = open(hamTextOpen, 'r')
spamTextOpen = os.path.join(os.path.dirname(__file__), "spam.txt")
spamText = open(spamTextOpen, 'r')

ham_massege = hamText.read()
tknzd_ham = tokenizer.tokenize(ham_massege)
ham_tokens = [token.lower() for token in tknzd_ham]

filtered_sw_ham = [word for word in ham_tokens if word not in english_stops]

lemmatized_ham_tknz = list(())

# for tokens in filtered_sw:
for tokens in ham_tokens:
    lemma = lemmatizer.lemmatize(tokens)
    lemmatized_ham_tknz.append(lemma)

fdist_ham = FreqDist(lemmatized_ham_tknz)
print(fdist_ham.items())

print(len(set(lemmatized_ham_tknz)), len(fdist_ham))

spam_massege = spamText.read()
tknzd_spam = tokenizer.tokenize(spam_massege)

spam_tokens = [token.lower() for token in tknzd_spam]

filtered_sw_spam = [word for word in spam_tokens if word not in english_stops]

lemmatized_spam_tknz = list(())

# for tokens in filtered_spam_sw:
for tokens in spam_tokens:
    lemma = lemmatizer.lemmatize(tokens)
    lemmatized_spam_tknz.append(lemma)

fdist_spam = FreqDist(lemmatized_spam_tknz)
print(fdist_spam.items())

print(len(set(lemmatized_spam_tknz)), len(fdist_spam))


def find_bigrams(tokenlist):
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


def calculate_probabilities(new_tokens, fdist, bigrams, prob_values):
    for i, j in new_tokens.items():
        a = i[0].lower()
        b = i[1].lower()
        print(a, b)
        uni_count = fdist[a]
        bi_count = bigrams[a, b]
        prob_values.append((uni_count, bi_count, (bi_count + 1) / (uni_count + len(fdist))))


def find_final_probability(pvalues):
    f = 1
    for p in pvalues:
        f *= p[2]
    return f


bigrams_ham = Counter(find_bigrams(ham_tokens))
bigrams_spam = Counter(find_bigrams(spam_tokens))

for k, v in bigrams_ham.items():
    print(k, v)

# Message1 = " Sorry, ..use your brain dear"
# Message1 = " SIX chances to win CASH."
Message1 = input()

tokens_msg1 = tokenizer.tokenize(Message1)
# tokens_msg2 = tokenizer.tokenize(Message2)

bigrams_msg1 = Counter(find_bigrams(tokens_msg1))

probability_values_ham = list(())
probability_values_spam = list(())

calculate_probabilities(bigrams_msg1, fdist_ham, bigrams_ham, probability_values_ham)
calculate_probabilities(bigrams_msg1, fdist_spam, bigrams_spam, probability_values_spam)

print(probability_values_ham)
print(probability_values_spam)

final_prob_ham = find_final_probability(probability_values_ham)
final_prob_spam = find_final_probability(probability_values_spam)

print(format(final_prob_ham, '.12g'))
print(format(final_prob_ham))

print(format(final_prob_spam, '.12g'))
print(format(final_prob_spam))

if final_prob_ham >= final_prob_spam:
    print("Ham")
else:
    print("Spam")
