# JSON to Pandas Dataframe

Convert nested JSON objects into flat pandas DataFrames with a simple Python API.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Overview

This package helps you transform JSON-like payloads into tabular data that is easier to inspect, analyze, and export.

It supports:

- Python dictionaries and lists
- JSON strings
- JSON files
- Deeply nested structures containing dicts, lists, tuples, scalars, `null`, and empty collections

## Installation

Install from source in editable mode:

```bash
pip install -e .
```

Or install runtime dependencies directly:

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from json2df.json2df import DeepNestedHandler, LoadInfo

json_file = "data/svg_example.json"
payload = LoadInfo(file=json_file).get_data()

df = DeepNestedHandler(json_data=payload).convert_to_df()
print(df.head())
```

## API

### `LoadInfo`

Loads JSON-compatible input from either:

- `info`: a Python `dict`/`list` or JSON `str`
- `file`: path to a JSON file

Example:

```python
from json2df.json2df import LoadInfo

payload_from_file = LoadInfo(file="data/sample_donut_data.json").get_data()
payload_from_str = LoadInfo(info='{"a": 1, "b": 2}').get_data()
```

### `DeepNestedHandler`

Flattens nested data into a pandas DataFrame.

Example:

```python
from json2df.json2df import DeepNestedHandler

payload = {
      "name": "John",
      "cars": [
            {"model": "BMW 230", "mpg": 27.5},
            {"model": "Ford Edge", "mpg": 24.1}
      ]
}

df = DeepNestedHandler(payload).convert_to_df()
print(df)
```

## Behavior Notes

- Nested keys are flattened using underscore-separated paths.
- Arrays generate multiple rows when needed.
- For top-level JSON arrays, each item is flattened and concatenated.
- Empty lists are represented with `NaN` values in the corresponding column.

## Running Tests

Run all tests:

```bash
python3 -m pytest -v
```

Run fixture coverage tests only:

```bash
python3 -m pytest -v test/test/test_json_fixtures.py
```

If you want to view DataFrame output from `print(...)` statements during tests:

```bash
python3 -m pytest -v -s test/test/test_json_fixtures.py
```

## Project Structure

```text
src/json2df/
   __init__.py
   json2df.py
test/data/
   *.json
test/test/
   test_json_fixtures.py
```

## License

MIT License.

