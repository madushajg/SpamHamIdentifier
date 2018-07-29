from Text_Processor import probability_manager
from nltk.tokenize import TweetTokenizer

uni_bigramvalues = probability_manager.activities()
tokenizer = TweetTokenizer()

fdist_ham = uni_bigramvalues[0]
fdist_spam = uni_bigramvalues[1]
bigrams_ham = uni_bigramvalues[2]
bigrams_spam = uni_bigramvalues[3]

msg = input()

msg_tokens = tokenizer.tokenize(msg)

bigrams_msg = probability_manager.find_bigrams(msg_tokens)

probability_values_ham = probability_manager.calculate_probabilities(bigrams_msg, fdist_ham, bigrams_ham)
probability_values_spam = probability_manager.calculate_probabilities(bigrams_msg, fdist_spam, bigrams_spam)

print(probability_values_ham)
print(probability_values_spam)

final_prob_ham = probability_manager.find_final_probability(probability_values_ham)
final_prob_spam = probability_manager.find_final_probability(probability_values_spam)

print(format(final_prob_ham, '.12g'))
print(final_prob_ham)

print(format(final_prob_spam, '.12g'))
print(final_prob_spam)

if final_prob_ham >= final_prob_spam:
    print("Ham")
else:
    print("Spam")
