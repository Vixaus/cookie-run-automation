import platform
import shutil
from pathlib import Path

os_name = platform.system()
emulator_name = {
    "LDPlayer": Path("C:/LDPlayer/LDPlayer14/adb.exe"),
    "Mumu": Path("C:/Program Files/Netease/MuMuPlayerGlobal-12.0/nx_main/adb.exe")
}

found_adb_path = emulator_name["LDPlayer"] if os_name == "Windows" else ( shutil.which("adb") if os_name == "Darwin" else None )

if found_adb_path is None:
    raise RuntimeError("adb not found")

adb_path: Path | str = found_adb_path
print(f"adb path: {adb_path}")
