import subprocess
from pathlib import Path

adb_path = r"C:\LDPlayer\LDPlayer14\adb.exe"
file_path = Path(r"templates\screen.png")

result = subprocess.run([adb_path, "exec-out", "screencap", "-p"], capture_output=True)

with open(file_path, "wb") as f:
    f.write(result.stdout)
