import json
import sys
import threading

_lock = threading.Lock()


def emit(kind, **data):
    line = json.dumps({"type": kind, **data})
    with _lock:
        sys.stdout.write(line + "\n")
        sys.stdout.flush()
