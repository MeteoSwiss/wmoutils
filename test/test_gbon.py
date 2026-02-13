"""
Copyright (c) 2026 MeteoSwiss, contributors listed in AUTHORS

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause
"""

from wmoutils.gbon import get_resolution, get_influence_radius, resolution_to_influence_radius


def test_get_resolution():
    """ Test the get_resolution() function. """

    assert get_resolution('surface', over='land', high_density=False) == 200


def test_resolution_to_influence_radius():
    """ Test the resolution_to_influence_radius() function. """

    assert round(resolution_to_influence_radius(200), 0) == 141


def test_influence_radius():
    """ Test the get_influence_radius() function. """

    assert round(get_influence_radius('surface', over='land', high_density=False), 0) == 141
