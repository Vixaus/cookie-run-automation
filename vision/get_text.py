import cv2

from vision.ocr import get_reader

from .match_template import capture_screen


def get_text(device_Id: str, tl=(0, 0), br=(1280, 720), digits_only=False) -> list[str]:
    text_list = []

    _, gray = capture_screen(device_Id, tl, br)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    reader = get_reader()
    result = reader.readtext(
        gray, text_threshold=0.5, allowlist="0123456789," if digits_only else None
    )

    if not result:
        return ["0"] if digits_only else [""]

    for i, _ in enumerate(result):
        _, text, _ = result[i]
        text_list.append(text)

    return text_list
