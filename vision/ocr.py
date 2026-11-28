import sys
import warnings
from pathlib import Path

import easyocr

# Harmless torch notices easyocr triggers on CPU-only machines (the packaged app has no
# CUDA). They go to stderr, which the app's console shows in red as if the bot failed.
warnings.filterwarnings("ignore", message=r".*quantized tensor creation functions")
warnings.filterwarnings("ignore", message=r".*'pin_memory' argument is set as true")

_reader = None


def get_reader():
    global _reader

    if _reader is None:
        if getattr(sys, "frozen", False):
            # Packaged app: the models ship inside the bundle (see cookie-bot.spec),
            # so nothing is downloaded on the user's machine.
            models = Path(sys._MEIPASS) / "easyocr_models"
            _reader = easyocr.Reader(
                ["en"],
                model_storage_directory=str(models),
                download_enabled=False,
                verbose=False,  # drops the "Neither CUDA nor MPS" notice
            )
        else:
            _reader = easyocr.Reader(["en"], gpu=True, verbose=False)

    return _reader
