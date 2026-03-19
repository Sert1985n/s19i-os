from __future__ import annotations

from pathlib import Path


class UpdateService:
    def __init__(self, staging_dir: str = "/tmp/s19i-os-staging") -> None:
        self.staging_dir = Path(staging_dir)

    def status(self) -> dict:
        self.staging_dir.mkdir(parents=True, exist_ok=True)
        staged = sorted(p.name for p in self.staging_dir.iterdir() if p.is_file())
        return {
            "staging_dir": str(self.staging_dir),
            "staged_files": staged,
        }
