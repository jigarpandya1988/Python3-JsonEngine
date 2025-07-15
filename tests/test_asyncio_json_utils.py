import pytest

from src.json_utils.asyncio_json_utils import JSONUtilsAsync


@pytest.mark.asyncio
async def test_async_save_and_load(tmp_path):
    paths = [tmp_path / f"async_test_{i}.json" for i in range(5)]
    data_pairs = [(str(p), {"async": i}) for i, p in enumerate(paths)]

    # Save asynchronously
    written_files = await JSONUtilsAsync.save_multiple_json_files(data_pairs, indent=2)
    assert len(written_files) == 5

    # Load asynchronously
    loaded_files = await JSONUtilsAsync.load_multiple_json_files(
        [str(p) for p in paths]
    )
    for i, path in enumerate(paths):
        assert loaded_files[str(path)] == {"async": i}


@pytest.mark.asyncio
async def test_async_invalid_file(tmp_path):
    invalid_path = tmp_path / "does_not_exist.json"
    result = await JSONUtilsAsync.load_json_from_file(invalid_path)
    assert result is None


@pytest.mark.asyncio
async def test_async_save_invalid_path():
    result = await JSONUtilsAsync.save_json_to_file({"x": 1}, "?:/invalid/path.json")
    assert result is None
