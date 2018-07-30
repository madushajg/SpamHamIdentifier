import os.path
import csv

# dir = os.path.dirname(__file__)
# print(dir)
root_path = os.path.normpath(os.getcwd() + os.sep + os.pardir) + '/HamSpam/Resources'
# print(root_path)
os.chdir(root_path)
hamTextOpen = os.path.join(root_path, "ham.txt")
spamTextOpen = os.path.join(root_path, "spam.txt")


def clasify_tsv():
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


if __name__ == '__main__':
    clasify_tsv()
