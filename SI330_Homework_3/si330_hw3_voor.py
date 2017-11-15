import profile
import csv
import re

# Here, we are reusing the document distance code
# from docdist1 import count_frequency
from docdist_dict import (count_frequency, get_words_from_string, vector_angle)

# As a convention, "constant" variable names are usually written in all-caps
OUTPUT_FILE = 'Sentence_Database_With_ID.csv'

#MASTER_FILE = 'Sentences_Table_MasterList_sample.csv'
#SENTENCE_DB_FILE = 'Sentence_Database_Without_ID_sample.csv'
MASTER_FILE = 'Sentences_Table_MasterList.csv'
SENTENCE_DB_FILE = 'Sentence_Database_Without_ID.csv'


# Questions:
# How long does it take the program to process the sample csv files, without any speed improvements?  (This is known as the execution time.)
    # 37996681 function calls in 108.603 seconds
# What Python files exist in the Homework 3 folder?
    # docdist1.py
    # docdist_dict.py
    # optimize_this.py
# According to the profiler output, which function takes the most total time (not including subfunctions) and how much?
    # get_words_from_string takes 36.090 seconds
# Also list the total time for each function before making any speed improvements.
#   10.885    docdist1.py:148(inner_product)
#    0.927    docdist1.py:174(vector_angle)
#   36.090    docdist1.py:69(get_words_from_string)
#    4.174    docdist1.py:96(count_frequency)
#    0.074    optimize_this.py:110(lookup_similar_id)
#    1.229    optimize_this.py:151(find_alternate_sentence)
#    0.001    optimize_this.py:221(find_unique_targets)
#    0.003    optimize_this.py:24(main)
#    1.302    optimize_this.py:258(get_csv_rows)
#    0.019    optimize_this.py:270(write_output_file)
#    0.152    optimize_this.py:47(set_sentence_id)
#    0.003    optimize_this.py:79(replace_target_with_blank)

# What was the execution time of the program with the full input files, instead of the sample input files?
    # Without any optimization:
        # 901417495 function calls in 2483.115 seconds
    # With optimization:
        # 32986564 function calls in 124.907 seconds

    #############################
    # TOTAL TIME REDUCTION FACTOR
        # 19.8797
    #############################

    # Profile before optimization FULL FILES:

        #   4211994   93.210    0.000  147.653    0.000 docdist1.py:112(count_frequency)
        #   6317991  248.988    0.000  438.166    0.000 docdist1.py:175(inner_product)
        #   2105997   20.900    0.000  465.402    0.000 docdist1.py:201(vector_angle)
        #   4211994  830.650    0.000 1573.457    0.000 docdist1.py:69(get_words_from_string)
        #       459    0.013    0.000    0.023    0.000 optimize_this.py:116(replace_target_with_blank)
        #       453    2.025    0.004  126.572    0.279 optimize_this.py:158(lookup_similar_id)
        #       453   26.672    0.059 2282.213    5.038 optimize_this.py:209(find_alternate_sentence)
        #       453    0.010    0.000    0.018    0.000 optimize_this.py:318(find_unique_targets)
        #      1819   29.943    0.016  257.718    0.142 optimize_this.py:364(get_csv_rows)
        #       459    0.210    0.000    6.715    0.015 optimize_this.py:384(write_output_file)
        #         1    0.022    0.022 2483.113 2483.113 optimize_this.py:46(main)
        #       459    2.203    0.005   67.526    0.147 optimize_this.py:79(set_sentence_id)

    # Profile after optimiation FULL FILES:
       #    4211994   14.370    0.000   14.370    0.000 docdist_dict.py:109(count_frequency)
       #    6317991   18.684    0.000   18.684    0.000 docdist_dict.py:137(inner_product)
       #    2105997   18.160    0.000   42.552    0.000 docdist_dict.py:151(vector_angle)
       #    4211994   15.643    0.000   38.804    0.000 docdist_dict.py:93(get_words_from_string)
       #          1    0.015    0.015  124.906  124.906 optimize_this.py:123(main)
       #        459    1.437    0.003    2.683    0.006 optimize_this.py:160(set_sentence_id)
       #        459    0.012    0.000    0.021    0.000 optimize_this.py:197(replace_target_with_blank)
       #        453    0.293    0.001    0.293    0.001 optimize_this.py:244(lookup_similar_id)
       #        453   19.319    0.043  115.045    0.254 optimize_this.py:295(find_alternate_sentence)
       #        453    0.009    0.000    0.017    0.000 optimize_this.py:404(find_unique_targets)
       #          2    0.018    0.009    0.157    0.078 optimize_this.py:450(get_csv_rows)
       #        459    0.207    0.000    6.666    0.015 optimize_this.py:470(write_output_file)

