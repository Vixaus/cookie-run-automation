from pathlib import Path

adb_path = Path(__file__).parent.parent / "tools" / "adb.exe"

if not adb_path.exists():
    raise RuntimeError("adb not found")
