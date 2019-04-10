SciHub
======

|Python| |Build Status| |Pypi|

``scihub`` is an unofficial API for sci-hub.cc.
``scihub`` can download papers from ``sci-hub``.

If you believe in open access to scientific papers, please donate to
Sci-Hub.

Setup
-----

::

    pip install scihub

Usage
-----

fetch
~~~~~

.. code:: python

    from scihub import SciHub

    sh = SciHub()

    # fetch specific article (don't download to disk)
    # this will return a namedtuple of the form
    # result.pdf => PDF_DATA
    # result.url => SOURCE_URL
    # result.doi => PARSED_DOI
    result = sh.fetch('http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=1648853')

    if result:
      with open('output.pdf', 'wb+') as fd:
          fd.write(result.pdf)

License
-------

MIT

.. |Python| image:: https://img.shields.io/badge/Python-3%2B-blue.svg
   :target: https://www.python.org
.. |Build Status| image:: https://travis-ci.org/alejandrogallo/python-scihub.svg?branch=master
   :target: https://travis-ci.org/alejandrogallo/python-scihub
.. |Pypi| image:: https://badge.fury.io/py/scihub.svg
   :target: https://badge.fury.io/py/scihub
