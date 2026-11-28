import sys
from pathlib import Path

import easyocr

_reader = None


def get_reader():
    global _reader

    if _reader is None:
        if getattr(sys, "frozen", False):
            # Packaged app: the models ship inside the bundle (see cookie-bot.spec),
            # so nothing is downloaded on the user's machine.
            models = Path(sys._MEIPASS) / "easyocr_models"
            _reader = easyocr.Reader(
                ["en"], model_storage_directory=str(models), download_enabled=False
            )
        else:
            _reader = easyocr.Reader(["en"], gpu=True)

    return _reader
