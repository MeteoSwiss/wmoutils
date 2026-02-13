"""
Copyright (c) 2026 MeteoSwiss, contributors listed in AUTHORS

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

Module contains: functions to query external APIs, e.g. WDQMS and OSCAR/Surface.
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
def build_wdqms_request(station_type: str, interval: str) -> str:
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

    req = requests.get(build_wdqms_request(station_type, interval),
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


@log_func_call(logger)
def query_oscar_surface(extra_prms: list | None = None, **search_params: dict) -> pl.DataFrame:
    """ Utility function to query OSCAR/Surface and extract relevant station information.

    Args:
        extra_prms (list, optional): list of extra parameters to extract from the API reply in
            addition to the default ones.
        **search_params: search keyword-arguments-and-value-pairs, to be fed directly to the
            'params' keyword of the API requests.get() function.

    Returns:
        pl.DataFrame: containing the 'wigosId', 'Station name', 'longitude', and 'latitude' columns,
            and any extra parameters specified in the 'extra_prms' argument.

    Example:
        To query a station with a specific wigosId:
        query_oscar_surface(wigosId='0-20000-0-06610')

        To query all fixed surface stations in Switzerland:
        query_oscar_surface(territoryName='CHE',facilityType='LandFixed')

    API Reference:
       https://oscar.wmo.int/surface/#/faq/

    """

    # Launch the API request ...
    req = requests.get('https://oscar.wmo.int/surface/rest/api/search/station',
                       params=search_params,
                       timeout=10)

    # If something went wrong with the request, let's issue an error.
    if req.status_code != 200:
        raise WmoutilsError(f"OSCAR API request failed with status code {req.status_code}" +
                            f" and message: {req.text}")

    # Set the default parameters to extract from the API reply
    prms_out = ['wigosId', 'name', 'longitude', 'latitude']

    # Deal with possible additional prms
    if extra_prms is not None:
        # Make sure I got a list of strings, and not something else.
        if not isinstance(extra_prms, list) or not all(isinstance(item, str)
                                                       for item in extra_prms):
            raise WmoutilsError("The 'extra_prms' argument must be a list of strings.")

        # Very well, let's add the extra parameters to the list of parameters to extract.
        prms_out += extra_prms

    # Extract the necessary information from the reply ...
    stations = [[item[prm] for prm in prms_out] if 'wigosId' in item.keys()
                # If wigosId is missing, fill it with None
                else [None] + [item[prm] for prm in prms_out[1:]]
                for item in req.json()['stationSearchResults']]

    # ... and convert it to a bona-fide polars dataframe.
    stations_df = pl.DataFrame(stations, schema=prms_out, orient='row')

    return stations_df
