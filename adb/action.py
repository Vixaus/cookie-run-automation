import subprocess
import random

from utils.adb_path import adb_path
from .device import online_devices

type vector = tuple[int, int]

def click_position(tl: vector, br: vector):

    x = random.randint(tl[0], br[0])
    y = random.randint(tl[1], br[1])

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
