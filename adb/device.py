import subprocess

from utils.adb_path import adb_path

online_devices = []


def get_online_devices():
    try:
        result = subprocess.run(
            [adb_path, "devices", "-l"], check=True, capture_output=True, text=True
        )
        for i in result.stdout.splitlines()[1:]:
            if not i.strip():
                continue
            online_devices.append(i.split()[0])
        print(f"Online devices: {online_devices}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def open_cookie_run():
    subprocess.run(
        [
            adb_path,
            "-s",
            online_devices[0],
            "shell",
            "am",
            "start",
            "-n",
            "com.devsisters.crg/com.devsisters.CookieRunForKakao.OvenbreakX",
        ],
        check=True,
    )

get_online_devices()
