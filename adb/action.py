import subprocess
import random
import time

from dataclasses import dataclass
from config.adb_path import adb_path
from .device import online_devices

type vector = tuple[int, int]

@dataclass
class ClickAction:
    tl: vector
    br: vector
    wait: float


def click(tl: vector, br: vector):

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

def click_sequence(cs: list[ClickAction]):
    for action in cs:
        click(action.tl, action.br)
        time.sleep(action.wait)
