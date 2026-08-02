import easyocr

_reader = None


def get_reader():
    global _reader

    if _reader is None:
        _reader = easyocr.Reader(["en"], gpu=True)

    return _reader
