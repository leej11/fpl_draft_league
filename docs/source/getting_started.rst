Getting Started
===============

1. Getting your league's data
-------------------------------
The first step in analysing your FPL Draft League data is to use the :py:func:`fpl_draft_league.utils.get_json`
function.

.. code-block:: python
   :linenos:

   from fpl_draft_league import utils

   email_address = 'my_email@gmail.com'
   league_id = 12345
   output_location = 'path/to/data/folder/'

   utils.get_json(email_address, league_id, output_location)

Running the above (with your own values substituted), you will obtain all the supported .json data files in
your specified output_location.

If you perhaps wanted just a specific dataset, say the transactions dataset, then you could make use of the
optional argument `datasets`.

.. code-block:: python
   :linenos:

   from fpl_draft_league import utils

   email_address = 'my_email@gmail.com'
   league_id = 12345
   output_location = 'path/to/data/folder/'
   desired_datasets = ['transactions']

   utils.get_json(
       email_address=email_address,
       league_id=league_id,
       output_location=output_location,
       datasets=desired_datasets
   )

Very nice!
