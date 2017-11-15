import petl as etl
import sqlite3

##################################
# John Voorhess SI330 Homework 5 #
##################################

# Open a connection to the database
conn = sqlite3.connect('goodbooks.db')


# create petl objects for the contents of each of the csv files
ratings = etl.fromcsv('ratings.csv')
to_read = etl.fromcsv('to_read.csv')
tags = etl.fromcsv('tags.csv')
books = etl.fromcsv('books.csv')
book_tags = etl.fromcsv('book_tags.csv')

# print the top of each petl object to verify contents
print(ratings.head())
print(to_read.head())
print(tags.head())
print(books.head())
print(book_tags.head())

# store sql statement to create tags table with unique integer primary key in a variable
createTags = """
CREATE TABLE IF NOT EXISTS tags (
tag_id int primary key not null,
tag_name char(50)
)
"""

# store sql statement to create ratings table with user_id, book_id, and rating - book_id references books.book_id
createRatings = """
CREATE TABLE IF NOT EXISTS ratings (
user_id int, 
book_id int,
rating int,
FOREIGN KEY (book_id) REFERENCES books (book_id)
)
"""

# store sql statement to create to_read table with user_id and book_id referencing books.book_id
createTo_Read = """
CREATE TABLE IF NOT EXISTS to_read (
user_id int,
book_id int,
FOREIGN KEY (book_id) REFERENCES books (book_id)
)
"""

# store sql statement to create books table with all fields from csv - no foreign keys
createBooks = """
CREATE TABLE IF NOT EXISTS books (
book_id int primary key not null,
goodreads_book_id int,
best_book_id int,
work_id int,
books_count int,
isbn int,
isbn13 int,
authors varchar(255),
original_publication_year float,
original_title varchar(255),
title varchar(255),
language_code char(50),
average_rating float,
ratings_count int,
work_ratings_count int,
work_text_reviews_count int,
ratings_1 int,
ratings_2 int,
ratings_3 int,
ratings_4 int,
ratings_5 int,
image_url varchar(255),
small_image_url varchar(255)
)
"""

# store sql statement to create tags table with book_id, tag_id, and count
createBook_Tags = """
CREATE TABLE IF NOT EXISTS book_tags (
goodreads_book_id int,
tag_id int,
count int
)

"""

# store sql statement to create author_book association table to establish many-to-many relationship
# between author and book tables.
createAuthor_Book = """
CREATE TABLE IF NOT EXISTS author_book (
author_id int,
book_id int,
FOREIGN KEY (book_id) REFERENCES books (book_id),
FOREIGN KEY (author_id) REFERENCES author (ROWID)
)
"""

# store sql statement to create author table with unique rowid (by default) and author name
createAuthor = """
CREATE TABLE IF NOT EXISTS author (
author_name varchar(255) not null
)
"""


# list of table names for looping
tableNames = ['ratings', 'tags', 'to_read', 'books', 'book_tags', 'author_book', 'author']

# before creating the tables, they must be dropped if they already exist
for table in tableNames:
    conn.execute("DROP TABLE IF EXISTS "+table+";")

# list of create statements for looping
createList = [createRatings, createTags, createTo_Read, createBooks, createBook_Tags, createAuthor_Book, createAuthor]
# loop through all create statements and create all tables
for command in createList:
    conn.execute(command)

# create all tables from previously instantiated petl objects
ratings.todb(conn,'ratings')
tags.todb(conn,'tags')
to_read.todb(conn,'to_read')
books.todb(conn,'books')
book_tags.todb(conn,'book_tags')


# select the list of authors and the book_id from books
b = conn.execute('select authors, book_id from books')
# store the result of the query
authorsBookList = b.fetchall()
# create an empty list to store the authors
everyAuthor = []
# loop through the results of the query
for authorBook in authorsBookList:
    # store the book_id in a variable
    bookID = authorBook[-1]
    # store the string of authors in a variable
    authorString = str(authorBook[0])
    # store the list of authors split at ',' in a list variable
    authorSplit = authorString.split(',')
    # loop through the list of authors
    for authorName in authorSplit:
        # create a tuple with the author name and the book id
        authorNameBookIDTuple = (authorName.strip(),bookID)
        # store that tuple in a list of tuples
        everyAuthor.append(authorNameBookIDTuple)

