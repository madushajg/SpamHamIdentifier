from nltk.tokenize import TweetTokenizer
from itertools import tee, islice

tknzr = TweetTokenizer()
msg = "SIX chances to win CASH."
tokens = tknzr.tokenize(msg)


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


b = find_bigrams(tokens)
print(b)
