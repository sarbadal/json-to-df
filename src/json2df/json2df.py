import json
from functools import singledispatchmethod
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

class LoadInfo:
    """Load JSON-like input from a Python object, JSON string, or file path."""

    def __init__(self, info: Any = None, file: str | Path | None = None):
        self._info = info
        self._file = Path(file) if file is not None else None
        self._config = self._load_config()

    def get_data(self):
        return self._config

    def load_from_file(self):
        if self._file is None:
            raise ValueError("File path is required when loading from file.")

        with open(self._file, mode="r", encoding="utf-8") as file_obj:
            return json.load(file_obj)

    def load_from_str(self):
        if isinstance(self._info, (dict, list)):
            return self._info
        if isinstance(self._info, str):
            return json.loads(self._info)

        raise ValueError("Load config error")

    def _load_config(self):
        if self._info is not None:
            return self.load_from_str()
        return self.load_from_file()


class DeepNestedHandler:
    """Convert nested JSON-like data into a flattened pandas DataFrame."""
    _JOIN_KEY = "jkey_"

    def __init__(self, json_data: Any):
        self._json_data = json_data

    @property
    def json_data(self):
        return self._json_data

    def _new_join_key_frame(self) -> pd.DataFrame:
        return pd.DataFrame({self._JOIN_KEY: [1]})

    def _merge_with_master(self, master_df: pd.DataFrame, incoming_df: pd.DataFrame) -> pd.DataFrame:
        return pd.merge(master_df, incoming_df, how="inner", on=self._JOIN_KEY)

    def _field_name(self, prefix: str, key: str) -> str:
        return key if not prefix else f"{prefix}_{key}"

    def _normalize_dict_input(self, data_: Any | None) -> dict[str, Any]:
        payload = LoadInfo(self.json_data if data_ is None else data_).get_data()
        if not isinstance(payload, dict):
            raise ValueError("Nested conversion requires a dictionary-like object.")
        return payload

    @singledispatchmethod
    def _value_to_frame(self, value: Any, field_name: str) -> pd.DataFrame:
        return pd.DataFrame({field_name: [value], self._JOIN_KEY: [1]})

    @_value_to_frame.register(dict)
    def _(self, value: dict, field_name: str) -> pd.DataFrame:
        if not value:
            return self._new_join_key_frame()
        return self._flatten_mapping(value, prefix=field_name)

    @_value_to_frame.register(list)
    @_value_to_frame.register(tuple)
    def _(self, value: list | tuple, field_name: str) -> pd.DataFrame:
        if not value:
            return pd.DataFrame({field_name: [np.nan], self._JOIN_KEY: [1]})

        item_frames: list[pd.DataFrame] = []
        for item in value:
            if isinstance(item, dict):
                if item:
                    item_frames.append(self._flatten_mapping(item, prefix=field_name))
                else:
                    # Preserve existing behavior: empty dict in a list is treated as a scalar value.
                    item_frames.append(pd.DataFrame({field_name: [item], self._JOIN_KEY: [1]}))
            else:
                item_frames.append(self._value_to_frame(item, field_name))

        return pd.concat(item_frames, axis=0, ignore_index=True, sort=False)

    def _flatten_mapping(self, payload: dict[str, Any], prefix: str = "") -> pd.DataFrame:
        frame = self._new_join_key_frame()
        for key, value in payload.items():
            field_name = self._field_name(prefix, key)
            value_frame = self._value_to_frame(value, field_name)
            frame = self._merge_with_master(frame, value_frame)
        return frame

    def _json_to_df(self, data_: Any = None, col_pre_fix: str = "", **kwargs: Any) -> pd.DataFrame:
        """Recursively flatten one dictionary node into a DataFrame."""
        parsed_data = self._normalize_dict_input(data_)
        master_df = kwargs.get("master_df", self._new_join_key_frame())

        flattened_node = self._flatten_mapping(parsed_data, prefix=col_pre_fix)
        return self._merge_with_master(master_df, flattened_node)

    def convert_to_df(self):
        info = LoadInfo(self.json_data).get_data()
        if isinstance(info, list):
            frame_list = [self._json_to_df(item) for item in info]
            merged_frame = pd.concat(frame_list, axis=0, ignore_index=True, sort=False)
            merged_frame.drop(self._JOIN_KEY, axis=1, inplace=True)
            return merged_frame

        frame = self._json_to_df(self.json_data)
        frame.drop(self._JOIN_KEY, axis=1, inplace=True)
        return frame

