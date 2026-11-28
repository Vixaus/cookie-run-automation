import random
import subprocess
import time
from dataclasses import dataclass

from adb.adb_path import adb_path
from custom_types.types import Vector


@dataclass
class ClickAction:
    tl: Vector
    br: Vector
    wait: float


def swipe(device_id: str, start: Vector, end: Vector, duration: int):
    subprocess.run(
        [
            adb_path,
            "-s",
            device_id,
            "shell",
            "input",
            "swipe",
            str(start[0]),
            str(start[1]),
            str(end[0]),
            str(end[1]),
            str(duration),
        ],
        check=True,
        stdin=subprocess.DEVNULL,  # see capture_screen in vision/match_template.py
    )


def click(device_id: str, tl: Vector, br: Vector):

    x = random.randint(tl[0], br[0])
    y = random.randint(tl[1], br[1])

    subprocess.run(
        [
            adb_path,
            "-s",
            device_id,
            "shell",
            "input",
            "tap",
            str(x),
            str(y),
        ],
        check=True,
        stdin=subprocess.DEVNULL,  # see capture_screen in vision/match_template.py
    )


def click_sequence(device_id: str, cs: list[ClickAction]):
    for action in cs:
        click(device_id, action.tl, action.br)
        time.sleep(action.wait)
