import pytest

from src.json_utils.threading_json_utils import JSONUtils


def test_thread_save_and_load(tmp_path):
    file_path = tmp_path / "test.json"
    data = {"engine": "v8", "power": 450}

    JSONUtils.save_json_to_file(data, file_path)
    loaded = JSONUtils.load_json_from_file(file_path)

    assert loaded == data


def test_thread_load_from_string_and_pretty():
    data = {"speed": 200}
    json_str = '{"speed": 200}'
    loaded = JSONUtils.load_json_from_string(json_str)

    assert loaded == data
    pretty = JSONUtils.to_pretty_string(loaded)
    assert isinstance(pretty, str)
    assert "speed" in pretty


def test_thread_flatten_unflatten():
    nested = {"car": {"type": "sedan", "engine": {"power": 300}}}
    flat = JSONUtils.flatten_json(nested)
    expected = {"car.type": "sedan", "car.engine.power": 300}
    assert flat == expected

    unflat = JSONUtils.unflatten_json(flat)
    assert unflat == nested


def test_thread_search_nested_key():
    data = {"a": {"b": {"target": 1}}, "target": 2}
    found = JSONUtils.search_nested_key(data, "target")
    assert sorted(found) == [1, 2]


def test_thread_update_remove_merge():
    data = {"a": 1}
    updated = JSONUtils.update_json_key(data, "b", 2)
    assert updated["b"] == 2

    removed = JSONUtils.remove_json_key(updated, "b")
    assert "b" not in removed

    merged = JSONUtils.merge_json({"x": 1}, {"x": 2, "y": 3})
    assert merged == {"x": 2, "y": 3}


def test_thread_diff_json():
    a = {"x": 1, "y": 2}
    b = {"x": 2, "z": 3}
    diff = JSONUtils.diff_json(a, b)
    assert diff == {
        "x": {"old": 1, "new": 2},
        "y": {"old": 2, "new": None},
        "z": {"old": None, "new": 3},
    }


def test_thread_encode_decode_bytes():
    data = {"fuel": "diesel"}
    encoded = JSONUtils.encode_to_bytes(data)
    decoded = JSONUtils.decode_from_bytes(encoded)
    assert decoded == data


def test_thread_validation(tmp_path):
    valid_json_str = '{"valid": true}'
    invalid_json_str = '{"valid": true'

    assert JSONUtils.is_valid_json_string(valid_json_str)
    assert not JSONUtils.is_valid_json_string(invalid_json_str)

    valid_file = tmp_path / "valid.json"
    invalid_file = tmp_path / "invalid.json"

    valid_file.write_text(valid_json_str)
    invalid_file.write_text(invalid_json_str)

    assert JSONUtils.is_valid_json_file(valid_file)
    assert not JSONUtils.is_valid_json_file(invalid_file)


def test_thread_pretty_print(capsys):
    data = {"pretty": True}
    JSONUtils.pretty_print(data)
    captured = capsys.readouterr()
    assert "pretty" in captured.out
    assert "true" in captured.out  # JSON lowercase


def test_thread_normalize_keys():
    raw = {1: {"nested": True}, (2, 3): "value"}
    normalized = JSONUtils.normalize_keys_to_string(raw)
    assert "1" in normalized
    assert "(2, 3)" in normalized


def test_thread_load_all_json_files_from_dir(tmp_path):
    paths = [tmp_path / f"file_{i}.json" for i in range(3)]
    for i, path in enumerate(paths):
        path.write_text('{"index": %d}' % i)

    result = JSONUtils.load_all_json_files_from_dir(tmp_path)
    assert len(result) == 3
    for path in paths:
        assert "index" in result[str(path)]


def test_thread_load_empty_list():
    assert JSONUtils.load_multiple_json_files([]) == {}


def test_thread_save_empty_list():
    assert JSONUtils.save_multiple_json_files([]) == []


def test_thread_load_invalid_json(tmp_path):
    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text("NOT JSON")
    result = JSONUtils.load_multiple_json_files([str(invalid_file)])
    assert result[str(invalid_file)] is None


def test_thread_save_invalid_path():
    result = JSONUtils.save_multiple_json_files(
        [("Z:/this/path/does/not/exist.json", {"fail": True})]
    )
    assert result == []
