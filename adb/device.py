import socket
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

from adb.adb_path import adb_path

# `adb devices` finds emulators by itself only on ports 5555-5585 (LDPlayer shows up
# as emulator-5554, emulator-5556, ...). MuMu Player 12 needs an `adb connect` first,
# on port 16384 + 32 * instance number (16384, 16416, 16448, ...).
# Not 7555 (old MuMu 6): MuMu 12 also opens it for instance 0, which would list
# that instance twice.
CONNECT_PORTS = [16384 + 32 * i for i in range(16)]

# The first `adb devices` after the adb server stops can fail while it restarts.
ADB_TRIES = 3


class AdbError(RuntimeError):
    pass


def _adb(*args, timeout=10):
    return subprocess.run(
        [adb_path, *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
        stdin=subprocess.DEVNULL,  # see capture_screen in vision/match_template.py
    )


def _port_open(port):
    """True if something listens on 127.0.0.1:port. An open local port answers in
    well under a millisecond; Windows takes seconds to refuse a closed one, hence
    the short timeout."""
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.2):
            return True
    except OSError:
        return False


def _list_devices():
    """{serial: state} from `adb devices`, retrying while the adb server starts."""
    for attempt in range(ADB_TRIES):
        result = _adb("devices")
        if result.returncode == 0:
            devices = {}
            for line in result.stdout.splitlines()[1:]:
                parts = line.split()
                if len(parts) >= 2:
                    devices[parts[0]] = parts[1]
            return devices
        time.sleep(1 + attempt)
    error = (result.stderr or result.stdout).strip().splitlines()
    raise AdbError(f"adb devices failed: {error[-1] if error else 'no output'}")


# While MuMu boots, its port is already open but adb inside it doesn't answer yet,
# so `adb connect` hangs. Give up on that port; the next scan tries again.
CONNECT_TIMEOUT = 5


def _connect(port):
    try:
        _adb("connect", f"127.0.0.1:{port}", timeout=CONNECT_TIMEOUT)
    except subprocess.TimeoutExpired:
        pass


def _connect_emulators(known):
    """`adb connect` every emulator port that is open but not listed yet."""
    ports = [p for p in CONNECT_PORTS if known.get(f"127.0.0.1:{p}") != "device"]
    with ThreadPoolExecutor(max_workers=len(ports) or 1) as pool:
        open_ports = [
            p for p, is_open in zip(ports, pool.map(_port_open, ports)) if is_open
        ]
        # In parallel, so one booting instance doesn't hold up the others.
        list(pool.map(_connect, open_ports))
    return bool(open_ports)


def get_online_devices():
    """Return serials of devices that `adb devices` reports as ready."""
    devices = _list_devices()
    if _connect_emulators(devices):
        devices = _list_devices()
    return [serial for serial, state in devices.items() if state == "device"]


# def open_cookie_run():
#     subprocess.run(
#         [
#             adb_path,
#             "-s",
#             online_devices[0],
#             "shell",
#             "am",
#             "start",
#             "-n",
#             "com.devsisters.crg/com.devsisters.CookieRunForKakao.OvenbreakX",
#         ],
#        check=True,
#     )