# Which function had the highest total time even after your speed improvements and how much?
    # find_alternate_sentence: 19.319 seconds

# What did you learn from this homework?
    # the quickest way to make a big change in runtime is to change functions that are repeatedly
    # called from using lists to using dictionaries for lookups since dictionaries are significantly
    # faster and lists can be O(N^2) or worse if used with other inefficient data structures.

######
# Change #1: TIME BEFORE: 108.603 TIME AFTER: 95.188 TIME REDUCTION FACTOR: 1.1409
# replaced references to "get_csv_rows(filename)" function calls to
# to references to global list variables so that get_csv_rows()
# is only run ONCE for each file that needs to be examined,
# rather than running each time the file contents need to be examined.
######

######
# Change #2 TIME BEFORE: 95.188 TIME AFTER: 29.465 TIME REDUCTION FACTOR: 3.2305
# Changed the import of get_words_from_string to the version
# in docdist_dict.py that uses the extend method rather than append.
######

######
# Change #3 TIME BEFORE: 29.465 TIME AFTER: 5.772 TIME REDUCTION FACTOR: 5.1048
# Changed the import of vecor_angle and count_frequency to the versions that
# use dictionaries in docdist_dict.py. I should have done this first.
######

###### (Change made on full file run)
# Change #4 TIME BEFORE: 124.907 TIME AFTER: 123.144 TIME REDUCTION FACTOR: 1.014
# Changed replace_target_with_blank to use a regex and re.sub() to replace the
# substring with XXXXX. I've only included this anectdote because it seemed noteworthy
# that it didn't really make a difference.
######


def main():
    # establishes that global variables declared outside of main() are available inside main()
    global MASTER_FILE, SENTENCE_DB_FILE
    global sentence_db_file_list, master_file_list

    # load SENTENCE_DB_FILE and MASTER_FILE into global list variables so that
    # they may be reused without having to call get_csv_rows more than necessary
    sentence_db_file_list = get_csv_rows(SENTENCE_DB_FILE)
    master_file_list = get_csv_rows(MASTER_FILE)


    # we will be collecting each row of the output file in this list
    output = []
    # a variable that counts the number of rows stored in "output" list is instatiated
    row_count = 0

    # looping through the SENTENCE_DB_FILE to process each row
    # loop through each item in the list returned from 'get_csv_rows' (see 'get_csv_rows' for explanation)
    for row in sentence_db_file_list:
        # the entire row from the list is passed to 'set_sentence_id' (see comments @ function definition)
        set_sentence_id(row)
        # the entire row from the list is passed to 'replace_target_with_blank()' (see comments @ function definition)
        replace_target_with_blank(row)
        # if set_sentence_id() failed to match a real sentence ID for this row,
        if row['SentID_GM'] != 'NA':
            # the row is passed to 'lookup_similar_row()' (see comments @ function definition)
            lookup_similar_id(row)
            # the row is passed to 'find_alternate_sentence()' (see comments @ function definition)
            find_alternate_sentence(row)
            # the row is passed to 'find_unique_targets()' (see comments @ function definition)
            find_unique_targets(row)
        # the row is appended to the list of 'output' rows
        output.append(row)
        # the 'row_count' accumulator variable is incremented by one
        row_count += 1
        # the new count of rows is printed to the terminal window
        print(row_count)
        # the 'output' list of rows is sent to the write_file_output() function
        write_output_file(output)

def set_sentence_id(row):
    '''
        If you look at the SENTENCE_DB_FILE, each row has a Sentence with a missing SentID_GM
        SentID_GM can be found in the MASTER_FILE
        So, we use the MASTER_FILE data to find SentID_GM for each Sentence

        # -------------------------------------------------------------------------
        # Implement a better way to "lookup" SentID_GM,
        # without looping through each row again and again
        #
        # Ask yourself:
        # -------------
        #   - Is "list" the best data structure for "lookup / search"?
        #   - What is the 'type' of running time for the current implementation?
        #     Is it linear or quadratic?
        #
        # -------------------------------------------------------------------------

    '''
    # loop through each item in the list returned from 'get_csv_rows' (see 'get_csv_rows' for explanation)
    for record in master_file_list:
        # record is a row in MASTER_FILE
        # this conditional block checks the value of ['Sentence_with_Target'] from ->
        # MASTER_FILE against the value of ['Sentence'] from the row that has been input
        if record['Sentence_with_Target'].strip() == row['Sentence'].strip():
            # found a matching sentence!
            # if a match is found, the value of ['SentID_GM'] in the input row is set->
            # to match the value of ['SentID_GM'] from MASTER_FILE
            row['SentID_GM'] = record['SentID_GM']
            break
            # if a match is not found for ['Sentence'] from MASTER_FILE,
        else:
            # the default value 'NA' is assigned to ['SentID_GM'] from the row->
            # that was passed to the function
            row['SentID_GM'] = 'NA'


