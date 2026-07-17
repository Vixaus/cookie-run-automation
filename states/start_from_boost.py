from opencv.template_match import match_template
from adb.action import click_position
import time

def start_from_boost(bot, state_enum):
    time.sleep(2)
    if match_template("play") and bot.state == state_enum.StartFromBoost:
        print("starting the game")
        click_position((807, 619), (1112, 668))
        time.sleep(2)
        return bot.update(state_enum.Idle)
    else:
        print("play button not found")
