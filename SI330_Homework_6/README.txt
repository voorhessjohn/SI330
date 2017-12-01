**Homework 6**
SI330
John Voorhess 
voor@umich.edu

In order to find the 50 most frequent bigrams in Victor Hugo's Les Miserables, the text file must be rid of non-artistic text. This is done manually as it takes very little time and does not warrant it's own code. The resulting text is stored in a file called, "lesmis.txt."

The Python file, JohnVoorhessHomework6PreProcessing.py, takes in a file called, "lesmis.txt," which is a traditionally-wrapped text file-- , uses the natural language toolkit, and outputs a file called,"lesmissentences.txt," which is formatted so that each line contains one and only one sentence.

The file, "lesmissentences.txt," can then be sent to mrjobs.py which outputs a list of bigrams, sorted in descending order by frequency of appearance. This is acheived by processing each line of the txt file and assembling bigrams, outputting those to a reducer function that sums the occurences of each bigram, and sending that output to a reducer function that swaps the yield values so that the output is sorted by the sum of occurences, rather than the bigram, itself.

Please see JohnVoorhessHomework6PreProcessing.py and mrjobs.py for more specific technical comments.

**"What are the top 50 most frequently appearing bigrams?"**
["jean", "valjean"]
["old", "man"]
["good", "god"]
["thousand", "francs"]
["said", "marius"]
["le", "maire"]
["hundred", "francs"]
["said", "gavroche"]
["every", "day"]
["every", "one"]
["great", "deal"]
["young", "man"]
["father", "madeleine"]
["human", "race"]
["one", "would"]
["reverend", "mother"]
["young", "girl"]
["homme", "arm\u00e9"]
["louis", "xviii"]
["madame", "th\u00e9nardier"]
["wine", "shop"]
["said", "enjolras"]
["years", "old"]
["grave", "digger"]
["etc", "etc"]
["little", "girl"]
["low", "voice"]
["old", "woman"]
["taken", "place"]
["caught", "sight"]
["let", "us"]
["rue", "plumet"]
["three", "days"]
["turned", "round"]
["door", "opened"]
["good", "man"]
["little", "one"]
["first", "floor"]
["five", "francs"]
["long", "live"]
["long", "time"]
["mon", "dieu"]
["old", "fellow"]
["said", "courfeyrac"]
["years", "ago"]
["chimney", "piece"]
["du", "calvaire"]
["first", "place"]
["grape", "shot"]
["honest", "man"]

**Sample terminal output:**
![sample terminal output](http://www.johnvoorhess.com/bigrams.png)