##################
# John Voorhess
# Homework 6
# SI330 Fall 2017
##################



import nltk
from nltk.tokenize import RegexpTokenizer
nltk.download('punkt')

############
# NOTE:
#
# Preamble and postamble text have been removed manually.
# It took seconds and didn't warrant code that wouldn't
# be reusable without handling edge cases far out of scope.
#
############

# open the text file and store the file object in a variable, f
f = open('lesmis.txt', 'r')

# store the file in an object variable
rawLesMiserables = f.read()

# load up an english pickle
sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')

# open an output file
with open('lesmissentences.txt','w') as f:
    # write each sentence as it's own line in a new file
    f.write('\n'.join(sentence_detector.tokenize(rawLesMiserables.strip().replace("\n"," "))))

