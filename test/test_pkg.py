"""
Copyright (c) 2026 MeteoSwiss, contributors listed in AUTHORS

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause
"""

# Import from this module
import wmoutils


def test_pkg_import():
    """ Test that the package can be imported. """

    assert wmoutils.gbon.resolution_to_influence_radius(200) < 200
