The ``gbon`` module
===================

GBON resolution
----------------

This ``gbon`` module encodes the applicable GBON horizontal resolutions for different station types
within the function:

.. autofunction:: wmoutils.gbon.get_resolution
   :noindex:

GBON radius of influence
-------------------------

The true *raison d'être* of the ``gbon`` module is to ease the derivation of the radius of
influence of GBON stations, via the function:

.. autofunction:: wmoutils.gbon.get_influence_radius
   :noindex:

