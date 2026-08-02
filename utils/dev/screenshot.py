import subprocess
from pathlib import Path

from adb.adb_path import adb_path

file_path = Path(r"vision/templates/screen.png")
device_id = "emulator-5554"


try:
    result = subprocess.run(
        [adb_path, "-s", device_id, "exec-out", "screencap", "-p"],
        check=True,
        capture_output=True,
    )

    with open(file_path, "wb") as f:
        f.write(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
