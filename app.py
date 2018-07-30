from Text_Processor import probability_manager
from nltk.tokenize import TweetTokenizer

uni_bigramvalues = probability_manager.activities()
tokenizer = TweetTokenizer()

fdist_ham = uni_bigramvalues[0]
fdist_spam = uni_bigramvalues[1]
bigrams_ham = uni_bigramvalues[2]
bigrams_spam = uni_bigramvalues[3]


def find_bigrams(tklist):
    bg = list(())
    pr = None
    for tk in tklist:
        if pr is not None:
            bg.append((pr, tk))
        pr = tk
    return bg


def calculate_probabilities(new_tokens, fdist, bigrams):
    pv = list(())
    for t in new_tokens:
        a = t[0].lower()
        b = t[1].lower()
        uni_count = fdist[a]
        bi_count = bigrams[a, b]
        pv.append((uni_count, bi_count, (bi_count + 1) / (uni_count + len(fdist))))
    return pv


def find_final_probability(pvalues):
    f = 1
    for p in pvalues:
        f *= p[2]
    return f


def find_type():
    msg = input()
    msg_tokens = tokenizer.tokenize(msg)

    bigrams_msg = find_bigrams(msg_tokens)

    probability_values_ham = calculate_probabilities(bigrams_msg, fdist_ham, bigrams_ham)
    probability_values_spam = calculate_probabilities(bigrams_msg, fdist_spam, bigrams_spam)

    print(probability_values_ham)
    print(probability_values_spam)

    final_prob_ham = find_final_probability(probability_values_ham)
    final_prob_spam = find_final_probability(probability_values_spam)

    print(format(final_prob_ham, '.12g'))
    print(format(final_prob_spam, '.12g'))

    if final_prob_ham >= final_prob_spam:
        print("Ham")
    else:
        print("Spam")


if __name__ == '__main__':
    find_type()
