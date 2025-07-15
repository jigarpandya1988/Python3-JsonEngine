import pytest

from src.json_utils.multiprocessing_json_utils import JSONUtilsProcess


def test_process_save_and_load(tmp_path):
    paths = [tmp_path / f"process_test_{i}.json" for i in range(3)]
    data_pairs = [(str(p), {"index": i}) for i, p in enumerate(paths)]

    written = JSONUtilsProcess.save_multiple_json_files(data_pairs, workers=2, indent=2)
    assert len(written) == 3

    loaded = JSONUtilsProcess.load_multiple_json_files(
        [str(p) for p in paths], workers=2
    )
    for i, path in enumerate(paths):
        assert loaded[str(path)] == {"index": i}


def test_process_load_invalid_json(tmp_path):
    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text("{ invalid json ")

    result = JSONUtilsProcess.load_multiple_json_files([str(invalid_file)], workers=2)
    assert result[str(invalid_file)] is None


def test_process_save_invalid_path():
    result = JSONUtilsProcess.save_multiple_json_files(
        [("Z:/this/path/does/not/exist.json", {"fail": True})], workers=2
    )
    assert result == []
