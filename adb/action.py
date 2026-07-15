import subprocess

from ..utils.adb_path import adb_path
from .device import online_devices


def click_position(x, y):
    subprocess.run(
        [
            adb_path,
            "-s",
            online_devices[0],
            "shell",
            "input",
            "tap",
            str(x),
            str(y),
        ],
        check=True,
    )
