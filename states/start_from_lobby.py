import time
from opencv.template_match import match_template
from adb.action import click
from utils.load_config import load_config

def start_from_lobby(bot, state_enum):
    config = load_config()
    buy_boost = config.get("Buy_Boost", False)
    buy_multi_boost = config.get("Buy_Multi_Boost", False)

    next_boost = [
        (buy_boost, state_enum.BuyBoost),
        (buy_multi_boost, state_enum.RandomBoost)
    ]

    if match_template("lobby") and bot.state == state_enum.StartFromLobby:
        click((807, 619), (1112, 668))
        time.sleep(2)
        for selected, state in next_boost:
            if selected:
                return bot.update(state)
        return bot.update(state_enum.StartFromBoost)
    else:
        return False
