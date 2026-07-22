from adb.action import click
from utils.wait import wait
from config.config import load_config

def auto_jump(stop_event):
    delay = load_config()["Auto_Jump_Delay"]

    while not stop_event.is_set():
        wait(delay[0], delay[1])
        click((110, 600), (255, 665))
