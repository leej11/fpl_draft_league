FPL Draft League documentation!
============================================

Welcome to the FPL Draft League documentation. This is a hobby project I've been working on to pull data from the the
[fantasy premier league (FPL) draft game](https://draft.premierleague.com/), produce some cool insights and charts and
share with other league members.

Repository Structure
^^^^^^^^^^^^^^^^^^^^^^^^^
A brief overview of how the repository is structured.

*/data*

Any data related to the FPL Draft League will be stored here.
This is typically json responses from various api calls made to the FPL website.

*/fpl_draft_league*
This is the "package" containing the package modules, for example:

* `fpl_draft_league.py`
* `charts.py`
* `utils.py`
* `transactions.py`
* `player_performance.py`

*/notebooks*
This is for storing example notebooks for illustrating functionality of the package.

Contextual Reading
^^^^^^^^^^^^^^^^^^^^^
* [Reddit comment about how to identify FPL Draft APIs and get the URLs](https://www.reddit.com/r/FantasyPL/comments/9rclpj/python_for_fantasy_football_using_the_fpl_api/)
* [FantasyFutopia.com article on querying an API, capturing the data and getting it into a dataframe](http://www.fantasyfutopia.com/python-for-fantasy-football-apis-and-json-data/)

Query the FPL Draft API
^^^^^^^^^^^^^^^^^^^^^^^^^
To query and get the latest data from the Draft FPL API, you essentially do 3 things

1. Use *requests* to send a
2. tbd
3. tbd

Guide
^^^^^^
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   source/getting_started
   source/licence
   source/help

.. automodule:: fpl_draft_league
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