def replace_target_with_blank(row):
    '''
        Each row in SENTENCE_DB_FILE has a "Target" word like "[education]".
        In this function, we replace the target word with "XXXXX", and
        store its value in "Sentence_With_Blank" column

        # -------------------------------------------------------------------------
        # Implement a better way to replace the Target word with XXXXX,
        # without looping through the words
        #
        # Ask yourself:
        # -------------
        #   - Is there an inbuilt python function,
        #     that can be used to substitute a word with another word?
        #
        # -------------------------------------------------------------------------

    '''
    # I tried using a regular expression here instead of looping and it made->
    # such a small difference that it's only worth noting because of how ineffective it was
    sentenceString = row['Sentence']
    re.sub("[\[](.*?)[\]]","XXXXX", sentenceString)
    row['Sentence_With_Blank'] = sentenceString

    #a list variable used to store words is instantiated
    # new_words = []
    #
    # # Here, we split the sentence into words and loop through it till we find the target
    # # String.split() method is invoked to split the ['Sentence'] string into a list of words
    # for word in row['Sentence'].split():
    #     # each word is tested to see if it begins with a square bracket->
    #     # and ends with a square bracket or a square bracket followed by a period ->
    #     # and if the string between the brackets is equivalent to the value of ->
    #     # the string ['Targ']
    #     if word[0]=='[' and (word[-1]==']' or word[-2:]=='].') and word[1:-1]==row['Targ']:
    #         # if those conditions are met, the word has been matched and 'XXXXX' is added->
    #         # to the new_words list
    #         new_words.append('XXXXX')
    #     else:
    #         # if those conditions are not met, the word is added to the new_word list,->
    #         # thus preserving the order of the words in the sentence
    #         new_words.append(word)
    # # the list of new words is then passed to the join() function ->
    # # where it is reassembled with spaced between the list items and ->
    # # stored back in the ['Sentence_With_Blank'] spot from whence it came.
    # row['Sentence_With_Blank'] = ' '.join(new_words)


def lookup_similar_id(row):
    '''
        The MASTER_FILE also has a column 'SimilarTo_SentID_GM',
        which is the sentence ID of a similar sentence in the MASTER_FILE.

        In this function, we lookup the similar sentence for the given 'row',
        using the data in the MASTER_FILE

        # -------------------------------------------------------------------------
        # Implement a better way to find similar sentence,
        # without looping through the each row again and again
        #
        # Ask yourself:
        # -------------
        #   - Is "list" the best data structure for "lookup / search"?
        #   - What is the 'type' of running time for the current implementation?
        #     Is it linear or quadratic?
        #   - Can I reuse something from a previous step?
        #
        # -------------------------------------------------------------------------

    '''

    similar_to = None
    # Here we get SimilarTo_SentID_GM for this row's SentID_GM using the MASTER_FILE
    # MASTER_FILE is passed to get_csv_rows()
    for record in master_file_list:
        # record is a row in MASTER_FILE
        # if 'SentID_GM' from the row that has been passed to this function->
        # matches 'SentID_GM' from a record in MASTER_FILE
        if record['SentID_GM'] == row['SentID_GM']:
            # found a match
            # the value of 'SimilarTo_SentID_GM' is stored in the variable 'similar_to'
            similar_to = record['SimilarTo_SentID_GM']
            break

    # then we find the similar sentence from the MASTER_FILE
    # if a value has been stored in 'similar_to'
    if similar_to is not None:
        # each record in MASTER_FILE is checked
        for record in master_file_list:
            # record is a row in MASTER_FILE
            # the 'SentID_GM' is matched to the value stored in 'similar_to'
            if record['SentID_GM'] == similar_to:
                # if a matching value is found, the value of 'Sentence_with_Target' ->
                # from MASTER_FILE is stored in the row at 'SimilarTo_Sentence'
                row['SimilarTo_Sentence'] = record['Sentence_with_Target']
                # the value of 'similar_to' is stored in row at 'SimilarTo_SentID_GM'
                row['SimilarTo_SentID_GM'] = similar_to
                break

