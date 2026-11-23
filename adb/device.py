import subprocess

from adb.adb_path import adb_path


def get_online_devices():
    """Return serials of devices that `adb devices` reports as ready."""
    result = subprocess.run(
        [adb_path, "devices"], check=True, capture_output=True, text=True
    )
    devices = []
    for line in result.stdout.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device":
            devices.append(parts[0])
    return devices


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
