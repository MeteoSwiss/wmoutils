"""
Copyright (c) 2026 MeteoSwiss, contributors listed in AUTHORS

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause
"""

import polars as pl

from wmoutils.errors import WmoutilsError
from wmoutils.wmo import get_wdqms_request, query_wdqms, query_oscar_surface


def test_get_wdqms_request():
    """ Test the get_wdqms_request function living in wmo.py """

    # Test for surface station and monthly interval
    request = get_wdqms_request(station_type='surface', interval='monthly')
    assert request == 'https://wdqms.wmo.int/wdqmsapi/v1/download/gbon/synop/monthly/availability/?'

    # Test for upper-air station and daily interval
    request = get_wdqms_request(station_type='upper-air', interval='daily')
    assert request == 'https://wdqms.wmo.int/wdqmsapi/v1/download/gbon/temp/daily/availability/?'

    # Test for invalid station type
    try:
        get_wdqms_request(station_type='invalid', interval='monthly')
        assert False, "Expected WmoutilsError for invalid station type"
    except WmoutilsError as e:
        assert str(e) == "Unknown station_type: invalid"


def test_query_wdqms():
    """ Test the query_wdqms function living in wmo.py """

    # Test for valid input
    df = query_wdqms(station_type='surface', var_name='temperature',
                     interval='monthly', date='2023-11')
    assert isinstance(df, pl.DataFrame)

    # Test for failed request via invalid data
    try:
        query_wdqms(station_type='surface', var_name='temperature',
                    interval='monthly', date='invalid-date')
        assert False, "Expected WmoutilsError for failed request"
    except WmoutilsError as e:
        assert "WDQMS API request failed" in str(e)


def test_query_oscar_surface():
    """ Test that we can query OSCAR Surface, and get proper results. """

    # Query a single station
    out = query_oscar_surface(wigosId='0-20000-0-06610')

    assert len(out) == 1
    assert out['name'][0] == 'PAYERNE (6610-0)'  # pylint: disable=unsubscriptable-object
    assert out['wigosId'][0] == '0-20000-0-06610'  # pylint: disable=unsubscriptable-object

    # Query stations with no wigosId, and make sure the wigosId column is filled with None
    # Argentina has 6 of them as of 2026-02-13
    out = query_oscar_surface(territoryName='ARG', facilityType='LandFixed')
    assert 'wigosId' in out.columns
    assert out['wigosId'].null_count() > 0  # pylint: disable=unsubscriptable-object
