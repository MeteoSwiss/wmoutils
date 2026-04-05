"""
Copyright (c) 2026 MeteoSwiss, contributors listed in AUTHORS

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause
"""

import pytest

from wmoutils.gbon import get_resolution, get_influence_radius, resolution_to_influence_radius
from wmoutils.errors import WmoutilsError


def test_get_resolution():
    """ Test the get_resolution() function. """

    assert get_resolution('surface', over='land', high_density=False) == 200
    assert get_resolution('surface', over='land', high_density=True) == 100
    assert get_resolution('surface', over='sea', high_density=False) == 500
    with pytest.raises(WmoutilsError, match='Unrecognized "over" value: bad_value'):
        get_resolution('surface', over='bad_value')
    assert get_resolution('upper-air', over='land', high_density=False) == 500
    assert get_resolution('upper-air', over='land', high_density=True) == 200
    assert get_resolution('upper-air', over='sea', high_density=False) == 1000
    with pytest.raises(WmoutilsError, match='Unrecognized "over" value: bad_value'):
        get_resolution('upper-air', over='bad_value')
    with pytest.raises(WmoutilsError, match='Unrecognized "station_type" value: bad_value'):
        get_resolution('bad_value')

    # Assert the errors
    try:
        get_resolution('invalid-station-type')
        assert False, "Expected WmoutilsError for invalid station type"
    except WmoutilsError as e:
        assert str(e) == 'Unrecognized "station_type" value: invalid-station-type'


def test_resolution_to_influence_radius():
    """ Test the resolution_to_influence_radius() function. """

    assert round(resolution_to_influence_radius(200), 0) == 141


def test_influence_radius():
    """ Test the get_influence_radius() function. """

    assert round(get_influence_radius('surface', over='land', high_density=False), 0) == 141
