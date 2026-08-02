import subprocess

from adb.adb_path import adb_path

online_devices = []


def check_online_devices():
    if not online_devices:
        raise ValueError("No online devices found")


def get_online_devices():

    print("\nPreparing to start...\n")

    try:
        result = subprocess.run(
            [adb_path, "devices", "-l"], check=True, capture_output=True, text=True
        )

        for i in result.stdout.splitlines()[1:]:
            if not i.strip():
                continue
            online_devices.append(i.split()[0])

        check_online_devices()

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


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


get_online_devices()
