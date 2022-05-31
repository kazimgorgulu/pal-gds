How to Use
==========

.. toctree::
   :hidden:

   pcell
   circuit
   pdk

This tutorial covers the major concepts you need to know to start designing. It starts with the introducing the general
concept of PCell. Then, ``PCell`` class of ``palgds`` is

Crawl a web page

The most simple way to use our program is with no arguments.
Simply run

.. code-block:: python

    python main.py -u <url>
    print("kdd")

to crawl a webpage.

Crawl a page slowly

To add a delay to your crawler,
use -d::

    python main.py -d 10 -u <url>

This will wait 10 seconds between page fetches.

Crawl only your blog

You will want to use the -i flag,
which while ignore URLs matching the passed regex::

    python main.py -i "^blog" -u <url>

This will only crawl pages that contain your blog URL.


.. code-block:: python
   :linenos:
   :emphasize-lines: 3,5-6

   def some_function():
       interesting = False
       print 'This line is highlighted.'
       print 'This one is not...'
       print '...but this one is.'
       print 'This one is highlighted too.'