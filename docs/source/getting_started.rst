Getting Started
===============

.. _GS Step 1:

1. Getting JSON Data
--------------------
The first step in analysing your FPL Draft League data is to use the
:py:func:`fpl_draft_league.utils.get_json` function.

.. code-block:: python
   :linenos:

   from fpl_draft_league import utils

   email_address = 'my_email@gmail.com'
   league_id = 12345
   output_location = 'path/to/data/folder/'

   utils.get_json(email_address, league_id, output_location)

Running the above (with your own values substituted), you will obtain all the
supported .json data files in your specified output_location.

..
   TODO: Add list of the "supported" .json data files

If you perhaps wanted just a specific dataset, say the transactions dataset,
then you could make use of the optional argument `datasets`:

.. code-block:: python
   :linenos:

   from fpl_draft_league import utils

   email_address = 'my_email@gmail.com'
   league_id = 12345
   output_location = 'path/to/data/folder/'
   desired_datasets = ['transactions']

   utils.get_json(email_address, league_id, output_location, datasets)

Very nice!

2. Convert JSON to Dataframes
-------------------------------
In, :ref:`Step 1<GS Step 1>`, we pulled the various different
JSON datasets from the FPL website.

If you want to then analyse your data, you'll most likely want it in a pandas
dataframe, and this is where :py:func:`fpl_draft_league.utils.get_dataframe`
comes in.

Perhaps for now we want to just analyse the standings data. This is contained
within the `details.json` file.

.. code-block:: python
   :linenos:

   from fpl_draft_league import utils

   df = utils.get_dataframe('standings')

   df.head()