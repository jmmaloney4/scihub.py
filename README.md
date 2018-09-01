scihub.py
[![Python](https://img.shields.io/badge/Python-3%2B-blue.svg)](https://www.python.org)
[![Build Status](https://travis-ci.org/alejandrogallo/python-scihub.svg?branch=master)](https://travis-ci.org/alejandrogallo/python-scihub)
=========

`scihub` is an unofficial API for sci-hub.cc. scihub.py can download papers
from `sci-hub`.

If you believe in open access to scientific papers, please donate to Sci-Hub.

Setup
-----
```
pip install scihub
```

Usage
------

### fetch

```
from scihub import SciHub

sh = SciHub()

# fetch specific article (don't download to disk)
# this will return a dictionary in the form 
# {'pdf': PDF_DATA,
#  'url': SOURCE_URL
# }
result = sh.fetch('http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=1648853')
```

License
-------
MIT










