import asyncio
import json
from typing import Any, Dict, List, Tuple, Union

import aiofiles


class JSONUtilsAsync:
    """
    JSON utility for concurrent async file I/O using aiofiles.
    """

    @staticmethod
    async def load_json_from_file(
        file_path: str, encoding: str = "utf-8"
    ) -> Union[Dict[str, Any], List[Any], None]:
        """
        Load JSON from a file asynchronously.

        Args:
            file_path (str): Path to the JSON file.
            encoding (str): Encoding used.

        Returns:
            dict or list or None: Parsed JSON or None on failure.
        """
        try:
            async with aiofiles.open(file_path, "r", encoding=encoding) as f:
                content = await f.read()
                return json.loads(content)
        except Exception:
            return None

    @staticmethod
    async def save_json_to_file(
        data: Union[Dict[str, Any], List[Any]],
        file_path: str,
        encoding: str = "utf-8",
        **kwargs,
    ) -> Union[str, None]:
        """
        Save JSON to a file asynchronously.

        Args:
            data (dict or list): JSON data to save.
            file_path (str): Output file path.
            encoding (str): Encoding used.
            **kwargs: Additional json.dump args.

        Returns:
            str or None: Path if successful, None otherwise.
        """
        try:
            json_str = json.dumps(data, **kwargs)
            async with aiofiles.open(file_path, "w", encoding=encoding) as f:
                await f.write(json_str)
            return file_path
        except Exception:
            return None

    @staticmethod
    async def load_multiple_json_files(
        file_paths: List[str],
    ) -> Dict[str, Union[Dict[str, Any], List[Any], None]]:
        """
        Concurrently load multiple JSON files asynchronously.

        Args:
            file_paths (list): List of file paths.

        Returns:
            dict: Mapping of file path to JSON data or None on failure.
        """
        tasks = [JSONUtilsAsync.load_json_from_file(path) for path in file_paths]
        results = await asyncio.gather(*tasks)
        return {path: data for path, data in zip(file_paths, results)}

    @staticmethod
    async def save_multiple_json_files(
        file_data_pairs: List[Tuple[str, Union[Dict[str, Any], List[Any]]]], **kwargs
    ) -> List[str]:
        """
        Concurrently write multiple JSON files asynchronously.

        Args:
            file_data_pairs (list): List of (file path, data) tuples.
            **kwargs: Additional json.dump args.

        Returns:
            list: Paths successfully written.
        """
        tasks = [
            JSONUtilsAsync.save_json_to_file(data, path, **kwargs)
            for path, data in file_data_pairs
        ]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r is not None]
