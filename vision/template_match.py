import subprocess
from pathlib import Path

import numpy as np
import cv2

from adb.device import online_devices
from utils.adb_path import adb_path

type color = tuple[int, int, int]
type vector = tuple[int, int]

templates = {}


def load_templates():
    for file in Path("templates").glob(("*png")):
        templates[file.stem] = cv2.imread(str(file), cv2.IMREAD_GRAYSCALE)


def capture_screen(tl: vector = (0, 0), br: vector = (1280, 720)):
   result = subprocess.run(
       [adb_path, "-s", f"{online_devices[0]}", "exec-out", "screencap", "-p"],
       capture_output=True,
       check=True,
    )

   raw = cv2.imdecode(
      np.frombuffer(result.stdout, dtype=np.uint8),
      cv2.IMREAD_COLOR,
   )


   x1 = tl[0]
   y1 = tl[1]
   x2 = br[0]
   y2 = br[1]

   roi = raw[y1:y2, x1:x2]

   gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

   if roi is None:
      raise RuntimeError(
         f"Could not decode screenshot. ADB stderr: {result.stderr.decode(errors='replace')}"
        )

   return roi, gray


def match_template(img):
    _, gray = capture_screen()
    result = cv2.matchTemplate(
        gray,
        templates[img],
        cv2.TM_CCOEFF_NORMED,
    )

    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    x, y = max_loc
    h, w = templates[img].shape[:2]

    center_matched_pos = (x + w // 2, y + h // 2)

    if max_val >= 0.9:
        return center_matched_pos

    return False

def match_color(rgb: color, positon: vector):
    x, y = positon
    ss, _ = capture_screen()
    b, g, r = ss[y, x]

    if r == rgb[0] and g == rgb[1] and b == rgb[2]:
        return True
    return False

load_templates()