def find_alternate_sentence(row):
    '''
        Just like SimilarTo_Sentence and SimilarTo_SentID_GM, we will determine
        Alternate_SimilarTo_Sentence and Alternate_SimilarTo_SentID_GM
        by calculating the cosine distance between two sentences
        using the **document distance** code that we discussed in the previous class

        # -------------------------------------------------------------------------
        # Your aim in this function is to speed up the code using a simple trick
        # and a modification
        #
        # Biggest hint: look at the other files in the folder
        #
        # Ask yourself:
        # -------------
        #   - Why are the functions called here, so slow?
        #   - Is there something you learned in the class about "document distance" problem,
        #     that can be used here?
        #   - Is there a step which can be taken out of the 'for' loop?
        #
        # -----
        # Bonus:
        # ------
        # This code calculates the cosine distance between the given row's Sentence
        # and the Sentence_with_Target all the rows in MASTER_FILE.
        # This is repeated for each 'row' in SENTENCE_DB_FILE.
        # In first iteration, you already calculate the cosine distance of
        # "I go to school because I want to get a good [education]."
        # and all the rows in the MASTER_FILE
        # and that includes "I go to school because I want to get a good [education]."
        # This is repeated in 2nd iteration for "I go to school because I want to get a good [education].".
        #
        # Can you cache (store) these calculations for future iterations?
        # What would be the best data structure for caching?
        # Try to further optimize the code using a cache
        # -------------------------------------------------------------------------

    '''

    # find alternate similar sentence using document distance
    # a variable is instantiated to store a dictionary->
    # with relevant similarity information
    similar_sentence = None
    # each record in MASTER_FILE is examined
    for record in master_file_list:
        # record is a row in MASTER_FILE
        # if the 'SentID_GM' from MASTER_FILE matches 'SentID_GM' from the input row,->
        # these sentences are the same and will be ignored
        if record['SentID_GM'] == row['SentID_GM']:
            # ignore the same sentence
            continue

        # get frequency mapping for row['Sentence']
        # the String value of 'Sentence' from the input row->
        # is passed to get_words_from_string(), which returns->
        # a list of words that is stored in row_word_list
        # see comments regarding get_words_from_string in docdist1.py
        row_word_list = get_words_from_string(row['Sentence'])
        # the list of words returned from get_words_from_string->
        # is passed to the count_frequency() function, the->
        # results of which are stored in the variable, 'row_freq_mapping'
        # see comments regarding count_frequency in docdist1.py
        row_freq_mapping = count_frequency(row_word_list)

        # get frequency mapping for record['Sentence_with_Target']
        # the String value of 'Sentence_with_Target' from the MASTER_FILE->
        # is passed to get_words_from_string(), which returns->
        # a list of words that is stored in record_word_list
        # see comments regarding get_words_from_string in docdist1.py
        record_word_list = get_words_from_string(record['Sentence_with_Target'])

        # the list of words returned from get_words_from_string->
        # is passed to the count_frequency() function, the->
        # results of which are stored in the variable, 'record_freq_mapping'
        # see comments regarding count_frequency in docdist1.py
        record_freq_mapping = count_frequency(record_word_list)
        # the lists stored in 'row_freq_mapping' and 'record_freq_mapping'->
        # are passed to vector_angle(), the result of which is stored->
        # in the variable, distance, as a float
        # im not commenting in docdist_dict.py because I have->
        # not been instructed to include docdist_dict.py
        distance = vector_angle(row_freq_mapping, record_freq_mapping)
        # if the document distance (the measure of similarity) is->
        # between 0 and .75
        if 0 < distance < 0.75:
            # if there isn't a value stored in similar_sentence OR->
            # the value of 'distance' is less than the value stored at->
            # 'distance' in the 'similar_sentence' dictionary
            if (not similar_sentence) or (distance < similar_sentence['distance']):
                # then the similarity is great enough to store the value of distance->
                # (the measure of that sentences similarity), the sentence with which->
                # it shares similarity, and the 'SentID_GM' of the sentence with which->
                # it shares similarity in a dictionary stored in the variable, 'similar_sentence'
                similar_sentence = {
                    'distance': distance,
                    'Sentence_with_Target': record['Sentence_with_Target'],
                    'SentID_GM': record['SentID_GM']
                }
    # if the value of ['SentID_GM'] from similar_sentence is not equivalent to 'SimilarTo_SentID_GM'->
    # from the row being examined,
    if similar_sentence and similar_sentence['SentID_GM'] != row.get('SimilarTo_SentID_GM'):
        # the value of 'SentID_GM' from 'similar_sentence' is stored in->
        # 'Alternate_SimilarTo_SentID_GM' from the input row
        row['Alternate_SimilarTo_SentID_GM']  = similar_sentence['SentID_GM']
        # the value of 'Sentence_with_Target' from 'similar_sentence' is stored in->
        # 'Alternat_similarTo_Sentence' from the input row
        row['Alternate_SimilarTo_Sentence']  = similar_sentence['Sentence_with_Target']


