from pathlib import Path
from pydanticio import decide_data_format_from_path

from pytest import raises


def test_decide_data_format_from_path():
    assert decide_data_format_from_path(Path("test.csv")) == "csv"
    assert decide_data_format_from_path(Path("test.json")) == "json"
    assert decide_data_format_from_path(Path("test.jsonl")) == "json_lines"

    with raises(ValueError):
        decide_data_format_from_path(Path("test.txt"))

    with raises(ValueError):
        decide_data_format_from_path(Path("test"))

    with raises(ValueError):
        decide_data_format_from_path(Path("test."))
