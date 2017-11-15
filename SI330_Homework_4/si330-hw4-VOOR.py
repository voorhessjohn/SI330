###############
# HOMEWORK FOUR
# John Voorhess
# SI330 Fall 2017
# Dr. Teplovs
###############



# -*- coding: utf-8 -*-
#!/usr/bin/python -tt
import re
import csv
from collections import defaultdict


def write_log_entries(filename, list_of_rows_to_write):
    row_counter = 0
    with open(filename, 'w+', newline = '') as f:
        row_writer = csv.DictWriter(f, delimiter='\t', quotechar='"', extrasaction='ignore',
                                    # Changed one of the field names to "URL" to match the output file
                                    fieldnames=["IP", "Ignore1", "Ignore2", "Timestamp", "Ignore3", "HTTP_Verb",
                                                "HTTP_Status", "HTTP_Duration", "HTTP_Redirect", "Browser_Type",
                                                "Top_Level_Domain"])
        row_writer.writeheader()
        for row in list_of_rows_to_write:
            row_writer.writerow(row)
            row_counter = row_counter + 1

    print("Wrote {} rows to {}".format(row_counter, filename))

# Function get_top-level_domain:
#    Input:  A string containing a URL
#    Output:  the top-level domain in the URL, or None if no valid top-level domain was found.  The top-level
#             domain, if it exists, should be normalized to always be in lower case.

def get_toplevel_domain(url):

    # the following regex return a match group where group[1] = HTTP verb and group[2] is TLD (top level domain)

    # it goes like this:
    # match a string that begins with either GET or POST,
    # followed by some amount of whitespace,
    # followed by http, followed by 0 or more 's',
    # followed by '://'
    # followed by one or more upper or lowercase letters,
    # followed by zero or more uppercase letters, lowercase letters, digits, dots, or dashes,
    # followed by a dot,
    # followed by one to three upper or lowercase letters,
    # followed by a forward slash OR whitespace OR a colon
    tld = re.search('(GET|POST)(?:\shttp[s]*:\/\/[A-Za-z]+[a-zA-Z0-9\.\-]*)(?:\.)([a-zA-Z]{1,4})(?:\/+|\s|:)', url, re.IGNORECASE)

    return tld

# Function read_log_file:
#   Input: the file name of the log file to process
#   Output:  A two-element tuple with element 0 a list of valid rows, and element 1 a list of invalid rows
def read_log_file(filename):
    valid_entries   = []
    invalid_entries = []

    with open(filename, 'r', newline='') as input_file:
        log_data_reader = csv.DictReader(input_file, delimiter='\t', quotechar ='"', skipinitialspace=True,
                                         fieldnames=["IP","Ignore1","Ignore2","Timestamp","Ignore3","HTTP_Verb","HTTP_Status","HTTP_Duration","HTTP_Redirect","Browser_Type",])
        for row in log_data_reader:
            # ['HTTP_Verb'] contains the verb as well as the address, so we send this to get_toplevel_domain()
            # which splits it into the verb and the top level domain.
            tld = get_toplevel_domain(row['HTTP_Verb'])
            # if top_level_domain() regex does not return a match (the criteria for a match are related to
            # the criteria for a valid entry) OR if the http status from the row is anything other than '200'...
            if tld==None or not row['HTTP_Status'] == '200':
                # ...then not_a_valid_line boolean flag is set to TRUE
                not_a_valid_line = True

            else:
                # is a match is found and the status is 200, the the boolean flag is set to False
                not_a_valid_line = False


            #1. The HTTP verb is GET or POST

            #2. AND the status code is 200

            #3. AND the URL being accessed starts with http:// or https://,
            # followed by one or more alphabetic characters (i.e. not a digit or a symbol).
            # For example, the URL should NOT start with 'http:///', which is an error.

            #4. AND the top-level domain consists of only letters.
            # This is to say, if the host name is actually a numerical IP address
            # like '202.96.254.200', we don’t count it.
            # If the whole domain name is just '.com' as in http://.com/blah or
            # does not even contain a dot as in http://c/blah, we do not count it.




            if not_a_valid_line:

                # invalid lines are added to the list of invalid rows
                if not tld==None:
                    topLevelDomain = tld[2]
                    row['Top_Level_Domain'] = topLevelDomain.lower()
                ###############
                # I don't know why I had to do this, but without it I had a tuple in the row dictionary
                # consisting of a nonetype object as element 0 and a list of 10-ish empty strings in position 1
                # I may ask you about this.
                ###############
                del row[None]
                invalid_entries.append(row)
                continue

            # if we get here, it's a valid line
            # tld match group 2 is assigned to a string variable
            topLevelDomain = tld[2]
            # the string variable holding the top level domain is assigned as a
            # value in the row dictionary whose key is 'Top_Level_Domain'
            row['Top_Level_Domain'] = topLevelDomain.lower()

            ###############
            # I don't know why I had to do this, but without it I had a tuple in the row dictionary
            # consisting of a nonetype object as element 0 and a list of 10-ish empty strings in position 1
            # I may ask you about this.
            ###############
            del row[None]


            valid_entries.append(row)


    return (valid_entries, invalid_entries)

def main():
    #valid_rows, invalid_rows = read_log_file(r'access_log_first_1000_lines.txt')
    valid_rows, invalid_rows = read_log_file(r'access_log.txt')
    write_log_entries('valid_access_log_VOOR.txt', valid_rows)
    write_log_entries('invalid_access_log_VOOR.txt', invalid_rows)

    ##############
    # SUBMISSION NOTE:
    #
    #
    # The files are the same when compared with the first 1000 examples.
    # However, DiffMerge crashes when I load the full comparison file, 'valid_access_log_YOURUNIQUENAME.txt'
    # Valid_access_log is positive by 3 rows, invalid_access_log is negative by 3 rows.
    # I have tried making the regex more strict, but haven't come up with a method that
    # remedies the discrepancy.
    ##############

# This is boilerplate python code: it tells the interpreter to execute main() only
# if this module is being run as the main script by the interpreter, and
# not being imported as a module.
if __name__ == '__main__':
    main()

