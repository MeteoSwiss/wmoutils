.. image:: https://img.shields.io/pypi/v/wmoutils.svg
    :target: https://pypi.org/project/wmoutils/

.. image:: https://img.shields.io/pypi/pyversions/wmoutils.svg
    :target: https://pypi.org/project/wmoutils/

.. image:: https://img.shields.io/pypi/l/wmoutils.svg
    :target: https://pypi.org/project/wmoutils/

.. image:: https://github.com/MeteoSwiss/wmoutils/actions/workflows/github-code-scanning/codeql/badge.svg
    :target: https://github.com/MeteoSwiss/wmoutils/actions/workflows/github-code-scanning/codeql

.. image:: https://github.com/MeteoSwiss/wmoutils/actions/workflows/CI_test.yaml/badge.svg
    :target: https://github.com/MeteoSwiss/wmoutils/actions/workflows/CI_test.yaml

.. image:: https://github.com/MeteoSwiss/wmoutils/actions/workflows/CI_publish_dev_documentation.yaml/badge.svg
    :target: https://github.com/MeteoSwiss/wmoutils/actions/workflows/CI_publish_dev_documentation.yaml

===============
Getting Started
===============

Collection of utilities to interact with WMO ecosystems




Development Setup with Poetry
-----------------------------

Building the Project
''''''''''''''''''''
.. code-block:: console

    $ cd wmoutils
    $ poetry install

Run Tests
'''''''''

.. code-block:: console

    $ poetry run pytest

Run Quality Tools
'''''''''''''''''

.. code-block:: console

    $ poetry run pylint wmoutils
    $ poetry run mypy wmoutils

Generate Documentation
''''''''''''''''''''''

.. code-block:: console

    $ poetry run sphinx-build doc doc/_build

Then open the index.html file generated in *wmoutils/doc/_build/*.

Build wheels
''''''''''''

.. code-block:: console

    $ poetry build

Using the Library
-----------------

To install wmoutils in your project, run this command in your terminal:

.. code-block:: console

    $ poetry add wmoutils

You can then use the library in your project through

    import wmoutils

Release the Project
-------------------

The project follows the **GitOps concept**: releases are triggered whenever a Git TAG is created.

The TAG must follow the `semantic version <https://semver.org/>`__ format and `PEP 440 <https://peps.python.org/pep-0440/>`__ , otherwise the release task will fail.

Follow these steps to create a new release:

* Adapt CHANGELOG.rst with release information
* Adapt ``doc/_static/switcher_config.json`` adding the new documentation URL for the release
* Create a new Release in the Github project
