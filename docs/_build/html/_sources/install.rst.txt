============
Installation
============

This program is designed to run on a particular raspberry pi with particular equipment.
For development purposes, run the following command

.. code-block:: bash

    python setup.py install --user

--user this flag tells setup.py to install into the user's local bin rather than the system bin.

or

.. code-block:: bash

    pip install -e --user .

-e this tells pip to create a link to directory files allowing for quick changes.
--user this tells pip to install to the user's local bin rather than the system bin.