import argparse
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


def get_config(device_id):
    """Load device config; create a fresh one if missing or outdated."""
    config = load_config(device_id)
    if not config or not set(default_config).issubset(set(config)):
        config = create_config(device_id)
    return config


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

    for line in sys.stdin:  # blocks until a line arrives; ends when stdin closes
        if line.strip() == "stop":
            break

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
        from adb.device import get_online_devices

        emit("devices", devices=get_online_devices())
        return

    device_ids = [d for d in args.devices.split(",") if d]
    if not device_ids:
        p.error("pass --devices, --list-devices or --default-config")

    run_bots(device_ids)


if __name__ == "__main__":
    main()