# loop through the list of (author, book) tuples
for eachTuple in everyAuthor:
    # insert the author_name into the author table
    conn.execute('INSERT INTO author (author_name) VALUES ("'+eachTuple[0]+'");')

# loop through the list of (author, book) tuples
for eachTuple in everyAuthor:
    # insert author_id and book_id into author book by matching the names against the names in the author table to return author_id
    conn.execute('INSERT INTO author_book (book_id, author_id) SELECT '+str(eachTuple[-1])+', ROWID FROM author WHERE author_name LIKE "'+eachTuple[0]+'";')

# loop through the tables, count the rows, and print the number for verification
for table in tableNames:
    r = conn.execute('select count(*) from '+ table)
    rowcount = r.fetchone()[0]
    print(str(rowcount) + ' rows in ' + table + ' table')

print("*************************************")
print("")

######################################################
# 1.) What are the top 10 most highly-rated authors? #
######################################################
# Authors of books with largest proportion of 5-star rating? (ratings_5/work_ratings_count)

# Select the bookID and title from books ordered by the proportion of 5-star ratings to total ratings.
questionOneQuery = conn.execute("SELECT book_id, title FROM books ORDER BY CAST(ratings_5 as FLOAT) / CAST(work_ratings_count as FLOAT) desc LIMIT 50")
# assign the query result to a variable
queryOne = questionOneQuery.fetchall()

# create a list to store authors
authorList = []
# loop through the query results
for row in queryOne:
    # get the author name for each bookID returned from the previous query
    authorNameQuery = conn.execute("SELECT author.author_name FROM author INNER JOIN author_book ON author.ROWID=author_book.author_id WHERE author_book.book_id='"+str(row[0])+"';")
    # assign results to a variable
    queryTwo = authorNameQuery.fetchone()
    # add the author name if it is not already in the authorList. This keeps the names distinct
    if queryTwo[0] not in authorList:
        authorList.append(queryTwo[0])
    else:
        pass
print("************************************************************************************************")
print("The authors of books whose ratings have the highest proportion of 5-star reviews are as follows:")
print("************************************************************************************************")

# print the author names
for i in range(10):
    print(authorList[i])


#########################################################################
# What are the top 10 most popular authors on peoples’ “to-read” lists? #
#########################################################################


# this is a select from a subquery.
# the subquery selects book_ids from the to_read table ordered by the incidence of the book_id, descending, limited to the top ten results.
# the second part of the query selects a distinct set of author names where the book id exists in the subquery results.
questionTwoQuery = conn.execute("SELECT DISTINCT author.author_name FROM author INNER JOIN author_book ON author.ROWID=author_book.author_id INNER JOIN books on author_book.book_id=books.book_id WHERE books.book_id IN (SELECT to_read.book_id FROM to_read GROUP BY to_read.book_id ORDER BY count(*) desc LIMIT 10) LIMIT 10;")
# assign the result to a variable
queryThree = questionTwoQuery.fetchall()

print("*********************************************************************")
print("The top ten most popular authors on peoples' \"to-read\" lists are:")
print("*********************************************************************")
# loop through the results and print the answer
for item in queryThree:
    print(item[0])

###############################################################
# Who are the authors of the most tagged books on Good Reads? #
###############################################################


# this query is slightly modified from the #2 query since the structure of the solution is similar, but addresses different tables
questionThreeQuery = conn.execute("SELECT DISTINCT author.author_name FROM author INNER JOIN author_book ON author.ROWID=author_book.author_id INNER JOIN books on author_book.book_id=books.book_id WHERE books.book_id IN (SELECT book_tags.goodreads_book_id FROM book_tags GROUP BY book_tags.goodreads_book_id ORDER BY count(*) desc LIMIT 10) LIMIT 10;")
queryFour = questionThreeQuery.fetchall()

print("*************************************************")
print("The authors of the top ten most tagged books are:")
print("*************************************************")

for item in queryFour:
    print(item[0])


conn.commit()
conn.close()

