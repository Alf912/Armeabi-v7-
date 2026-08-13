"""Android host abstraction for Ninja.

The host supplies an application-private writable directory to the engine.
This module intentionally does not depend on an Android SDK at import time,
so the Python core remains testable outside Android.
"""

from pathlib import Path


class AndroidHost:
    def __init__(self, files_dir):
        self.files_dir = Path(files_dir).expanduser().resolve()
        self.ninja_data_dir = self.files_dir / "ninja"
        self.ninja_data_dir.mkdir(parents=True, exist_ok=True)

    def get_ninja_data_dir(self):
        return self.ninja_data_dir

    def create_engine(self):
        from ninja.engine import create_default_engine
        return create_default_engine(self.ninja_data_dir)
