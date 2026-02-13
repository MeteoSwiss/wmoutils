"""
Copyright (c) 2026 MeteoSwiss, contributors listed in AUTHORS

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause
"""

# Import from Python
import logging
from io import StringIO
import requests
import polars as pl

# import from this module
from .logger import log_func_call
from .errors import WmoutilsError

# Setup the logger
logger = logging.getLogger(__name__)


@log_func_call(logger)
def get_wdqms_request(station_type: str, interval: str) -> str:
    """ Return th string required for a WDQMS API request.

    Args:
        station_type (str): either 'surface' or 'upper-air'.
        interval (str): assessment interval, i.e. one of ['monthly', 'daily', 'six_hour'].

    Returns: str of API request
    """

    match station_type:
        case 'surface':
            key = 'synop'
        case 'upper-air':
            key = 'temp'
        case _:
            raise WmoutilsError(f"Unknown station_type: {station_type}")

    return f'https://wdqms.wmo.int/wdqmsapi/v1/download/gbon/{key}/{interval}/availability/?'


@log_func_call(logger)
def query_wdqms(station_type: str, var_name: str, interval: str, date: str) -> pl.DataFrame:
    """ Send a request to WDQMS via its API, and return the text of the reply as a polars.DataFrame.

    Args:
        station_type (str): either 'surface' or 'upper-air'.
        var_name (str): name of variable, e.g. '2m Temperature'.
        interval (str): assessment interval, i.e. one of ['monthly', 'daily', 'six_hour'].
        date (str): date of the availability assessment, e.g. '2023-11'

    Returns: polars.DataFrame

    """

    req = requests.get(get_wdqms_request(station_type, interval),
                       params={'date': date,
                               'variable': var_name,
                               'centers': 'all'},
                       timeout=10)

    # Issue an error if the request was not successful.
    if req.status_code != 200:
        raise WmoutilsError(f"WDQMS API request failed with status code {req.status_code}" +
                            f" and message: {req.text}")

    # Convert the text of the reply to a polars.DataFrame, and return it.
    pdf = pl.read_csv(StringIO(req.text))

    return pdf
