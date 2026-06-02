from pathlib import Path

import pandas as pd
import pytest

from json2df.json2df import DeepNestedHandler, LoadInfo


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
JSON_FILES = sorted(DATA_DIR.glob("*.json"))


@pytest.mark.parametrize("json_file", JSON_FILES, ids=lambda p: p.name)
def test_each_fixture_converts_to_dataframe(json_file: Path) -> None:
    payload = LoadInfo(file=json_file).get_data()
    frame = DeepNestedHandler(payload).convert_to_df()
    print(f"Testing {json_file.name}...")
    print(frame.head())

    assert isinstance(frame, pd.DataFrame)
    assert not frame.empty
    assert len(frame.columns) > 0


def test_parametrization_covers_all_json_fixtures() -> None:
    discovered = {p.name for p in JSON_FILES}
    expected = {p.name for p in DATA_DIR.iterdir() if p.suffix == ".json"}
    assert discovered == expected
