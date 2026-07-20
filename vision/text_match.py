import easyocr
from .template_match import capture_screen

def match_text(arg: list, tl = (0,0), br = (1280, 720)):
    _, gray = capture_screen(tl, br)
    reader = easyocr.Reader(['en'], gpu=True)
    result = reader.readtext(gray)

    if not result:

        return False


    for i, _ in enumerate(result):
        box, text, _ = result[i]
        if text.lower() in [t.lower() for t in arg]:
            center_x = round(sum(result[0] for result in box) / 4)
            center_y = round(sum(result[1] for result in box) / 4)

            screen_center_x = tl[0] + center_x
            screen_center_y = tl[1] + center_y

            return screen_center_x, screen_center_y
    return False
