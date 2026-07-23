import subprocess
from config.adb_path import adb_path
from pathlib import Path

file_path = Path(r"vision/templates/screen.png")

result = subprocess.run([adb_path, "exec-out", "screencap", "-p"], capture_output=True)

with open(file_path, "wb") as f:
    f.write(result.stdout)
