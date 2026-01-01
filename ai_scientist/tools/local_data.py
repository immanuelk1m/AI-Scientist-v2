import csv
import json
import os
import os.path as osp
from itertools import islice
from typing import Any, Dict, List, Optional

from ai_scientist.tools.base_tool import BaseTool


class LocalDataReadTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="ReadLocalData",
            description=(
                "Read a local data file (txt, md, csv, tsv, json, jsonl) and return "
                "a small preview for ideation. Use this to inspect datasets." 
                "Paths must be inside the repository."
            ),
            parameters=[
                {
                    "name": "path",
                    "type": "str",
                    "description": "File path relative to repo root (or absolute path inside repo).",
                },
                {
                    "name": "max_chars",
                    "type": "int",
                    "description": "Maximum characters to return for text previews (default: 4000).",
                },
                {
                    "name": "max_rows",
                    "type": "int",
                    "description": "Maximum rows/items to return for CSV/JSON previews (default: 20).",
                },
            ],
        )

    def use_tool(
        self, path: str, max_chars: int = 4000, max_rows: int = 20
    ) -> str:
        repo_root = osp.abspath(osp.join(osp.dirname(__file__), "..", ".."))
        if not osp.isabs(path):
            full_path = osp.abspath(osp.join(repo_root, path))
        else:
            full_path = osp.abspath(path)

        if not full_path.startswith(repo_root + os.sep):
            return (
                f"Error: path must be inside the repository root ({repo_root}). "
                f"Got: {full_path}"
            )

        if not osp.exists(full_path):
            return f"Error: file not found: {full_path}"

        ext = osp.splitext(full_path)[1].lower()
        size_bytes = osp.getsize(full_path)

        if ext in {".csv", ".tsv"}:
            return self._preview_csv(full_path, ext, max_rows, size_bytes)
        if ext in {".json", ".jsonl"}:
            return self._preview_json(full_path, ext, max_rows, max_chars, size_bytes)

        return self._preview_text(full_path, max_chars, size_bytes)

    def _preview_csv(
        self, path: str, ext: str, max_rows: int, size_bytes: int
    ) -> str:
        delimiter: Optional[str] = "\t" if ext == ".tsv" else None
        rows: List[List[str]] = []
        with open(path, "r", encoding="utf-8", errors="replace", newline="") as f:
            if delimiter is None:
                sample = f.read(4096)
                f.seek(0)
                try:
                    dialect = csv.Sniffer().sniff(sample)
                except csv.Error:
                    dialect = csv.excel
            else:
                dialect = csv.excel_tab
            reader = csv.reader(f, dialect)
            rows = list(islice(reader, max_rows))

        if not rows:
            return f"File: {path} (bytes: {size_bytes})\nPreview: <empty>"

        header = rows[0]
        body = rows[1:]
        lines = ["\t".join(header)]
        lines.extend("\t".join(row) for row in body)
        preview = "\n".join(lines)
        return (
            f"File: {path} (bytes: {size_bytes})\n"
            f"Preview (tab-separated):\n{preview}"
        )

    def _preview_json(
        self,
        path: str,
        ext: str,
        max_rows: int,
        max_chars: int,
        size_bytes: int,
    ) -> str:
        if ext == ".jsonl":
            items = []
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                for line in islice(f, max_rows):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        items.append(json.loads(line))
                    except json.JSONDecodeError:
                        items.append(line)
            return (
                f"File: {path} (bytes: {size_bytes})\n"
                f"Preview (first {len(items)} items):\n"
                f"{json.dumps(items, ensure_ascii=True, indent=2)[:max_chars]}"
            )

        if size_bytes > 2_000_000:
            return self._preview_text(path, max_chars, size_bytes)

        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            return self._preview_text(path, max_chars, size_bytes)

        if isinstance(data, list):
            preview_data = data[:max_rows]
        elif isinstance(data, dict):
            preview_data = {k: data[k] for k in list(data.keys())[:max_rows]}
        else:
            preview_data = data

        return (
            f"File: {path} (bytes: {size_bytes})\n"
            f"Preview:\n"
            f"{json.dumps(preview_data, ensure_ascii=True, indent=2)[:max_chars]}"
        )

    def _preview_text(self, path: str, max_chars: int, size_bytes: int) -> str:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            preview = f.read(max_chars)
        suffix = "" if len(preview) < max_chars else "\n...<truncated>"
        return (
            f"File: {path} (bytes: {size_bytes})\n"
            f"Preview:\n{preview}{suffix}"
        )
