import time

from adb.action import click
from vision.match_template import match_template
from vision.templates import OPEN_BOX


def open_box(device_id, bot, state_enum, _):

    if match_template(device_id, OPEN_BOX):
        for _ in range(2):
            click(device_id, (600, 625), (690, 661))
            time.sleep(2)

        return bot.update(device_id, state_enum.Idle)

    return bot.update(device_id, state_enum.MatchEnd)
