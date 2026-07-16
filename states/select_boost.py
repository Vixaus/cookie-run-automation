from opencv.template_match import match_template
from adb.action import click_position
import time

def select_boost(bot, state_enum):
    if match_template("boost") and bot.state == state_enum.SelectBoost:
        print("buying Multi Boost")
        click_position((1070, 178), (1120, 208))
        time.sleep(2)
        click_position((545, 570), (716, 609))
        return
    else:
        print("boost screen not found")
