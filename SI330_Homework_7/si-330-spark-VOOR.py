######################### 
### John Voorhess
### Homework 7
### SI330 Fall 2017
### Dr. Teplovs
### Based on code created by Kevyn Collins-Thompson
### 
########################## 

import json
import math
import re
from pyspark import SparkContext
from pyspark import SparkConf
import si330_helper

conf = (SparkConf().set("spark.hadoop.validateOutputSpecs", "false").setAppName("PythonYelpSentiment"))
sc2 = SparkContext(conf = conf)
sc2.addPyFile('hdfs:///var/si330f17/si330_helper.py')

### Only keep more frequent words whose frequency is more than this threshold:
frequent_word_threshold = 5000

WORD_RE = re.compile(r'\b[\w]+\b')

### This helper function takes a dictionary loaded from the Yelp JSON business entry
### and creates a list of tuples of the form (rating, w) for each word w in a Yelp review with a given rating.
def convert_dict_to_tuples(d):
    text   = d['text'].lower()
    rating = d['stars']

    tokens = WORD_RE.findall(text)
    tuples = []

    for w in tokens:
        tuples.append((rating, w))

    return tuples

input_file = sc2.textFile("/var/si330f17/yelp_academic_dataset_review.json")

### convert each json review into a dictionary.  HINT: use the json module
step_1a = input_file.map(lambda line: json.loads(line))

### convert a review's dictionary to a list of (rating, word) tuples.  HINT: Use convert_dict_to_tuples
step_1b = step_1a.flatMap(lambda x: convert_dict_to_tuples(x))

### count all words from all reviews
step_2a1 = step_1b
step_2a2 = step_2a1.map(lambda x: (x[1],1))
step_2a3 = step_2a2.reduceByKey(lambda x,y: x+y)
### filter out all word-tuples from positive reviews
step_2b1 = step_1b.filter(lambda x: x[0] >= 4)

### count all words from positive reviews
step_2b2 = step_2b1.map(lambda x: (x[1],1))
step_2b3 = step_2b2.reduceByKey(lambda x,y: x+y)
### filter out all word-tuples from negative reviews
step_2c1 = step_1b.filter(lambda x: x[0] <= 2)

### count all words from negative reviews
step_2c2 = step_2c1.map(lambda x: (x[1],1))
step_2c3 = step_2c2.reduceByKey(lambda x,y: x+y)
### get total word count for all, positive, and negative reviews
all_review_word_count = step_2a3.map(lambda x: (1,x[1])).reduceByKey(lambda x,y: x+y).collect()[0][1]
pos_review_word_count = step_2b3.map(lambda x: (1,x[1])).reduceByKey(lambda x,y: x+y).collect()[0][1]
neg_review_word_count = step_2c3.map(lambda x: (1,x[1])).reduceByKey(lambda x,y: x+y).collect()[0][1]

### filter to keep only frequent words, i.e. those with
### count greater than frequent_word_threshold.
freq_words = step_2a3.filter(lambda x: x[1] > 5000)

### filter to keep only those word count tuples whose word can
### be found in the frequent list
step_3pos = freq_words.join(step_2b3)
step_3neg = freq_words.join(step_2c3)

### compute the log ratio score for each positive review word
# UNCOMMENT THE NEXT LINE
unsorted_positive_words = step_3pos.map(lambda x: (x[0], math.log(float(x[1][1])/pos_review_word_count) - math.log(float(x[1][1])/all_review_word_count)))

### sort by descending score to get the top-scoring positive words
sorted_positive_words = unsorted_positive_words.sortBy(lambda x:x[1], False)

### compute the log ratio score for each negative review word
# UNCOMMENT THE NEXT LINE
unsorted_negative_words = step_3neg.map(lambda x: (x[0], math.log(float(x[1][1])/neg_review_word_count) - math.log(float(x[1][1])/all_review_word_count)))

### sort by descending score to get the top-scoring negative words
sorted_negative_words = unsorted_negative_words.sortBy(lambda x:x[1], False)

### write out the top-scoring positive words to a text file
sorted_positive_words.saveAsTextFile('/user/voor/output-positive/part-00000')

### write out the top-scoring negative words to a text file
sorted_negative_words.saveAsTextFile('/user/voor/output-negative/part-00000')

### Let Spark know the job is done
sc2.stop()
