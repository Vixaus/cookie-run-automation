import subprocess
from pathlib import Path

import numpy as np

import cv2

from utils.adb_path import adb_path

templates = {}


def load_templates():
    for file in Path("templates").glob(("*png")):
        templates[file.stem] = cv2.imread(str(file), cv2.IMREAD_GRAYSCALE)


def capture_screen():
    result = subprocess.run(
        [adb_path, "exec-out", "screencap", "-p"],
        capture_output=True,
        check=True,
    )

    screen = cv2.imdecode(
        np.frombuffer(result.stdout, dtype=np.uint8),
        cv2.IMREAD_COLOR,
    )

    if screen is None:
        raise RuntimeError(
            f"Could not decode screenshot. ADB stderr: {result.stderr.decode(errors='replace')}"
        )

    return cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)


def match_template():
    result = cv2.matchTemplate(
        capture_screen(),
        next(iter(templates.values())),
        cv2.TM_CCOEFF_NORMED,
    )

    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    print(max_val)

    if max_val >= 0.9:
        print("Matched Image")

    return


load_templates()
match_template()
