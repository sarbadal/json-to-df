.. _usage_examples:

Usage Examples
==============

This page shows practical JsonToFrame patterns using the current API:

- ``LoadInfo`` for normalizing inputs
- ``DeepNestedHandler`` for flattening and conversion

All examples are designed to run from the project root.

Common Import Pattern
---------------------

Use this import style in all examples:

.. code-block:: python

	from json2df.json2df import LoadInfo, DeepNestedHandler

Example 1: Convert a Python Dictionary
--------------------------------------

Use this when your payload already exists as a Python object.

.. code-block:: python

	from json2df.json2df import LoadInfo, DeepNestedHandler

	payload = {
		 "user": {
			  "name": "Alice",
			  "address": {
					"city": "Berlin",
					"zip": "10115"
			  }
		 },
		 "active": True
	}

	normalized = LoadInfo(info=payload).get_data()
	df = DeepNestedHandler(json_data=normalized).convert_to_df()

	print(df)
	print(df.columns.tolist())

Expected behavior:

- Nested keys are flattened with underscore separators.
- Output columns may include fields such as ``user_name`` and ``user_address_city``.

Example 2: Convert from a JSON File
-----------------------------------

Use this for fixture files, exported API responses, or local JSON snapshots.

.. code-block:: python

	from json2df.json2df import LoadInfo, DeepNestedHandler

	payload = LoadInfo(file="test/data/svg_example.json").get_data()
	df = DeepNestedHandler(json_data=payload).convert_to_df()

	print(df.head())
	print(f"rows={len(df)}, cols={len(df.columns)}")

Try with other provided fixtures:

- ``test/data/superhero_team_roster.json``
- ``test/data/product_supplier_inventory.json``
- ``test/data/user_household_data.json``

Example 3: Convert from a JSON String
-------------------------------------

Use this when data arrives as a raw JSON string (for example from HTTP or logs).

.. code-block:: python

	from json2df.json2df import LoadInfo, DeepNestedHandler

	raw_json = '{"app":"store","stats":{"visits":1200,"country":"US"}}'
	normalized = LoadInfo(info=raw_json).get_data()
	df = DeepNestedHandler(json_data=normalized).convert_to_df()

	print(df)

Expected behavior:

- The JSON string is parsed once by ``LoadInfo``.
- Nested fields become flat DataFrame columns.

Example 4: Top-Level List Input
-------------------------------

If your top-level structure is a list of objects, each item is flattened,
then concatenated into a single DataFrame.

.. code-block:: python

	from json2df.json2df import DeepNestedHandler

	payload = [
		 {"id": 1, "profile": {"name": "Ana", "age": 27}},
		 {"id": 2, "profile": {"name": "Lee", "age": 31}}
	]

	df = DeepNestedHandler(json_data=payload).convert_to_df()
	print(df)

Expected behavior:

- One output row per top-level list item (subject to nested list expansion).
- Columns are merged across items; missing values appear as ``NaN``.

Example 5: Nested List Expansion
--------------------------------

Lists inside dictionaries expand into additional rows.

.. code-block:: python

	from json2df.json2df import DeepNestedHandler

	payload = {
		 "order_id": "ORD-10",
		 "items": [
			  {"sku": "A1", "qty": 2},
			  {"sku": "B9", "qty": 1}
		 ]
	}

	df = DeepNestedHandler(json_data=payload).convert_to_df()
	print(df)

Expected behavior:

- ``items`` entries generate multiple rows.
- Parent-level fields (for example ``order_id``) are repeated across expanded rows.

Example 6: Empty Collections and Null-Like Values
-------------------------------------------------

This example highlights how empty lists and empty nested objects are handled.

.. code-block:: python

	from json2df.json2df import DeepNestedHandler

	payload = {
		 "name": "sample",
		 "tags": [],
		 "meta": {}
	}

	df = DeepNestedHandler(json_data=payload).convert_to_df()
	print(df)

Expected behavior:

- Empty list fields are represented as ``NaN``.
- Empty dicts do not add nested columns by themselves.

Example 7: Tuple Support
------------------------

Tuple values are treated similarly to lists.

.. code-block:: python

	from json2df.json2df import DeepNestedHandler

	payload = {
		 "session_id": "S-1",
		 "scores": (10, 20, 30)
	}

	df = DeepNestedHandler(json_data=payload).convert_to_df()
	print(df)

Expected behavior:

- Tuple items can expand row-wise like list values.

Example 8: Validate Output Programmatically
-------------------------------------------

Use assertions to verify conversion quality in scripts and tests.

.. code-block:: python

	import pandas as pd
	from json2df.json2df import LoadInfo, DeepNestedHandler

	payload = LoadInfo(file="test/data/fruit_metadata.json").get_data()
	df = DeepNestedHandler(payload).convert_to_df()

	assert isinstance(df, pd.DataFrame)
	assert not df.empty
	assert len(df.columns) > 0

	print("Validation passed")

Batch Conversion Pattern
------------------------

To quickly inspect multiple fixture files:

.. code-block:: python

	from pathlib import Path
	from json2df.json2df import LoadInfo, DeepNestedHandler

	data_dir = Path("test/data")
	for json_file in sorted(data_dir.glob("*.json")):
		 payload = LoadInfo(file=json_file).get_data()
		 df = DeepNestedHandler(payload).convert_to_df()
		 print(f"{json_file.name}: rows={len(df)}, cols={len(df.columns)}")

Troubleshooting Tips
--------------------

- If ``LoadInfo`` fails, confirm your input is valid ``dict``, ``list``, or JSON string.
- If file loading fails, ensure the path is correct relative to your current working directory.
- If output row count is higher than expected, inspect list-valued fields in your JSON.
- If columns are sparse, this usually means list items or records have different schemas.

See Also
--------

- ``getting_started`` for installation and first-run setup
- ``api_reference`` for class and method details
- ``testing_and_validation`` for pytest-based verification workflows
