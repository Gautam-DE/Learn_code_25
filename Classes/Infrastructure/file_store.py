from __future__ import annotations

from pathlib import Path
from typing import Iterable, List


class FileStore:
    def read_lines(self, path: str) -> List[str]:
        file_path = Path(path)
        if not file_path.exists():
            file_path.touch()
        return file_path.read_text(encoding="utf-8").splitlines()

    def write_lines(self, path: str, lines: Iterable[str]) -> None:
        Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")

    def write_text(self, path: str, content: str) -> None:
        Path(path).write_text(content, encoding="utf-8")
