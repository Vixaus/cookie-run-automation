import argparse
import os
import sys
import threading
import time

from automation.bridge import emit
from config.config import (
    create_config,
    default_config,
    load_config,
    set_config_dir,
)

STOP_TIMEOUT = 10  # seconds to wait for all bot threads after "stop"
STOP_POLL = 0.2  # seconds between checks of the stdin pipe


def _stdin_pipe():
    """stdin's Windows handle if it is a pipe (started by the app), else None."""
    import _winapi
    import msvcrt

    handle = msvcrt.get_osfhandle(sys.stdin.fileno())
    try:
        _winapi.PeekNamedPipe(handle, 0)
    except BrokenPipeError:
        return handle  # already closed: the poll loop stops at once
    except OSError:
        return None  # a console: someone types "stop"
    return handle


def _poll_pipe_for_stop(handle):
    import _winapi

    buffer = b""
    while True:
        try:
            available = _winapi.PeekNamedPipe(handle, 0)[0]
        except OSError:  # the app closed our stdin: it quit or crashed
            return
        if not available:
            time.sleep(STOP_POLL)
            continue
        buffer += os.read(sys.stdin.fileno(), available)
        *lines, buffer = buffer.split(b"\n")
        if any(line.strip() == b"stop" for line in lines):
            return


def wait_for_stop():
    """Return when "stop" arrives on stdin, or stdin closes.

    On Windows, a thread blocked reading a stdin pipe freezes the other threads
    whenever they load a DLL that has its own C runtime (numpy, cv2, torch): the
    loader checks the standard handles and waits for that read to finish. The
    bots would hang on `import numpy` until "stop" arrived. So we never leave a
    read waiting there: peek at the pipe, and read only what's already in it.
    """
    if sys.platform == "win32":
        handle = _stdin_pipe()
        if handle is not None:
            _poll_pipe_for_stop(handle)
            return

    for line in sys.stdin:  # blocks until a line arrives; ends when stdin closes
        if line.strip() == "stop":
            return


def get_config(device_id):
    """Load device config; keys added since it was saved get their defaults."""
    config = load_config(device_id)
    return {**default_config, **config} if config else create_config(device_id)


def start_bot(device_id, config, stop_event):
    # Imported here so --list-devices / --default-config don't load the
    # vision stack (easyocr, torch), which takes seconds.
    from states.base import bot_state

    try:
        bot_state().run(device_id, config, stop_event)
    except Exception as e:
        emit("error", device=device_id, msg=f"{type(e).__name__}: {e}")
        raise


def run_bots(device_ids):
    stop_event = threading.Event()

    threads = []
    for device_id in device_ids:
        config = get_config(device_id)
        # daemon=True: if a thread is stuck in a long loop when we stop,
        # it can't keep the process alive after the timeout below.
        t = threading.Thread(
            target=start_bot, args=(device_id, config, stop_event), daemon=True
        )
        t.start()
        threads.append(t)

    emit("started", devices=device_ids)

    wait_for_stop()

    emit("stopping")
    stop_event.set()
    deadline = time.monotonic() + STOP_TIMEOUT
    for t in threads:
        t.join(timeout=max(0, deadline - time.monotonic()))
    emit("stopped")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--list-devices", action="store_true")
    p.add_argument("--default-config", action="store_true")
    p.add_argument("--devices", default="")
    p.add_argument("--config-dir", default=None)
    args = p.parse_args()

    if args.config_dir:
        set_config_dir(args.config_dir)

    if args.default_config:
        emit("default_config", config=default_config)
        return

    if args.list_devices:
        from adb.device import AdbError, get_online_devices

        try:
            emit("devices", devices=get_online_devices())
        except AdbError as e:
            sys.exit(str(e))  # one line on stderr: the app shows it as the error
        return

    device_ids = [d for d in args.devices.split(",") if d]
    if not device_ids:
        p.error("pass --devices, --list-devices or --default-config")

    run_bots(device_ids)


if __name__ == "__main__":
    main()
