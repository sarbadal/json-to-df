.. _api_reference:

.. currentmodule:: json2df.json2df

API Reference
=============

This page documents the public API used to normalize JSON-like inputs and
convert nested structures into flat pandas DataFrames.

Module
------

Primary module:

- ``json2df.json2df``

Public classes:

- :class:`LoadInfo`
- :class:`DeepNestedHandler`

LoadInfo
--------

.. py:class:: LoadInfo(info: Any = None, file: str | pathlib.Path | None = None)

	Load JSON-compatible input from one of the following sources:

	- Python ``dict`` or ``list`` provided through ``info``
	- JSON string provided through ``info``
	- JSON file path provided through ``file``

	Exactly one source should be provided for predictable behavior.

	:param info: In-memory JSON payload or JSON string.
	:type info: Any
	:param file: Path to a JSON file.
	:type file: str | pathlib.Path | None

	Notes:

	- If ``info`` is provided, it is preferred over ``file``.
	- File paths are converted to ``pathlib.Path`` internally.

.. py:method:: get_data()

	Return the normalized payload loaded during object initialization.

	:returns: Parsed JSON-compatible data.
	:rtype: Any

.. py:method:: load_from_file()

	Read and parse JSON data from ``file``.

	:raises ValueError: If ``file`` was not provided.
	:raises FileNotFoundError: If the given file path does not exist.
	:raises json.JSONDecodeError: If file contents are not valid JSON.
	:returns: Parsed JSON payload.
	:rtype: Any

.. py:method:: load_from_str()

	Parse ``info`` when it is a supported in-memory type.

	Behavior:

	- If ``info`` is ``dict`` or ``list``, it is returned unchanged.
	- If ``info`` is ``str``, it is parsed as JSON.

	:raises ValueError: If ``info`` is not a dict, list, or JSON string.
	:raises json.JSONDecodeError: If ``info`` is a malformed JSON string.
	:returns: Parsed or passthrough payload.
	:rtype: Any

DeepNestedHandler
-----------------

.. py:class:: DeepNestedHandler(json_data: Any)

	Convert nested JSON-like structures to a flattened pandas DataFrame.

	:param json_data: Input payload as dict, list, JSON string, or JSON-like value.
	:type json_data: Any

	Flattening behavior summary:

	- Nested dictionary keys are flattened with underscore-separated names.
	- Lists and tuples expand into row-wise records when needed.
	- Top-level list input is converted item-by-item, then concatenated.
	- Empty lists produce ``NaN`` in the related flattened column.

.. py:attribute:: json_data

	Read-only property returning the original payload passed at initialization.

	:rtype: Any

.. py:method:: convert_to_df()

	Convert input payload to a flattened DataFrame.

	Top-level input behavior:

	- ``dict``: flattened as a single object conversion path.
	- ``list``: each item is flattened and rows are concatenated.

	Internal join columns used for merge operations are removed before returning.

	:raises ValueError: If a nested conversion path receives non-dict where dict is required.
	:returns: Flattened DataFrame.
	:rtype: pandas.DataFrame

Data Flattening Rules
---------------------

Key naming
^^^^^^^^^^

- Child keys are prefixed with parent names using underscores.
- Example: ``{"user": {"profile": {"age": 30}}}`` becomes a column like
  ``user_profile_age``.

Scalar values
^^^^^^^^^^^^^

- Scalars are stored as single-value columns.

Dictionary values
^^^^^^^^^^^^^^^^^

- Non-empty dictionaries are recursively flattened.
- Empty dictionaries preserve join continuity and may not add new columns.

List and tuple values
^^^^^^^^^^^^^^^^^^^^^

- Non-empty list/tuple values are expanded item by item.
- List items that are dictionaries are flattened recursively.
- Empty list values produce ``NaN`` in the related field.
- Empty dictionaries inside a list are preserved as scalar ``{}`` entries.

Top-level list inputs
^^^^^^^^^^^^^^^^^^^^^

- The converter expects each top-level list item to be dictionary-like for nested
  flattening.
- Heterogeneous schemas are supported; missing fields appear as ``NaN``.

Exceptions and Error Surface
----------------------------

Most common exceptions to handle at integration points:

- ``ValueError``:
  - Missing file path when file loading is requested.
  - Unsupported ``info`` type in ``LoadInfo``.
  - Nested conversion requires dictionary-like objects.
- ``json.JSONDecodeError``:
  - Malformed JSON string or invalid JSON file contents.
- ``FileNotFoundError``:
  - Non-existent input path passed via ``file``.

Recommended handling pattern:

.. code-block:: python

	import json
	from json2df.json2df import LoadInfo, DeepNestedHandler

	try:
		 payload = LoadInfo(file="test/data/svg_example.json").get_data()
		 df = DeepNestedHandler(payload).convert_to_df()
	except (ValueError, FileNotFoundError, json.JSONDecodeError) as exc:
		 print(f"Conversion failed: {exc}")

Version Notes
-------------

- Current documented API corresponds to the implementation in
  ``src/json2df/json2df.py``.
- If class names or signatures change, update this page and examples in
  ``usage_examples`` accordingly.
