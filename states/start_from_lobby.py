import time
from vision.template_match import match_template
from adb.action import click
from config.config import load_config
from vision.templates import LOBBY

def start_from_lobby(bot, state_enum):
    config = load_config()
    buy_boost = config.get("Buy_Boost", False)
    buy_multi_boost = config.get("Buy_Multi_Boost", False)

    next_boost = [
        (buy_boost, state_enum.BuyBoost),
        (buy_multi_boost, state_enum.RandomBoost)
    ]

    if match_template(LOBBY["img"], LOBBY["tl"], LOBBY["br"]) and bot.state == state_enum.StartFromLobby:
        click((807, 619), (1112, 668))
        time.sleep(2)
        for selected, state in next_boost:
            if selected:
                return bot.update(state)
        return bot.update(state_enum.StartFromBoost)
    else:
        return bot.update(state_enum.Idle)
