.. _home:

JsonToFrame Documentation
=========================

JsonToFrame converts nested JSON-like payloads into flat pandas DataFrames.
It is useful when API responses or deeply nested structures need to be analyzed
in tabular form.

Key Features
------------

- Accepts Python dict/list inputs, JSON strings, and JSON files.
- Flattens nested dictionaries using underscore-separated column names.
- Expands list-like structures into row-wise DataFrame output.
- Supports mixed nested data (dict, list, tuple, scalar, empty collections).
- Produces pandas DataFrame output directly for analysis and export workflows.

Quick Example
-------------

.. code-block:: python

   from json2df.json2df import LoadInfo, DeepNestedHandler

   payload = LoadInfo(file="test/data/svg_example.json").get_data()
   df = DeepNestedHandler(json_data=payload).convert_to_df()
   print(df.head())

How It Works
------------

1. LoadInfo normalizes input from a Python object, JSON string, or JSON file.
2. DeepNestedHandler recursively walks nested structures.
3. Nested keys are flattened into column names using underscore separators.
4. List/tuple values are expanded and concatenated into row-level output.
5. Internal join keys are removed before final DataFrame return.

Input and Behavior Notes
------------------------

- Top-level list payloads are converted item-by-item, then concatenated.
- Empty lists are represented using NaN in the relevant output column.
- Nested conversion expects mapping-like objects where required.
- Invalid loader input raises ValueError during normalization/parsing.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :hidden:

   getting-started
   usage-examples
   api-reference
   testing-and-validation
   development-notes