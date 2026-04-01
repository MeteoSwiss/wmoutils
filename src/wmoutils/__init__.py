"""
Copyright (c) 2026 MeteoSwiss, contributors listed in AUTHORS

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause
"""

# Import from Python
import logging
from importlib.metadata import version as getversion

# Import from this package
from . import gbon
from . import query

# Make sure users can do things like import wmoutils -> wmoutils.query.etc ...
__all__ = ['query', 'gbon']

# Extract the version from the system, because it is set (upon release) by the CI/CD pipeline
# via the pyproject.toml file (using poetry).
__version__ = getversion("wmoutils")

# Instantiate the module logger
logger = logging.getLogger(__name__)
# Hide any log messages if the user did not instantiate any handler
# For details, see: https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
logger.addHandler(logging.NullHandler())
