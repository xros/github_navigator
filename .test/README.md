How is this built?
=====================

* GitHub navigator

The file `application.py` is the main application. File `.test/results.txt` is the output of the var `results` in `application.py`.

The file `.test/save.json` is the direct json gotten from GitHub API v3 by requesting: https://api.github.com/search/repositories?q=arrow&order=desc

The file `.test/sort.py` is an Insertion Sorting Algorithm Implementation in Python which would sort a list of dict by the value of **created_at**

The file `.test/sorted.json` is sorted by `sort.py` from `save.json`.

The file `.test/search.json` is a search result using GitHub API v3 which looks pretty and convenient for coding
