from vision.match_template import capture_screen

device_id = "emulator-5554"


def get_color(positon: tuple[int, int]):
    x, y = positon
    ss, _ = capture_screen(device_id)
    b, g, r = ss[y, x]

    print(f"color: {r}, {g}, {b}")


get_color((150, 200))
