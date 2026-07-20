from typing import Tuple
from vision.template_match import capture_screen


def match_color(positon: Tuple[int, int]):
    x, y = positon
    ss, _ = capture_screen()
    b, g, r = ss[y, x]

    print(f"color: {r}, {g}, {b}")

match_color((173,392))
match_color((327,392))
match_color((534, 392))
