.. _development_notes:

.. currentmodule:: json2df.json2df

Development Notes
=================

This page provides contributor and maintainer guidance for working on
JsonToFrame locally, validating changes, and publishing updates safely.

Repository Structure
--------------------

Top-level layout:

- ``src/json2df``: package source code
- ``test/data``: JSON fixtures used for conversion validation
- ``test/test``: pytest suite
- ``src/docs``: Sphinx documentation project

Important files:

- ``pyproject.toml``: packaging metadata and build system config
- ``requirements.txt``: runtime dependency baseline
- ``src/docs/source/conf.py``: Sphinx settings
- ``.readthedocs.yaml``: Read the Docs build configuration

Local Development Setup
-----------------------

Recommended environment setup from repository root:

.. code-block:: bash

	python3 -m venv .venv
	source .venv/bin/activate
	pip install --upgrade pip
	pip install -e .

Install documentation dependencies:

.. code-block:: bash

	pip install -r src/docs/requirements.txt

Install test tooling (if not already available in your environment):

.. code-block:: bash

	pip install pytest

Package and Build Configuration
-------------------------------

Build backend:

- ``setuptools.build_meta``

Current package metadata highlights:

- Project name: ``json-to-frame``
- Python requirement: ``>=3.10``
- Runtime dependency: ``pandas``
- Package discovery root: ``src``

When updating package metadata, keep these areas synchronized:

- Version in ``pyproject.toml``
- Any version labels in Sphinx docs
- Release/tag naming strategy in source control

Running Tests
-------------

Run complete test suite:

.. code-block:: bash

	python3 -m pytest -v

Run fixture conversion suite only:

.. code-block:: bash

	python3 -m pytest -v test/test/test_json_fixtures.py

Run tests with printed DataFrame previews:

.. code-block:: bash

	python3 -m pytest -v -s test/test/test_json_fixtures.py

What the current tests guarantee:

- Every JSON fixture under ``test/data`` is included in parametrized coverage.
- Each fixture converts to a non-empty DataFrame with at least one column.

Documentation Build Workflow
----------------------------

The docs project uses Sphinx and is rooted at ``src/docs``.

Build docs locally:

.. code-block:: bash

	cd src/docs
	make html

Alternative explicit command:

.. code-block:: bash

	sphinx-build -M html source build

Useful Sphinx targets:

.. code-block:: bash

	make clean
	make dirhtml
	make linkcheck

Read the Docs Integration
-------------------------

Read the Docs configuration is defined in ``.readthedocs.yaml``:

- OS: Ubuntu 24.04
- Python: 3.12
- Sphinx builder: ``dirhtml``
- Config path: ``src/docs/source/conf.py``
- Dependency file: ``src/docs/requirements.txt``

If docs fail remotely but work locally, compare local package versions against
the versions resolved in the Read the Docs build logs.

Autodoc and API Documentation Notes
-----------------------------------

Autodoc is enabled in Sphinx extensions, so API pages can reference module
members directly. Keep public class names and import paths stable, or update:

- ``usage_examples`` page snippets
- ``api_reference`` directives and signatures
- README usage sections

Coding and Change Guidelines
----------------------------

When modifying conversion logic in ``src/json2df/json2df.py``:

1. Add or update at least one fixture scenario that exercises the change.
2. Run fixture tests with ``-s`` and inspect frame shape/columns.
3. Update ``usage_examples`` and ``api_reference`` when behavior changes.
4. Rebuild docs locally to catch rst or autodoc regressions.

Prefer behavior-preserving refactors unless the change is intentionally
user-facing and documented.

Release Checklist
-----------------

Before cutting a release:

1. Ensure tests pass locally.
2. Ensure docs build without warnings.
3. Confirm README examples still use valid API names.
4. Confirm package version is updated in ``pyproject.toml``.
5. Confirm documentation version labels match project version.
6. Tag and push release artifacts according to your Git flow.

Known Consistency Checks
------------------------

Check these items periodically to avoid drift:

- ``conf.py`` release value should match ``pyproject.toml`` version.
- ``main.py`` sample entrypoint should reference currently exported class names.
- Docs toctree entries should include all maintained rst pages.

Troubleshooting
---------------

Import errors during docs build
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cause:

- Missing editable install or missing dependencies.

Fix:

- Run ``pip install -e .`` and ``pip install -r src/docs/requirements.txt``.

Autodoc page shows missing members
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cause:

- Import path mismatch or renamed symbols not reflected in rst files.

Fix:

- Update module/class paths in ``api_reference`` and rebuild docs.

Fixture tests fail after adding new JSON data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cause:

- New fixture introduces unsupported structure or malformed JSON.

Fix:

- Validate JSON syntax and inspect nested dict/list shape expectations.

See Also
--------

- ``getting_started`` for installation and first-run steps
- ``usage_examples`` for practical conversion patterns
- ``testing_and_validation`` for test execution and diagnosis
- ``api_reference`` for method-level behavior details
