from __future__ import annotations

import os
from typing import Final

DEFAULT_VSTORAGE_PATH: Final[str] = "/data/vstorage"


def _resolve_target_path() -> str:
    path = os.getenv("VSTORAGE_PATH", DEFAULT_VSTORAGE_PATH)

    if path.endswith(os.sep):
        raise ValueError(
            "VSTORAGE_PATH must point to a file. Got a directory-like path ending with a separator.",
        )

    if os.path.isdir(path):
        raise ValueError(
            "VSTORAGE_PATH points to a directory. Configure it to reference the log file directly.",
        )

    return path


def append_to_vstorage(line: str) -> None:
    path = _resolve_target_path()
    directory = os.path.dirname(path)

    if directory:
        os.makedirs(directory, exist_ok=True)

    data = line.rstrip("\n") + "\n"

    with open(path, "a", encoding="utf-8") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
