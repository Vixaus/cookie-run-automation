from vision.template_match import match_template
from adb.action import click
from vision.templates import OPEN_BOX

import time

def open_box(bot, state_enum):

    if match_template(OPEN_BOX["img"], OPEN_BOX["tl"], OPEN_BOX["br"]) and bot.state == state_enum.OpenBox:
        for _ in range(2):
            time.sleep(2)
            click((528,621), (742,655))

        return bot.update(state_enum.Idle)

    return bot.update(state_enum.MatchEnd)
