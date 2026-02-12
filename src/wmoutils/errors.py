"""
Copyright (c) 2026 MeteoSwiss, contributors listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

Module contains: custom error and warning classes
"""


class WmoutilsError(Exception):
    """ The default error class for wmoutils, which is a child of the :py:exc:`Exception` class.
    """


class WmoutilsWarning(Warning):
    """ The default warning class for wmoutils, which is a child of the :py:class:`Warning` class.
    """
