.. _testing_and_validation:

Testing and Validation
======================

This page explains how to validate JsonToFrame behavior using the existing
pytest suite and fixture-driven checks.

Test Objectives
---------------

The current test strategy verifies that:

- Every JSON fixture in ``test/data`` is included in parametrized test coverage.
- Every covered fixture can be converted into a pandas DataFrame.
- Converted DataFrames are non-empty and include at least one column.

Current Test File
-----------------

Main test module:

- ``test/test/test_json_fixtures.py``

Key tests:

- ``test_each_fixture_converts_to_dataframe``
- ``test_parametrization_covers_all_json_fixtures``

These tests use ``LoadInfo`` and ``DeepNestedHandler`` directly, providing
an end-to-end validation path from input fixture to tabular output.

Prerequisites
-------------

Before running tests, ensure dependencies are installed:

.. code-block:: bash

	pip install -e .

or:

.. code-block:: bash

	pip install -r requirements.txt

Make sure ``pytest`` is available in your environment.

Run Test Commands
-----------------

Run all tests:

.. code-block:: bash

	python3 -m pytest -v

Run only fixture conversion tests:

.. code-block:: bash

	python3 -m pytest -v test/test/test_json_fixtures.py

Run tests and keep print output visible:

.. code-block:: bash

	python3 -m pytest -v -s test/test/test_json_fixtures.py

Run a single test function:

.. code-block:: bash

	python3 -m pytest -v test/test/test_json_fixtures.py::test_each_fixture_converts_to_dataframe

How the Fixture Tests Work
--------------------------

1. The suite discovers all ``*.json`` files under ``test/data``.
2. Pytest parametrizes one test case per discovered fixture.
3. Each file is loaded with ``LoadInfo(file=...)``.
4. Data is converted using ``DeepNestedHandler(...).convert_to_df()``.
5. Assertions check type and minimal structural validity:

	- output is a pandas DataFrame
	- DataFrame is not empty
	- DataFrame has one or more columns

6. A second test compares discovered fixture names against expected fixture names
	to ensure no JSON fixture is silently skipped.

Validation Criteria
-------------------

The current baseline validates structural conversion correctness, not business
semantic correctness.

What is validated now:

- Conversion pipeline runs without exceptions on sample fixtures.
- Output shape is viable for downstream usage.
- Fixture parametrization remains in sync with files on disk.

What is not yet validated:

- Exact output column names for each fixture.
- Exact row counts for specific nested structures.
- Type-level expectations per output column.
- Deterministic ordering guarantees for columns and rows.

Interpreting Failures
---------------------

``ValueError`` failures
^^^^^^^^^^^^^^^^^^^^^^^

Common causes:

- Invalid input type passed through loader.
- Nested conversion expected a dictionary but received another type.

Actions:

- Inspect the failing fixture payload structure.
- Confirm top-level and nested shapes match expected converter behavior.

``json.JSONDecodeError`` failures
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Common cause:

- Malformed JSON in a fixture file.

Actions:

- Validate JSON syntax.
- Reformat or correct invalid tokens, quotes, or trailing commas.

``FileNotFoundError`` failures
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Common cause:

- Broken fixture path or renamed file.

Actions:

- Confirm fixture file exists under ``test/data``.
- Re-run tests from repository root.

Debugging Workflow
------------------

When a fixture fails conversion:

1. Re-run the test with ``-s`` to inspect printed frame previews.
2. Run only the failing fixture by adding a name filter:

	.. code-block:: bash

		python3 -m pytest -v -s test/test/test_json_fixtures.py -k "fixture_name"

3. Open the fixture and inspect nested list/dict structure.
4. Reproduce in a small script:

	.. code-block:: python

		from pathlib import Path
		from json2df.json2df import LoadInfo, DeepNestedHandler

		json_file = Path("test/data/svg_example.json")
		payload = LoadInfo(file=json_file).get_data()
		frame = DeepNestedHandler(payload).convert_to_df()

		print(frame.head())
		print(frame.shape)
		print(frame.columns.tolist())

Adding New Fixture Coverage
---------------------------

To extend dataset coverage:

1. Add a new ``*.json`` file into ``test/data``.
2. Re-run ``python3 -m pytest -v test/test/test_json_fixtures.py``.
3. No manual parametrization updates are required because fixtures are discovered
	dynamically.

If the new fixture includes uncommon patterns (for example deep tuple/list
combinations), consider adding explicit assertions in a dedicated test module.

Recommended Additional Tests
----------------------------

For stronger regression protection, add targeted tests for:

- Stable flattened column names for representative payloads.
- Row-count expectations for known list-expansion inputs.
- Empty list handling to confirm ``NaN`` output behavior.
- Top-level list payload conversion with heterogeneous keys.
- Error-path tests for invalid loader inputs and malformed JSON strings.

Example of a targeted assertion-style test:

.. code-block:: python

	import pandas as pd
	from json2df.json2df import DeepNestedHandler

	def test_nested_key_flattening_shape():
		 payload = {
			  "user": {"name": "Ana", "profile": {"age": 30}},
			  "active": True,
		 }

		 frame = DeepNestedHandler(payload).convert_to_df()

		 assert isinstance(frame, pd.DataFrame)
		 assert "user_name" in frame.columns
		 assert "user_profile_age" in frame.columns
		 assert len(frame) == 1

Continuous Validation Tips
--------------------------

- Run fixture tests before every release.
- Run tests after adding or editing fixture files.
- Keep sample fixtures diverse to reflect real nested payload complexity.
- Keep failing fixtures in version control as regression reproductions.

See Also
--------

- ``getting_started`` for setup and initial conversion workflow
- ``usage_examples`` for practical conversion patterns
- ``api_reference`` for method-level behavior and exception details
