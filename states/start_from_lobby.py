from opencv.template_match import match_template
from adb.action import click_position
import time

def start_from_lobby(bot, state_enum):
    time.sleep(1)
    if match_template("lobby") and bot.state == state_enum.StartFromLobby:
        print("starting from lobby")
        click_position((807, 619), (1112, 668))
        time.sleep(2)
        return bot.update(state_enum.SelectBoost)
    else:
        print("lobby not found")
        return bot.update(state_enum.ConfirmPopup)
