.. _getting_started:

Getting Started
===============

This guide helps you install JsonToFrame and run your first JSON to DataFrame conversion.

What You Will Learn
-------------------

- How to install the package
- Which Python version and dependencies are required
- How to load data from a file, string, or Python object
- How to flatten nested JSON into a pandas DataFrame
- What output behavior to expect for nested lists and empty values

Prerequisites
-------------

Before you begin, make sure you have:

- Python 3.10 or newer
- pip available in your environment
- Basic familiarity with pandas DataFrame operations

Installation
------------

Install from the project:

.. code-block:: bash

	pip install json-to-frame

To verify installation:

.. code-block:: bash

	python -c "import pandas; from json2df.json2df import LoadInfo, DeepNestedHandler; print('ok')"

Your First Conversion
---------------------

The simplest workflow has two steps:

1. Load JSON-compatible input
2. Convert nested data to a DataFrame

Example using a JSON file:

.. code-block:: python

	from json2df.json2df import LoadInfo, DeepNestedHandler

	payload = LoadInfo(file="test/data/svg_example.json").get_data()
	df = DeepNestedHandler(json_data=payload).convert_to_df()

	print(df.head())
	print(df.shape)

Supported Input Sources
-----------------------

LoadInfo accepts:

- Python dict or list passed as info
- JSON string passed as info
- JSON file path passed as file

Example with a Python dictionary:

.. code-block:: python

	from json2df.json2df import LoadInfo, DeepNestedHandler

	payload = {
		 "name": "John",
		 "cars": [
			  {"model": "BMW 230", "mpg": 27.5},
			  {"model": "Ford Edge", "mpg": 24.1}
		 ]
	}

	normalized = LoadInfo(info=payload).get_data()
	df = DeepNestedHandler(json_data=normalized).convert_to_df()
	print(df)

Example with a JSON string:

.. code-block:: python

	from json2df.json2df import LoadInfo, DeepNestedHandler

	raw_json = '{"team":"A","members":[{"name":"Ana"},{"name":"Lee"}]}'
	normalized = LoadInfo(info=raw_json).get_data()
	df = DeepNestedHandler(json_data=normalized).convert_to_df()
	print(df)

How Flattening Works
--------------------

DeepNestedHandler converts nested keys into flat column names using underscores.

For example, an input like:

.. code-block:: json

	{
	  "user": {
		 "profile": {
			"age": 30
		 }
	  }
	}

can produce a column similar to:

- user_profile_age

Important behavior:

- Top-level lists are processed item-by-item and concatenated into one DataFrame
- Empty lists are represented as NaN for the related field
- Nested dictionaries are recursively expanded into prefixed column names
- Internal join logic is removed before final output is returned

Common Errors and Fixes
-----------------------

ValueError while loading data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Likely causes:

- file is missing when using file input
- info is neither dict, list, nor valid JSON string

Fix:

- Provide a valid file path, or
- Provide a valid dict, list, or JSON string

JSON decoding errors
^^^^^^^^^^^^^^^^^^^^

Likely cause:

- malformed JSON string input

Fix:

- Validate the string with a JSON validator
- Ensure double quotes are used for JSON keys and string values

Unexpected row expansion
^^^^^^^^^^^^^^^^^^^^^^^^

Likely cause:

- list fields produce multiple rows by design

Fix:

- Inspect list-valued keys in your input
- Aggregate or group the resulting DataFrame as needed

Quick Validation
----------------

After conversion, validate basic output shape and columns:

.. code-block:: python

	import pandas as pd
	from json2df.json2df import LoadInfo, DeepNestedHandler

	payload = LoadInfo(file="test/data/user_household_data.json").get_data()
	df = DeepNestedHandler(payload).convert_to_df()

	assert isinstance(df, pd.DataFrame)
	assert not df.empty
	assert len(df.columns) > 0

Next Steps
----------

- Continue with usage_examples for real-world conversion patterns
- See api_reference for class and method-level details
- Review testing_and_validation to run fixture-based checks
