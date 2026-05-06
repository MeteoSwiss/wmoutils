Installation
============

``wmoutils`` is available on `PyPI`_, and can be installed using ``pip``:

.. code-block:: bash

   pip install wmoutils

If you are so inclined, you can also install ``wmoutils`` from source, via a local clone of
the relevant `Github`_ repository:

.. code-block:: bash

   git clone https://github.com/MeteoSwiss/wmoutils.git
   cd wmoutils
   pip install -e .

Please refer to the code `contributing guidelines`_ for more details, inclduing on how to set
up a suitable development environment for ``wmoutils`` (should you be interested to contribute).


.. _PyPI: https://pypi.org/project/wmoutils/
.. _Github: https://github.com/MeteoSwiss/wmoutils
.. _contributing guidelines: https://github.com/MeteoSwiss/wmoutils/blob/main/CONTRIBUTING.rst


Logging
=======

``wmoutils`` comes with a built-in logging setup relying on a `NullHandler`_ to avoid bothering
users with unwanted messages. Should you wish to see/record the log messages (e.g. for debugging
purposes), you can do so by setting up your own handler, e.g. via:

.. code-block:: python

      import logging

      logging.basicConfig(level=logging.INFO)
      logging.getLogger('wmoutils').setLevel(logging.DEBUG)

      # ... your code using wmoutils here ...


.. _NullHandler: https://docs.python.org/3/library/logging.handlers.html#logging.NullHandler