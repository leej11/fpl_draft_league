# FPL Draft League
---
This is a hobby project to produce fun data and charts related to the [fantasy premier league (FPL) draft game](https://draft.premierleague.com/).

## Repository Structure

#### /data
Any data related to the FPL Draft League will be stored here. This is typically json responses from various api calls made to the FPL website.

#### /feature_name
For now, I think a nice structure is to have a sub-folder for each feature. For example:

* /transactions
* /head2head
* /league_details

Within these folders, a nice structure is to have a sub-module paired with a demo jupyter notebook.

For example:

* /transactions
    * transactions.py
    * transactions.ipynb


## Useful Links / Reading

https://www.reddit.com/r/FantasyPL/comments/9rclpj/python_for_fantasy_football_using_the_fpl_api/
http://www.fantasyfutopia.com/python-for-fantasy-football-apis-and-json-data/
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.merge.html
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.merge.html
