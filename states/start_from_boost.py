import time
from opencv.template_match import match_template
from adb.action import click


def start_from_boost(bot, state_enum):
    if match_template("play") and bot.state == state_enum.StartFromBoost:
        print("starting the game")
        time.sleep(1.5)
        click((807, 619), (1112, 668))
        return bot.update(state_enum.InGame)
    else:
        print("play button not found")
