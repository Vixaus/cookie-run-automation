from opencv.template_match import match_template
from adb.action import click_position
import time

def start_game(bot, state_enum):
    if match_template("lobby") and bot.state == state_enum.StartGame:
        print("starting the game")
        click_position((807, 619), (1112, 668))
        time.sleep(2)
        return bot.update(state_enum.SelectBoost)
    else:
        print("lobby not found")
