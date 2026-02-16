"""
Copyright (c) 2026 MeteoSwiss, contributors listed in AUTHORS

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

Module contains: functions to query external APIs, e.g. WDQMS and OSCAR/Surface.
"""

# Import from Python
import logging
from io import StringIO
from datetime import datetime
import requests
import polars as pl

# import from this module
from .logger import log_func_call
from .errors import WmoutilsError

# Setup the logger
logger = logging.getLogger(__name__)


@log_func_call(logger)
def build_base_wdqms_request(module: str, station_type: str, interval: str, category: str) -> str:
    """ Return the string required for a WDQMS API request.

    Args:
        module (str): one of ['gbon', 'nwp']
        station_type (str): one of ['surface','upper-air', 'marine']
        interval (str): assessment interval, i.e. one of ['monthly', 'daily', 'six_hour'].
        category (str): one of ['availability', 'quality', 'timeliness']

    Returns:
        str: base URL of the API request

    Warning:
        Not all combinations of the above parameters are valid, and the function will raise an error
        if an invalid combination is provided.

    TODO:
       - Add support for GCOS
       - Add support for Transition Monitoring

    """

    # Basic sanity checks on the input parameters
    if module not in ['gbon', 'nwp']:
        raise WmoutilsError(f"Unknown 'module': {module}")
    if interval not in ['monthly', 'daily', 'six_hour']:
        raise WmoutilsError(f"Unknown 'interval': {interval}")
    if category not in ['availability', 'quality', 'timeliness']:
        raise WmoutilsError(f"Unknown 'category': {category}")

    # For the station type, we need to map our own keys to those used by WDQQMS.
    match station_type:
        case 'surface':
            key = 'synop'
        case 'upper-air':
            key = 'temp'
        case 'marine':
            key = 'marine_surface'
        case _:
            raise WmoutilsError(f"Unknown 'station_type': {station_type}")

    # Raise some errors in case of know wrong parameter pairs
    # GBON upper-air has no six-hour
    if module == 'gbon' and station_type == 'upper-air' and interval == 'six_hour':
        raise WmoutilsError("Six-hourly assessments are not part of upper-air GBON,'+"
                            " cannot build request.")
    # GBON has no marine stations
    if module == 'gbon' and station_type == 'marine':
        raise WmoutilsError("Marine stations are not part of GBON, cannot build request.")
    # GBON can only have availability assessments
    if module == 'gbon' and category != 'availability':
        raise WmoutilsError("GBON only has availability assessments, cannot build request.")

    return f'https://wdqms.wmo.int/wdqmsapi/v1/download/gbon/{key}/{interval}/{category}/?'


@log_func_call(logger)
def query_wdqms(  # pylint: disable=too-many-arguments, too-many-positional-arguments
                module: str, station_type: str, interval: str, category: str,
                var_name: str, date: str, period: str = '00',
                baseline: str = 'OSCAR') -> pl.DataFrame:
    """ Utility function to query WDQMS via its API, and format the reply as a polars.DataFrame.

    Args:
        module (str): one of ``['gbon', 'nwp']``.
        station_type (str): one of ``['surface', 'upper-air', 'marine']``.
        interval (str): assessment interval, i.e. one of ``['monthly', 'daily', 'six_hour']``.
        category (str): one of ``['availability', 'quality', 'timeliness']``.
        var_name (str): one of ``['temperature', 'pressure', 'humidity', 'zonal_wind',
            'meridional_wind']``.
        date (str): date of the availability assessment, e.g. ``'2023-11'``.
        period (str, optional): one of ``['00', '06', '12', '18']``. Defaults to ``'00'``.
            No effect unless if interval is ``'six_hour'``.
        baseline (str, optional): one of ``['OSCAR', 'hourly']``. Defaults to ``'OSCAR'``.
            No effect unless if module is ``'nwp'``.

    Returns:
        polars.DataFrame: the reply from the API request formatted as a polars DataFrame.

    Raises:
        WmoutilsError: if the API request fails, or if the combination of input parameters is
            invalid.

    Examples:
        Querying the availability of temperature observations for surface stations in GBON for
        January 2026::

            from wmoutils.query import query_wdqms

            out = query_wdqms(module='gbon', station_type='surface', var_name='temperature',
                              interval='monthly', category='availability', date='2026-01')


    TODO:
        - Allow to query individual NWP centers.
        - Add support for GCOS and Transition Monitoring.

    """

    # Check if the date format is correct using datetime.strptime
    try:
        valid_date = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        try:
            valid_date = datetime.strptime(date, '%Y-%m')
        except ValueError as exc:
            raise WmoutilsError(f"Invalid date format: {date}." +
                                " Expected 'YYYY-MM-DD' or 'YYYY-MM'.") from exc

    if interval in ['monthly']:
        date = valid_date.strftime('%Y-%m')
    else:
        date = valid_date.strftime('%Y-%m-%d')

    # Prepare the dict of parametters
    params = {'date': date,
              'variable': var_name,
              'centers': 'COMBINED'}

    # In some cases, I need to add more keywords
    if interval == 'six_hour':
        params['period'] = period

    if module == 'nwp':
        params['baseline'] = baseline

    req = requests.get(build_base_wdqms_request(module, station_type, interval, category),
                       params=params,
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
    """ Utility function to query OSCAR/Surface and extract relevant station information and return
    them as a polars DataFrame.

    This function acts as a simple wrapper around the
    `OSCAR/Surface API <https://oscar.wmo.int/surface/#/faq/>`_: it merely forwards the keyword
    arguments it receives to the API, and extracts a few relevant parameters from the reply into a
    polars DataFrame.

    Warning:
        This function does **not** check the validity of the keywords arguments. It is up to the
        user to ensure the keyword arguments are valid and supported by the OSCAR/Surface API.

    Note:
        See the `OSCAR/Surface API Reference <https://oscar.wmo.int/surface/#/faq/>`_ for the full
        range of supported keyword arguments.

    Args:
        extra_prms (list, optional): list of additional parameters to extract from the API reply, in
            addition to ``['wigosId', 'name', 'longitude', 'latitude']``.
        **search_params: search keyword-arguments-and-value-pairs, to be fed directly to the
            ``params`` keyword of the API ``requests.get()`` function.

    Returns:
        pl.DataFrame: DataFrame containing the API response data.

    Raises:
        WmoutilsError: if the API request fails, or if the ``extra_prms`` argument is not a list of
            strings.

    Examples:
        To query a station with a specific wigosId::

            from wmoutils.query import query_oscar_surface

            out = query_oscar_surface(wigosId='0-20000-0-06610')

        To query all fixed surface stations in Switzerland::

            out = query_oscar_surface(territoryName='CHE',facilityType='LandFixed')

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
