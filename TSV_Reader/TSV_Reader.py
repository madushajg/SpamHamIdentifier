import os.path
import csv

root_path = os.path.normpath(os.getcwd() + os.sep + os.pardir)
os.chdir(root_path+'/Resources')
hamTextOpen = os.path.join(root_path, "ham.txt")
spamTextOpen = os.path.join(root_path, "spam.txt")


ham = open("ham.txt", "w+")
spam = open("spam.txt", "w+")


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


# f = open('ham.txt', 'r')
# ham_massege = f.read()
# wt = word_tokenize(ham_massege)
# print(len(wt))
#
# f2 = open('spam.txt', 'r')
# spam_massege = f2.read()
# wt2 = word_tokenize(spam_massege)
# print(len(wt2))
