# Search Engine

We have also included the documentation as a pdf if you want to understand how our project works

## Tools used

- python
- you will need Python 3.10 or above to run it
- you will need to download nltk library package
- you can do so by executing the following command
  `pip install nltk` in the terminal,
- you may need to upgrade pip, you can do so by executing
  `pip install --upgrade pip` in the terminal

After installation of nltk you will have to download stopwords
you can do so by running downloadStopWords.py in the projectDirectory

## Running the Code

There are 2 things that you can do to test the code:

1. Test it using the GUI, run main.py and click on
   insert data, there you can choose the folder which contains the dataset
   in our case it is in'./newsdata' and after the indexing is completed you can use the GUI to search

2. You can run test.py and it will automatically generate the inverted index and fwd index in the path described above
   and then you can use the GUI to search

The project directory contains:

- `./newsData` (contains a part of the dataset, we used the NELA-GT-2020 news data)
- `./forwardBarrels` (contains all the forward Barrels)
- `./InvertedBarrels` (contains all the inverted Barrels)
- `./document_index.txt` (will be created after creation of index, is used to store the document index and the url of the article)
- `./lexicon.txt` (will be created after the creation of index, stored the word, the wordID and the pointer into the invertedBarrel)
- `./indexer.py` (is used to generate the forwardIndex, contains a function, if you pass the path of the data to the function it generates the fwd index of the json data at that path)
- `./main.py` (contains the GUI and related function)
- `./searcher.py` (contains the searching function which calculates the rank of each document)
- `./sorter.py` (creates the inverted index, by sorting each forward barrel)
- `./test.py` (contains the testing part in case you choose option 2)
- `./tkHyperLinkManager.py` (is used to display hyperLinks in the GUI)
- `./downloadStopWords.py` (downloads the stopwords in nltk)
- `./README.md` (ignore, its used for git)

## Optimizations that can be made

Currently when we insert new Data we are resorting all the inverted barrels which takes a lot of time a simple optimization can be made, since we know that the current data in the inverted index is sorted we can just load that data in a counting sort format and load the rest of the data from the corresponding forward barrel and just append it at its respective index, we can also check if a forward barrel's size is 0kb then we dont need to update the corresponding inverted index at all

## Average search time

Average search time for single word query is between 0.02 - 0.1 seconds
Average search time for multi-word queries is between 0.2 - 0.8 seconds

Happy searching!
