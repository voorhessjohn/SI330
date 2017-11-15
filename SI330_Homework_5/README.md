**Homework 5**
SI330
John Voorhess 
voor@umich.edu

The Python file, homework5.py, creates a sqlite database from several csv files and generates two additional tables, `author` and `author_book` for normalization and to enforce a many-to-many relationship between authors and books in the database.

The row counts of the tables are printed as verification and queries are run to answer the following questions:

**"What are the top 10 most highly-rated authors?"**
I have chosen to interpret this question as:
*who are the authors of the books that have the highest proportion of 5-star votes to overall number of votes?*
![highratedimage](https://i.imgur.com/C7eE5TE.png)

**"What are the top 10 most popular authors on peoples’ “to-read” lists?"**
I have interpreted this question as:
*who are the authors of the books that appear most frequently in the `to_read` table?*
![toreadauthors](https://i.imgur.com/kNZMcBZ.png)

**"What are the authors of the top ten most tagged books?"**
Interpreted as:
*who are the authors of the books that appear most frequently in the `tags` table?*
![tagged](https://i.imgur.com/Udu7vxV.png)

The answers to these questions are printed to the console.
Please see comments in homework5.py for specific technical details.