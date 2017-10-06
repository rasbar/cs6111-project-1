# Query Augmentation Using Relevance Data
### Project 1 Group 33
Parth Panchmatia, psp2137
Rashad Barghouti, rb3074

## Files submitted
group33-proj1.zip contains:
- README
- proj1-stop.txt
- query.py
- transcript.txt

## Internal Design
- **main** function receives command line args and calls start
- **getStopWords** reads stop words from the proj1-stop.txt file
- **start** creates the custom search engine and then executes the uery
- **displayRes** then displays the result and asks for user feedback
- **evaluate** method decides whether to update the query or not on basis of the feedback
- **updateQuery** function adds the new words to the query and calls start again
- **createVectors** method simply creates vectors in the form of a dict with word count using the relevant and not relevant search results
- in **rocchio** method we generate the new vector on take the top 2 results which are augmented into the query

## Query modification method
- We generate two lists, both comprising of title and summary from the search results, one of the relevant and other of the non relevant results
- We use nltk to tokenize each entry in the list so that we break the sentence down to a list of words split appropriately without punctuations
- We then create a dict of words and their count for the relevant document and not relevant document set. While inserting into the dict we ensure that it is not a stop word, convert the words to lowercase and also lemmatize them so that we can get correct word counts for scenarios when a word is plural/singular and capitalized/lower case.
- We then multiply the value of these vectors with an appropriate constant (beta/gamma) and divide by the document count(relevant/ not relevant)
- We take a difference of these two vectors and obtain a new vector closer to the input query. We take the top 2 results of this vector (which are not already present in the query) and augment the query with the result.

## Key and Id
- api Key:      AIzaSyCqDEnJkCFVYJ2aF94ntsuEwUu1ofZRTLs
- engine Id:    009287071471840412963:zpb5-fjffom

## How to run

The project's implementation has a dependency on Python 3 and associated
packages. All, along with instructions for installation on the Google VM, are
listed in the next section. 

To run the program, uncompress the file `group33-proj1.zip` inside a working
directory on the VM.

Inside the project's directory, the project's python module can be run as 
follows: (Please install dependencies before that)

```bash
$ python3 query.py <google api key> <google engine id> <precision> <query>
```

## Dependencies
*   **Python3**. Should be already installed on the VM as part of the Ubuntu
    image. To check, run the following command

    ```bash
    which python3       
    ```
    On an Ubuntu 14.04 VM, this should return something like
    `/usr/bin/python3`. If not installed, the following will install Python
    3.6:

    ```bash
    sudo add-apt-repository ppa:jonathonf/python-3.6
    sudo apt-get update
    sudo apt-get install python3.6
    ```

*   **Update apt-get**. To install this toolkit, run the following command in a terminal
    window:
    
    ```bash
    sudo apt-get update
    ```

*   **pip for Python3**. To install this toolkit, run the following command in a terminal
    window:
    
    ```bash
    sudo apt-get install python3-pip
    ```

*   **NLTK**. To install this toolkit, run the following command in a terminal
    window:

    ```bash
    $ sudo -H pip3 install -U nltk 
    ```

*   **Google API Python Client for Python3**. To install this toolkit, run the following command in a terminal
    window:
    
    ```bash
    sudo -H pip3 install --upgrade google-api-python-client
    ```

*   **wordnet**. To install this toolkit, run the following command in a terminal
    window:

    ```bash
    $ python3
    >>> import nltk
    >>> nltk.download('wordnet')
    ```
