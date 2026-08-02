from adb.action import click
from utils.wait import wait


def auto_jump(device_id, stop_event, config):
    delay = config["Auto_Jump_Delay"]

    while not stop_event.is_set():
        wait(delay[0], delay[1])
        click(device_id, (129, 607), (212, 650))
