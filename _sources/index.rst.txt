wmoutils
========

Welcome to the documentation of wmoutils: a simple and unassuming collection of utility functions
to query and extract WMO-related information from various sources, such as `WDQMS`_ and
`OSCAR/Surface`_.

.. _WDQMS: https://wdqms.wmo.int/
.. _OSCAR/Surface: https://oscar.wmo.int/surface/#/

With wmoutils, you can:

- query OSCAR/Surface::

   from wmoutils.query import query_oscar_surface

   # Query a single station using its wigos ID
   one_site = query_oscar_surface(wigosId='0-20000-0-06610')

   # Query all fixed surface stations in Switzerland
   many_sites = query_oscar_surface(territoryName='CHE',facilityType='LandFixed')

- query WDQMS::

   from wmoutils.query import query_wdqms

   # Query the availability of temperature observations for all GBON surface stations in 2026-01
   availability = query_wdqms(module='gbon', station_type='surface', var_name='temperature',
                              interval='monthly', category='availability', date='2026-01')

- derive the so-called *radius of influence* for GBON stations::

   from wmoutils.gbon import get_influence_radius

   # Compute the radius of influence for all GBON surface stations in Switzerland
   roi_km = get_influence_radius(station_type='surface', over='land', high_density=False)

You can refer to the pages linked below for more details on these different functionalities.

If yopu face unexpected trouble while using wmoutils, please report the issue on the
`GitHub repository`_.

If you wish to contribute to the development of wmoutils, please refer to the
`contributing guidelines`_.

.. _GitHub repository: https://github.com/MeteoSwiss/wmoutils/issues
.. _contributing guidelines: https://github.com/MeteoSwiss/wmoutils/blob/main/CONTRIBUTING.md

.. toctree::
   :maxdepth: 2
   :caption: Table of contents

   Start <self>
   query
   gbon
   changelog
