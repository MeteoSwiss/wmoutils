"""
Copyright (c) 2026 MeteoSwiss, contributors listed in AUTHORS

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause
"""

from importlib.metadata import version as getversion

# Extract the version from the system, because it is set (upon release) by the CI/CD pipeline
# via the pyproject.toml file (using poetry).
__version__ = getversion("wmoutils")
