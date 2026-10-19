
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def analyze_python(code: str) -> list[dict]:
    if not code.strip():
        return []

    with tempfile.TemporaryDirectory() as temp_dir:
        target = Path(temp_dir) / "sample.py"
        target.write_text(code, encoding="utf-8")

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "ruff",
                "check",
                "--output-format",
                "json",
                str(target),
            ],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )

        if result.returncode not in (0, 1):
            raise RuntimeError(result.stderr[:500])

        findings = json.loads(result.stdout or "[]")

        return [
            {
                "rule": item.get("code"),
                "message": item.get("message"),
                "line": item.get("location", {}).get("row"),
            }
            for item in findings
        ]
