import json
from multiprocessing import Pool
from typing import Any, Dict, List, Tuple, Union


def load_json_file(path: str) -> Union[Dict[str, Any], List[Any], None]:
    """
    Load JSON from a file.

    Args:
        path (str): Path to the JSON file.

    Returns:
        dict or list or None: Parsed JSON data, or None on failure.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save_json_file(
    args: Tuple[str, Union[Dict[str, Any], List[Any]], Dict[str, Any]],
) -> Union[str, None]:
    """
    Save JSON to a file.

    Args:
        args (tuple):
            path (str): Output file path.
            data (dict or list): JSON-serializable data.
            kwargs (dict): Additional arguments for json.dump.

    Returns:
        str or None: File path if successful, None otherwise.
    """
    path, data, kwargs = args
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, **kwargs)
        return path
    except Exception:
        return None


class JSONUtilsProcess:
    """
    JSON utility for high-load concurrent processing via multiprocessing.
    """

    @staticmethod
    def load_multiple_json_files(
        file_paths: List[str], workers: int = 4
    ) -> Dict[str, Union[Dict[str, Any], List[Any], None]]:
        """
        Concurrently load multiple JSON files using multiprocessing.

        Args:
            file_paths (list): List of file paths.
            workers (int): Number of parallel processes.

        Returns:
            dict: Mapping of file path to loaded JSON or None on failure.
        """
        with Pool(processes=workers) as pool:
            results = pool.map(load_json_file, file_paths)

        return {path: data for path, data in zip(file_paths, results)}

    @staticmethod
    def save_multiple_json_files(
        file_data_pairs: List[Tuple[str, Union[Dict[str, Any], List[Any]]]],
        workers: int = 4,
        **kwargs,
    ) -> List[str]:
        """
        Concurrently write multiple JSON files using multiprocessing.

        Args:
            file_data_pairs (list): List of (file path, data) tuples.
            workers (int): Number of parallel processes.
            **kwargs: Additional arguments for json.dump.

        Returns:
            list: Paths successfully written.
        """
        task_args = [(path, data, kwargs) for path, data in file_data_pairs]

        with Pool(processes=workers) as pool:
            results = pool.map(save_json_file, task_args)

        return [r for r in results if r is not None]
