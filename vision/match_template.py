import subprocess
from pathlib import Path

import cv2
import numpy as np

from adb.adb_path import adb_path
from custom_types.types import Vector
from vision.templates import TemplateType

type Color = tuple[int, int, int]

templates = {}


def load_templates():
    for file in Path("vision/templates").rglob("*.png"):
        templates[file.stem] = cv2.imread(str(file), cv2.IMREAD_GRAYSCALE)


def capture_screen(device_Id: str, tl: Vector = (0, 0), br: Vector = (1280, 720)):
    result = subprocess.run(
        [adb_path, "-s", f"{device_Id}", "exec-out", "screencap", "-p"],
        capture_output=True,
        timeout=10,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"{device_Id}: screencap failed (exit {result.returncode}). "
            f"ADB stderr: {result.stderr.decode(errors='replace').strip()}"
        )

    raw = cv2.imdecode(
        np.frombuffer(result.stdout, dtype=np.uint8),
        cv2.IMREAD_COLOR,
    )

    if raw is None:
        raise RuntimeError(
            f"{device_Id}: Could not decode screenshot. ADB stderr: {result.stderr.decode(errors='replace')}"
        )

    x1 = tl[0]
    y1 = tl[1]
    x2 = br[0]
    y2 = br[1]

    roi = raw[y1:y2, x1:x2]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    return roi, gray


def match_template(device_Id: str, param: TemplateType):

    template = templates.get(param["img"])

    if template is None:
        raise ValueError(f"Template not loaded: {template}")

    _, base_gray = capture_screen(device_Id, param["tl"], param["br"])
    template_h, template_w = template.shape[:2]

    for scale in [1.0, 1.1, 1.2, 1.3, 1.4, 1.5]:
        gray = cv2.resize(base_gray, None, fx=scale, fy=scale)
        image_h, image_w = gray.shape[:2]

        if image_h < template_h or image_w < template_w:
            continue

        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val >= 0.85:
            x, y = max_loc
            return (
                round((x + template_w // 2) / scale) + param["tl"][0],
                round((y + template_h // 2) / scale) + param["tl"][1],
            )

    return False


def match_color(device_Id: str, rgb: Color, positon: Vector):
    x, y = positon
    ss, _ = capture_screen(device_Id)
    b, g, r = ss[y, x]

    if r == rgb[0] and g == rgb[1] and b == rgb[2]:
        return True
    return bool(r == rgb[0] and g == rgb[1] and b == rgb[2])


load_templates()
