# import pandas as pd
# import numpy as np
#
#
# url = "https://raw.githubusercontent.com/madushajg/SpamHamIdentifier/master/SMSSpamCollection.tsv"
#
# url_data = pd.read_table(url, sep='\t')
# print(url_data.head(3))

import csv
from nltk.tokenize import word_tokenize

ham = open("ham.txt", "w+")
spam = open("spam.txt", "w+")

# WORD_TOKENIZER = word_tokenize()

with open('SMSSpamCollection.tsv') as tsvfile:
    reader = csv.DictReader(tsvfile, dialect='excel-tab')
    for row in reader:
        label = row['Label']
        if label == 'ham':
            ham.write(row['Text'])
            ham.write("\n")
        else:
            spam.write(row['Text'])
            spam.write("\n")
            # print(row['Text'])

f = open('ham.txt', 'r')
ham_massege = f.read()
wt = word_tokenize(ham_massege)
print(len(wt))

f2 = open('spam.txt', 'r')
spam_massege = f2.read()
wt2 = word_tokenize(spam_massege)
print(len(wt2))
