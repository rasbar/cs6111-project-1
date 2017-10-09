## Project 1 Group 33
Rashad Barghouti (rb3074)  
Parth Panchmatia (psp2137)

### Project Files
*   `rfquery.py`— a Python 3 implementation of query expansion using explicit
    relevance feedback(& executable) file
*   `README.md`: — this readme file
*   `stopwords.txt` — A minimal stop-words list from link provided in assignment
    file
*   `keys` — a file containing Google's API key and CSE id. *Can be used in the
    program's command-line invocation* 

### Dependencies

The following are the packages needed to run the submitted `rfquery.py`
implementation. The installation instructions on an Ubuntu VM are
shown.

*   **Python3**

    Python 3 should be already part of the Ubuntu VM. To check run

    ```bash
    $ which python3       
    ```

    On Ubuntu 14.04 VM, this above command should return something like
    `/usr/bin/python3`. Nonetheless, to install or upgrade Python 3, the following
    sequence will put Python 3.6 on the system:

    ```bash
    sudo add-apt-repository ppa:jonathonf/python-3.6
    sudo apt-get update
    sudo apt-get install python3.6
    ```

*   **NumPy and SciPy**

    Python 3 versions of both can be installed/upgraded with python's `pip` command
    as follows:

    *   First upgrade `pip3` on the VM with:
        
        ```bash
        sudo -H pip3 install --upgrade pip
        ```

    *   To do a user-only installation, run:

        ```bash
        pip3 install --user numpy scipy
        # may need to add /home/<username>/.local/bin to PATH
        ```

    *   To install on the VM for all users, run

        ```bash
        sudo -H pip3 install numpy scipy

        # /home/<username>/.local/bin may need to be added to PATH after running
        # the above command 
        ```

*   **scikit-learn**

    To install, run

    ```bash
    sudo -H pip3 install -U scikit-learn
    ```

*   **Google API Python Client** for Python3

    `pip3` can be used as above:

    ```bash
    sudo -H pip3 install --upgrade google-api-python-client
    ```

### Running the Program

The Google API key and the custom search engine's id are:

**API key**: AIzaSyAlKLHe1eAmug6XeTlQ1DxzOsPI4zax7Ms  
**CSE ID**: 006096712590953604068:qoxtr78cjow

To run the implementation, the following steps can be used: 

*   In a directory on the VM, uncompress the `group33-proj1.tar.gz` file

    ```bash
    $ tar xvf group33-proj1.tar.gz
    ```

*   Invoke `rfquery.py`. The program comes with a simple command parser and a
    `-h | --help` option that displays usage info.

    First, it is probably a good idea to ensure the executable bits for the
    program are turned on. This can be done with this command:

    ```bash
    $ chomd +x rfquery.py
    ```
    Then, use either one of the following commands to run the program:

    ```bash
    $ rfquery.py <google api key> <cse id> <precision@10> <query>
    ```
    or
    ```bash
    $ rfquery.py @keys <precision@10> <query>
    ```
    The `keys` file contains the needed keys and is provided to simplify the
    command syntax.

### Code Design and the Query Augmentation Algorithm

The code has the following structure and sequence of operation:

1. `parse_cmdline()` — A simple parser that processes and validates the
   command-line arguments.
2. Data structure initializations in `main()` that set up an internal data
   structure and the
   search engine's service object
3. `process_query()` — a routine that (1) performs the initial Google search,
   (2) collects the relevance feedback from the user, and (3) computes the
   precision@10 value from the feedback data.
   Search results/items selected as relevant by the user are returned to the
   main program for the query expansion computations. Non-relevant data are not
   used.
4. `main()` — the main program component that performs the query expansion.

*The algorithm* for the query augmentation can be summarized as follows:
  
*   Vectorize the input text data to build a document-term matrix (index)
*   Aggregate the term-frequencies for each term in the index
*   Construct a list of (term, term_aggregate_frequency) tuples.
*   Sort the list in descending order on its aggregate frequency values 
*   Chose a maximum of 2 terms from the top of the list to augment the query.

#### Some Details

*   `title` and `snippet` data from relevant search results were used to
    construct each document's text. The two strings were concatenated
*   Two vectorization techniques were tried and compared: (1) term-frequency
    (tf) vectorization and (2) tfidf vectorization. Both were applied with
    stop-word elimination using the minimal list pointed to in the assignment document.
*   No other input pre-processing (e.g., stemming) was used.

The vectorizers are from [sklearn's text feature extraction
package](http://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction),
and both performed identically. The reasons for the lack of distinction between
them are a combination of: (1) the (very) small size of the input document set
and the lengths of the corresponding vectors, and (2) the short lengths of the
queries (two of which are single-word terms). The first factor made
document-frequency analysis and log-scaling not needed, because the index did
not have any high-frequency terms that could obscure the presence of important
rare terms. The second factor (the single-word queries) rendered document
frequency scaling neutral. In the end, term-frequencies were sufficient to
produce the high precision needed. 

Since idf scaling had no effect, stop-words removal was important to remove
high-frequency words. A side effect of this was the loss of 'per' from the 'per
se' query string. This, however, had no effect, since 'per' remained in the
original query string, which was appended with the augmentation terms.
