"""
Copyright (c) 2026 MeteoSwiss, contributors listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

Module contains: GBON-related functions
"""

# Import from Python
import logging

# Import from this module
from .logger import log_func_call
from .errors import WmoutilsError

# Setup the logger
logger = logging.getLogger(__name__)


@log_func_call(logger)
def get_resolution(station_type: str, over: str = 'land',
                   high_density: bool = False) -> int:
    """ Returns the GBON horizontal resolution for a given station type.

    Args:
        station_type (str): one of ``['surface', 'upper-air']``.
        over (str, optional): one of ``['land', 'sea']``. Defaults to ``'land'``.
        high_density (bool, optional): if ``True``, will return the GBON high density value.
            Defaults to ``False``.

    Returns:
        int: the GBON horizontal resolution in km

    """

    match station_type:
        case 'surface':
            match over:
                case 'land':
                    if high_density:
                        return 100
                    return 200
                case 'sea':
                    return 500
                case _:
                    raise WmoutilsError(f'Unrecognized "over" value: {over}')
        case 'upper-air':
            match over:
                case 'land':
                    if high_density:
                        return 200
                    return 500
                case 'sea':
                    return 1000
                case _:
                    raise WmoutilsError(f'Unrecognized "over" value: {over}')
        case _:
            raise WmoutilsError(f'Unrecognized "station_type" value: {station_type}')


@log_func_call(logger)
def resolution_to_influence_radius(res: float) -> float:
    """ Convert a GBON horizontal resolution into an influence radius. """

    return (2**0.5)/2 * res


@log_func_call(logger)
def get_influence_radius(station_type: str, over: str = 'land',
                         high_density: bool = False) -> float:
    """ Returns the so-called radius of influence of a GBON station given its type.

    The radius of influence is computed as R = (GBON horizontal resolution)/2 x sqrt(2), and
    represent the radius of the circle that ought to be drawn around each GBON stations when
    assembling network maps.

    Args:
        station_type (str): one of ``['surface', 'upper-air']``.
        over (str, optional): one of ``['land', 'sea']``. Defaults to ``'land'``.
        high_density (bool, optional): if ``True``, will return the GBON high density value.
            Defaults to ``False``.

    Returns:
        float: the radius of influence in km.

    Example:
        To get the the GBON radius of influence for a surface station over land,
        with standard desnity::

            from wmoutils.gbon import get_influence_radius

            radius_in_km = get_influence_radius(station_type='surface', over='land',
                                                high_density=False)

    Notes:

        The concept of radius of influence for GBON stations was first introduced in
        Appendix A of the SOFF National Contribution Plan for the Democratic Republic of Congo,
        `Vogt et al. (2024)`_. What follows is a summary of the relevant section of this document,
        to which we refer the interested reader for more details.

        The radius of influence R_inf of a GBON station corresponds to the maximum horizontal
        distance between the station and any geographical location situated closer to this station
        than any other GBON station.

        When performing a so-called *baseline GBON gap analysis*, WMO adopts the premise that GBON
        stations are being distributed on a regular, orthogonal, two-dimensional grid, with a
        horizontal/vertical distance between stations equal to the relevant GBON horizontal
        resolution.

        Under this specific premise, all stations thus have the same baseline radius of influence
        of:

        R_inf = sqrt(2)/2 x (GBON horizontal resolution)

        which represent the longest distance between any geographical point and its closest GBON
        station.

        .. _Vogt et al. (2024): https://www.un-soff.org/wp-content/uploads/2025/02/Democratic-Republic-of-Congo-GBON-National-Gap-Analysis.pdf

    """

    return resolution_to_influence_radius(get_resolution(station_type,
                                                         over=over, high_density=high_density))
