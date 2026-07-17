from typing import Tuple
from opencv.template_match import capture_screen


def match_color(positon: Tuple[int, int]):
    x, y = positon
    ss, _ = capture_screen()
    b, g, r = ss[y, x]

    print(f"color: {r}, {g}, {b}")

match_color((0,0))
