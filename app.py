from Text_Processor import content_manager
from nltk.tokenize import TweetTokenizer
from nltk.probability import FreqDist
from collections import Counter

tk, sw_tk, lm_tk = content_manager.preprocessor()
uni_ham, uni_spam = content_manager.find_unigrams(lm_tk)
bi_ham, bi_spam = content_manager.find_bigrams(lm_tk)
tokenizer = TweetTokenizer()

unigrams_ham = FreqDist(uni_ham)
unigrams_spam = FreqDist(uni_spam)
bigrams_ham = Counter(bi_ham)
bigrams_spam = Counter(bi_spam)

print(unigrams_spam.items())

def find_new_bigrams(tklist):
    bg = list(())
    pr = None
    for tk in tklist:
        if pr is not None:
            bg.append((pr, tk))
        pr = tk
    return bg


def calculate_probabilities(new_tokens, unig, bigrams):
    pv = list(())
    for t in new_tokens:
        a = t[0].lower()
        b = t[1].lower()
        uni_count = unig[a]
        bi_count = bigrams[a, b]
        # print(a, uni_count)
        # print(a, b, bi_count)
        pv.append((uni_count, bi_count, (bi_count + 1) / (uni_count + len(unig))))
    return pv


def find_final_probability(pvalues):
    f = 1
    for p in pvalues:
        f *= p[2]
    return f


def find_type():
    msg = input("Enter the message :")
    msg_tokens = tokenizer.tokenize(msg)
    lemmatized_msg_tokens = content_manager.lemmatize_tokens(msg_tokens)

    bigrams_msg = find_new_bigrams(lemmatized_msg_tokens)

    probability_values_ham = calculate_probabilities(bigrams_msg, unigrams_ham, bigrams_ham)
    probability_values_spam = calculate_probabilities(bigrams_msg, unigrams_spam, bigrams_spam)

    # print(probability_values_ham)
    # print(probability_values_spam)

    final_prob_ham = find_final_probability(probability_values_ham)
    final_prob_spam = find_final_probability(probability_values_spam)

    print("Ham Probability :", format(final_prob_ham, '.12g'))
    print("Spam Probability: ", format(final_prob_spam, '.12g'))

    print("------------------------------------------------------------------------------------")
    if final_prob_ham >= final_prob_spam:
        print("Ham")
    else:
        print("Spam")
    print("____________________________________________________________________________________")


if __name__ == '__main__':
    find_type()
