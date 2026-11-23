from vision.ocr import get_reader

from .match_template import capture_screen


def match_text(device_Id: str, arg: list, tl=(0, 0), br=(1280, 720)):
    _, gray = capture_screen(device_Id, tl, br)
    reader = get_reader()
    result = reader.readtext(gray)

    for i, _ in enumerate(result):
        box, text, _ = result[i]
        clean_text = text.lower().replace("~", "-")

        if clean_text in [t.lower() for t in arg]:
            center_x = round(sum(result[0] for result in box) / 4)
            center_y = round(sum(result[1] for result in box) / 4)

            screen_center_x = tl[0] + center_x
            screen_center_y = tl[1] + center_y

            return screen_center_x, screen_center_y, clean_text

    return 0, 0, ""
