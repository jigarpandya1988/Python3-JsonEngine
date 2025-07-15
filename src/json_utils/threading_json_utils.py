import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Union


class JSONUtils:
    """
    Utility class for JSON operations: validation, normalization, concurrent operations, async, and pretty-print.
    """

    @staticmethod
    def load_json_from_file(
        file_path: str, encoding: str = "utf-8", errors: str = "strict"
    ) -> Union[Dict[str, Any], List[Any]]:
        """
        Load JSON data from a file.

        Args:
            file_path (str): Path to the JSON file.
            encoding (str): File encoding.
            errors (str): Error handling strategy.

        Returns:
            Union[Dict[str, Any], List[Any]]: Parsed JSON data as dict or list.
        """
        with open(file_path, "r", encoding=encoding, errors=errors) as f:
            return json.load(f)

    @staticmethod
    def save_json_to_file(
        data: Union[Dict[str, Any], List[Any]],
        file_path: str,
        indent: int = 4,
        encoding: str = "utf-8",
        ensure_ascii: bool = False,
        **kwargs,
    ) -> None:
        """
        Save JSON data to a file.

        Args:
            data (dict or list): JSON-serializable data.
            file_path (str): Path to the output file.
            indent (int): Indentation level for pretty-printing.
            encoding (str): File encoding.
            ensure_ascii (bool): Escape non-ASCII characters.
            **kwargs: Additional arguments for json.dump.

        Returns:
            None
        """
        with open(file_path, "w", encoding=encoding) as f:
            json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii, **kwargs)

    @staticmethod
    def load_json_from_string(json_string: str) -> Union[Dict[str, Any], List[Any]]:
        """
        Parse JSON from a string.

        Args:
            json_string (str): JSON string.

        Returns:
            Union[Dict[str, Any], List[Any]]: Parsed JSON object.
        """
        return json.loads(json_string)

    @staticmethod
    def to_pretty_string(
        data: Union[Dict[str, Any], List[Any]],
        indent: int = 4,
        ensure_ascii: bool = False,
        **kwargs,
    ) -> str:
        """
        Convert JSON data to a pretty-printed string.

        Args:
            data (dict or list): JSON-serializable data.
            indent (int): Indentation level.
            ensure_ascii (bool): Escape non-ASCII characters.
            **kwargs: Additional arguments for json.dumps.

        Returns:
            str: Pretty-printed JSON string.
        """
        return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii, **kwargs)

    @staticmethod
    def update_json_key(data: Dict[str, Any], key: str, value: Any) -> Dict[str, Any]:
        """
        Update or add a key-value pair in a JSON dictionary.

        Args:
            data (dict): JSON dictionary.
            key (str): Key to update or add.
            value (Any): Value to set.

        Returns:
            dict: Updated dictionary.
        """
        data[key] = value
        return data

    @staticmethod
    def remove_json_key(data: Dict[str, Any], key: str) -> Dict[str, Any]:
        """
        Remove a key from JSON if it exists.

        Args:
            data (dict): JSON dictionary.
            key (str): Key to remove.

        Returns:
            dict: Dictionary after key removal.
        """
        if key in data:
            del data[key]
        return data

    @staticmethod
    def merge_json(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge two dictionaries; dict2 values overwrite dict1.

        Args:
            dict1 (dict): Base dictionary.
            dict2 (dict): Dictionary with updates.

        Returns:
            dict: Merged dictionary.
        """
        result = dict1.copy()
        result.update(dict2)
        return result

    @staticmethod
    def search_nested_key(
        data: Union[Dict[str, Any], List[Any]], search_key: str
    ) -> List[Any]:
        """
        Search nested JSON for all values associated with a specific key.

        Args:
            data (dict or list): JSON structure.
            search_key (str): Key to search for.

        Returns:
            list: Found values.
        """
        found = []
        stack = [data]

        while stack:
            current = stack.pop()
            if isinstance(current, dict):
                for k, v in current.items():
                    if k == search_key:
                        found.append(v)
                    stack.append(v)
            elif isinstance(current, list):
                stack.extend(current)

        return found

    @staticmethod
    def flatten_json(
        data: Dict[str, Any], parent_key: str = "", sep: str = "."
    ) -> Dict[str, Any]:
        """
        Flatten nested JSON into a single-level dictionary.

        Args:
            data (dict): Nested dictionary.
            parent_key (str): Prefix for recursive keys.
            sep (str): Separator for keys.

        Returns:
            dict: Flattened dictionary.
        """
        items = {}
        stack = [(data, parent_key)]

        while stack:
            current, parent = stack.pop()
            if isinstance(current, dict):
                for k, v in current.items():
                    new_key = f"{parent}{sep}{k}" if parent else k
                    stack.append((v, new_key))
            elif isinstance(current, list):
                for i, v in enumerate(current):
                    new_key = f"{parent}{sep}{i}" if parent else str(i)
                    stack.append((v, new_key))
            else:
                items[parent] = current

        return items

    @staticmethod
    def unflatten_json(flat_data: Dict[str, Any], sep: str = ".") -> Dict[str, Any]:
        """
        Convert flat dot-separated dictionary to nested JSON.

        Args:
            flat_data (dict): Flattened dictionary.
            sep (str): Separator used in keys.

        Returns:
            dict: Nested JSON dictionary.
        """
        nested: Dict[str, Any] = {}

        for compound_key, value in flat_data.items():
            keys = compound_key.split(sep)
            d = nested
            for key in keys[:-1]:
                if key not in d:
                    d[key] = {}
                d = d[key]
            d[keys[-1]] = value

        return nested

    @staticmethod
    def encode_to_bytes(
        data: Union[Dict[str, Any], List[Any]], encoding: str = "utf-8", **kwargs
    ) -> bytes:
        """
        Encode JSON to bytes.

        Args:
            data (dict or list): JSON data.
            encoding (str): Encoding type.
            **kwargs: Additional json.dump args.

        Returns:
            bytes: Encoded bytes.
        """
        json_str = json.dumps(data, **kwargs)
        return json_str.encode(encoding)

    @staticmethod
    def decode_from_bytes(
        data_bytes: bytes, encoding: str = "utf-8", **kwargs
    ) -> Union[Dict[str, Any], List[Any]]:
        """
        Decode bytes into JSON.

        Args:
            data_bytes (bytes): JSON encoded bytes.
            encoding (str): Encoding used.
            **kwargs: Additional json.load args.

        Returns:
            dict or list: Decoded JSON data.
        """
        json_str = data_bytes.decode(encoding)
        return json.loads(json_str, **kwargs)

    # -------------------- Concurrent Methods --------------------

    @staticmethod
    def load_multiple_json_files(
        file_paths: List[str], max_workers: int = 10
    ) -> Dict[str, Union[Dict[str, Any], List[Any], None]]:
        """
        Concurrently load multiple JSON files.

        Args:
            file_paths (list): List of file paths to load.
            max_workers (int): Maximum threads for concurrent reading.

        Returns:
            dict: Mapping of file path to loaded data or None on failure.
        """
        results = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(JSONUtils._load_file_helper, path)
                for path in file_paths
            ]
            for future in as_completed(futures):
                path, data = future.result()
                results[path] = data
        return results

    @staticmethod
    def save_multiple_json_files(
        file_data_pairs: List[tuple[str, Union[Dict[str, Any], List[Any]]]],
        max_workers: int = 10,
        **kwargs,
    ) -> List[str]:
        """
        Concurrently write multiple JSON files.

        Args:
            file_data_pairs (list): List of (file path, data) tuples.
            max_workers (int): Maximum threads for concurrent writing.
            **kwargs: Additional json.dump args.

        Returns:
            list: File paths successfully written.
        """
        success_paths = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(JSONUtils._save_file_helper, path, data, kwargs)
                for path, data in file_data_pairs
            ]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    success_paths.append(result)
        return success_paths

    @staticmethod
    def _load_file_helper(
        path: str,
    ) -> tuple[str, Union[Dict[str, Any], List[Any], None]]:
        """
        Helper to load a JSON file, wrapped for concurrency.

        Args:
            path (str): Path to the JSON file.

        Returns:
            tuple: (path, loaded data or None)
        """
        try:
            data = JSONUtils.load_json_from_file(path)
            return path, data
        except Exception:
            return path, None

    @staticmethod
    def _save_file_helper(path: str, data: Any, kwargs: dict) -> Union[str, None]:
        """
        Helper to save JSON to a file, wrapped for concurrency.

        Args:
            path (str): Output file path.
            data (dict or list): JSON data to save.
            kwargs (dict): Arguments passed to json.dump.

        Returns:
            str or None: Path if successful, None otherwise.
        """
        try:
            JSONUtils.save_json_to_file(data, path, **kwargs)
            return path
        except Exception:
            return None

    # -------------------- Additional Methods --------------------

    @staticmethod
    def is_valid_json_string(json_string: str) -> bool:
        """
        Validate if a string is valid JSON.

        Args:
            json_string (str): String to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        try:
            json.loads(json_string)
            return True
        except json.JSONDecodeError:
            return False

    @staticmethod
    def is_valid_json_file(file_path: str, encoding: str = "utf-8") -> bool:
        """
        Validate if a file contains valid JSON.

        Args:
            file_path (str): File path to validate.
            encoding (str): File encoding.

        Returns:
            bool: True if valid, False otherwise.
        """
        try:
            with open(file_path, "r", encoding=encoding) as f:
                json.load(f)
            return True
        except Exception:
            return False

    @staticmethod
    def pretty_print(
        data: Union[Dict[str, Any], List[Any]],
        indent: int = 4,
        ensure_ascii: bool = False,
    ) -> None:
        """
        Pretty-print JSON to console.

        Args:
            data (dict or list): JSON data.
            indent (int): Indentation level.
            ensure_ascii (bool): Escape non-ASCII characters.

        Returns:
            None
        """
        print(json.dumps(data, indent=indent, ensure_ascii=ensure_ascii))

    @staticmethod
    def diff_json(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Find key differences between two JSON dictionaries.

        Args:
            dict1 (dict): First dictionary.
            dict2 (dict): Second dictionary.

        Returns:
            dict: Keys where values differ with old/new values.
        """
        diff = {}
        for key in set(dict1) | set(dict2):
            if dict1.get(key) != dict2.get(key):
                diff[key] = {"old": dict1.get(key), "new": dict2.get(key)}
        return diff

    @staticmethod
    def normalize_keys_to_string(data: Any) -> Any:
        """
        Recursively convert all dictionary keys to strings.

        Args:
            data (Any): JSON data (dict, list, scalar).

        Returns:
            Any: Same structure with all dict keys as strings.
        """
        if isinstance(data, dict):
            return {
                str(k): JSONUtils.normalize_keys_to_string(v) for k, v in data.items()
            }
        elif isinstance(data, list):
            return [JSONUtils.normalize_keys_to_string(i) for i in data]
        return data

    @staticmethod
    def load_all_json_files_from_dir(
        directory: str, recursive: bool = True
    ) -> Dict[str, Union[Dict[str, Any], List[Any], None]]:
        """
        Load all JSON files from a directory.

        Args:
            directory (str): Directory path.
            recursive (bool): Recursively include subdirectories.

        Returns:
            dict: Mapping of file path to loaded JSON data.
        """
        paths = (
            list(Path(directory).rglob("*.json"))
            if recursive
            else list(Path(directory).glob("*.json"))
        )
        return JSONUtils.load_multiple_json_files([str(p) for p in paths])