def find_unique_targets(row):
    '''
        This steps finds [target] word in "SimilarTo_Sentence" and "Alternate_SimilarTo_Sentence",
        selects only unique target word(s), and saves it in `row['SimilarTo_Targets']`

        # -------------------------------------------------------------------------
        # Implement a better way to find unique target words,
        # without looping through the words
        #
        # Ask yourself:
        # -------------
        #   - Can you use regular expressions to do this?
        #   - What is the data structure that stores only unique values?
        #     Can it be used here instead of checking "if target not in targets:"?
        #     Try searching the web for "python get unique values from a list".
        #
        # -------------------------------------------------------------------------

    '''

    # find unique targets from similar sentences
    # a variable, called 'targets', storing an empty list is instantiated
    targets = []
    # 'SimilarTo_Sentence' and 'Alternate_SimilarTo_Sentence' are looped through
    for key in ('SimilarTo_Sentence', 'Alternate_SimilarTo_Sentence'):
        # each word is looped through
        for word in row.get(key, '').split():
            # if the word is enclosed by square brackets,
            if word.startswith('[') and word.endswith(']'):
                # the word, minus the square brackets, is stored in the variable, 'target'
                target = word[1:-1]
                # if that word is not already in the list of target words, 'targets,'
                if target not in targets:
                    # the word is added to targets
                    targets += [target]
            # the same action described above is taken if the target word's->
            # trailing square bracket is followed by a period
            elif word.startswith('[') and word.endswith('].'):
                target = word[1:-2]
                if target not in targets:
                    targets += [target]
    # the list of target words, 'targets,' is joined by commas and stored->
    # in the input row at 'SimilarTo_Targets'
    row['SimilarTo_Targets'] = ','.join(targets)


def get_csv_rows(filename):
    '''Read the CSV file using DictReader and then append all rows in a list'''
    # opens the file passed to the function in 'read' mode and specifies that new lines - >
    # are delineated by a blank space.
    # That open file is aliased as "input_file"
    with open(filename, 'r', newline='') as input_file:
        # a DictReader object that of input_file, delimited by a comma with double ->
        # quotes escaped is stored in the variable, "reader"
        reader = csv.DictReader(input_file, delimiter=',', quotechar='"')

        # an empty list called "data" is instatiated
        data = []
        # each row in the reader object is examined
        for row in reader:
            # and appended to the "data" list
            data.append(row)
        # the list, "data", that includes each row in "reader" is returned
        return data


def write_output_file(output):
    '''Write output into a new CSV file. Uses the OUTPUT_FILE variable to determine the filename.'''
    global OUTPUT_FILE
    # the function opens the file stored in the global variable, OUTPUT_FILE,->
    # with 'write' as a parameter and aliases it as 'output_file_obj'
    with open(OUTPUT_FILE, 'w', newline='') as output_file_obj:
        # a new DictWriter object is created specifying field names for the output file
        # it will ignore extra input and delimit the output file with commas and use
        # double quotes for quotes
        sentence_db_writer = csv.DictWriter(output_file_obj,
                                fieldnames=["SentID_GM", "Sentence", "Targ", "Sentence_With_Blank",
                                        "SimilarTo_Sentence", "SimilarTo_SentID_GM",
                                        "Alternate_SimilarTo_Sentence", "Alternate_SimilarTo_SentID_GM",
                                        "SimilarTo_Targets"],
                                extrasaction="ignore", delimiter=",", quotechar='"')
        # The header row is written
        sentence_db_writer.writeheader()
        # each row in the output list is looped through and the row is written to the output file
        for row in output:
            sentence_db_writer.writerow(row)


if __name__ == '__main__':
    profile.run('main()')
    # main()
