#!/usr/bin/python

##################
# John Voorhess
# Homework 6
# SI330 Fall 2017
##################

from mrjob.job import MRJob
from mrjob.step import MRStep
import nltk
from nltk.tokenize import RegexpTokenizer

# STOP_WORDS are to be checked against and bigrams containing words in STOP_WORDS will be omitted from output.
STOP_WORDS = {'their', 'she', 'did', 'not', 'needn', 'have', 'all', 'a', 'has', 'between', 'shouldn', 'where', 'these', 'had', 'ours', 'who', 'further', 'does', 's', 't', 'are', 'isn', 'should', 'both', 'against', 'll', 're', 'can', 'that', 'few', 'out', 'no', 'hers', 'myself', 'but', 'at', 'too', 'once', 'the', 'there', 'o', 'this', 'down', 'in', 'some', 'and', 'weren', 'we', 'own', 'into', 'don', 'other', 'him', 'during', 'himself', 'having', 'them', 'why', 'ain', 'each', 'it', 'when', 'were', 'will', 'mightn', 'very', 'aren', 'am', 'mustn', 'they', 'ourselves', 'only', 'd', 'or', 'than', 'if', 'itself', 'from', 'i', 'being', 'her', 'me', 'after', 'yourselves', 'more', 'yours', 'through', 'those', 'of', 'you', 'doesn', 'about', 'to', 'y', 'your', 'doing', 'just', 'herself', 'now', 'wouldn', 'its', 'been', 'under', 'hadn', 'wasn', 'above', 'any', 'nor', 'over', 'because', 'on', 'shan', 'themselves', 've', 'off', 'while', 'then', 'how', 'so', 'until', 'most', 'our', 'up', 'is', 'yourself', 'was', 'what', 'before', 'which', 'same', 'again', 'didn', 'haven', 'ma', 'be', 'do', 'with', 'won', 'm', 'couldn', 'whom', 'my', 'theirs', 'below', 'such', 'for', 'his', 'an', 'by', 'hasn', 'as', 'here', 'he'}


class MRRatingsCounter(MRJob):

  
    def steps(self):
        return [

            # sequence of mapper and reducer steps is defined
            MRStep(mapper=self.mapper_get_bigrams,
                   reducer=self.reducer_count_ratings),
            MRStep(reducer = self.sort_bigrams)

        ]
    # mapper operates on the input file one line at a time
    def mapper_get_bigrams(self, _, line):
        # a tokenizer instance is instantiated
        tokenizer = RegexpTokenizer('\w+')
        # tokenizer splits each line into a list of words
        words = tokenizer.tokenize(line)
        # the bigrams method of the natural language toolkit
        # creates bigrams out of the list of words
        bigrams = nltk.bigrams(words)

        # check bigrams against STOP_WORDS dictionary
        # prior to filtering out stop words, bigram count was 533720
        # after filtering stop words, bigram count is 93382

        for bigram in bigrams:
            # bigram is converted to lowercase
            a = bigram[0]
            b = bigram[1]
            y = a.lower()
            z = b.lower()
            # a new tuple representing the lowercase bigram is created
            lowerBigram = (y, z)
            # both elements of the tuple are checked against STOP_WORDS
            if lowerBigram[0] not in STOP_WORDS and lowerBigram[1] not in STOP_WORDS:
                outputBigram = lowerBigram
        # wrap the yield statement in a try/except incase something is messed up
        try:

            # emit each bigram and a frequency to be summed
            yield outputBigram,1
        except:
            # ignore mistakes
            pass

  ### input: self, in_key from mapper, in_value from mapper
    def reducer_count_ratings(self, key, values):

        # flip/flop the yield so that we can sort by the sum(values)
        # use 1/sum to sort descending
        yield str(1/(sum(values))).zfill(4),key

    def sort_bigrams(self, count, bigrams):
        # the sort is completed here.
        # Since the system automatically sorts by key,
        # we yield count as the key and the bigram as the value
        for bigram in bigrams:

            yield count, bigram

if __name__ == '__main__':
  MRRatingsCounter.run()


