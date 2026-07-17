import shutil

found_adb_path = shutil.which("adb")
if found_adb_path is None:
    raise RuntimeError("adb not found")

adb_path: str = found_adb_path
