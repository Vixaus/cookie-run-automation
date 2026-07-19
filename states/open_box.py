from opencv.template_match import match_template
from adb.action import click
import time

def open_box(bot, state_enum):

    for _ in range(2):
        time.sleep(2)
        click((528,621), (742,655))

    if match_template("open_box") and bot.state == state_enum.OpenBox:
        return False
    return bot.update(state_enum.Idle)
