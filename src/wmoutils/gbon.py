"""
Copyright (c) 2026 MeteoSwiss, contributors listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

Module contains: GBON-related functions
"""

# Import from Python
import logging
from typing import Optional

# Import from this module
from .logger import log_func_call
from .errors import WmoutilsError

# Setup the logger
logger = logging.getLogger(__name__)


@log_func_call(logger)
def get_resolution(station_type: str, over: Optional[str] = 'land',
                   high_density: Optional[bool] = False) -> int:
    """ Return the GBON horizontal resolution for a given station type.

    Args:
        station_type (str): one of ['surface', 'upper-air'].
        over (str, optional): one of ['land', 'sea']. Defaults to 'land'.
        high_density (bool, optional): if True, will return the GBON high density value.
            Defaults to False.

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
def get_influence_radius(station_type: str, over: Optional[str] = 'land',
                         high_density: Optional[bool] = False) -> float:
    """ Return the theoretical influence radius of a GBON station given its type.

    Args:
        station_type (str): one of ['surface', 'upper-air'].
        over (str, optional): one of ['land', 'sea']. Defaults to 'land'.
        high_density (bool, optional): if True, will return the GBON high density value.
            Defaults to False.

    Returns:
        float: the influence radius in km.

    The influence radius is computed as R = (GBON horizontal resolution)/2 * sqrt(2).
    This derives from the fact that with a uniform distribution of GBON stations in a regular grid,
    the most distant point will be located R km away.

    """

    return resolution_to_influence_radius(get_resolution(station_type,
                                                         over=over, high_density=high_density))
